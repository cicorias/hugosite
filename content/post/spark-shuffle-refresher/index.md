---
title: "Getting Back Up to Speed on Spark Shuffling"
date: 2026-05-22T09:00:00-05:00
slug: "spark-shuffle-refresher"
draft: false
tags: ["spark", "databricks", "data-engineering", "azure", "distributed-systems"]
summary: "An interview question about Spark shuffling sent me back to basics after five years away. I built a runnable Databricks demo covering shuffles, joins, skew, AQE, and Photon — here's what I relearned and what's changed."
feature_image: "/images/2026/05/spark-shuffle-hero.png"
aliases:
  - /spark-shuffle-refresher/
---

A few weeks back I was in an interview and got asked about Spark shuffling. I've been working at a higher stack level for a few years now — cloud architecture, platform engineering, AI/ML infra — and while the fundamentals are all still in there, the smooth recall that comes from daily use had faded. I knew the concepts. I couldn't walk through them cleanly under pressure.

That bothered me.

So I built a runnable demo — a Databricks Asset Bundle with five groups of notebooks that actually execute, produce real output, and let you watch the Spark UI while things happen. All data is synthetic and generated at runtime. The repo is [spark-shuffle-demo-diag](https://github.com/cicorias/spark-shuffle-demo-diag) and it covers shuffle fundamentals, join strategies, skew and salting, observability, and Photon. This post is the companion writeup: what I was refreshing, why it matters, and what's genuinely new since I last worked with Spark day-to-day.

Some context on where I was coming from: I spent years in the weeds of Spark and Hadoop at a large rideshare company, building and operating a custom PaaS that ran Spark workloads at scale. At that layer you get deep into scheduler internals, executor memory models, shuffle file management, and the plumbing that most people never see. Coming back after five years, the fundamentals are unchanged — it's still the same shuffle problem — but the ecosystem around it has gotten meaningfully better.

---

## The core problem: why shuffles are expensive

Apache Spark processes data across a cluster by breaking work into tasks that run in parallel on partitions. Most transformations are *narrow* — each output partition depends on exactly one input partition, so tasks work independently and nothing crosses the network. `filter`, `select`, `map`, `withColumn` are all narrow.

Shuffles happen when that independence breaks. The moment you need every record with the same key on the same machine — for a `groupBy`, a `join`, a `distinct` — Spark has to redistribute data across the cluster. That's a wide transformation.

The cost is layered: Spark serializes records, writes them to local disk bucketed by destination partition (the map side), ships them over the network to the right executors (the shuffle transfer), then reads and deserializes them on the receiving side (the reduce side). On large datasets this can dominate total job runtime.

Here's what the simplest possible demo looks like in practice:

```python
# Narrow — no shuffle, no Exchange in the plan
narrow = (
    events
    .filter(F.col("event_type") == "purchase")
    .select("user_id", "value")
    .withColumn("value_usd", F.col("value") * 1.08)
)
narrow.explain("formatted")   # FileScan → Filter → Project — no Exchange node

# Wide — forces a shuffle
wide = (
    events
    .groupBy("user_id")
    .agg(F.count("*").alias("event_count"), F.sum("value").alias("total_value"))
)
wide.explain("formatted")   # FileScan → HashAggregate → Exchange → HashAggregate
```

The `explain` output tells the story directly. No `Exchange` node means no shuffle. When you see `Exchange hashPartitioning(user_id, N)`, that's the shuffle point — every record gets routed to one of N partitions based on `hash(user_id) % N`, and the stage boundary sits right there.

The DAG visualization in the Spark UI makes this visual: each stage boundary is exactly one shuffle.

![Narrow vs. wide transformation notebook output](/images/2026/05/spark-narrow-vs-wide.png)

One thing Spark does well automatically: for `groupBy + count()` and `groupBy + sum()`, it performs a *partial aggregation* on the map side before the shuffle. Instead of shipping every event row, each map task ships pre-aggregated `(user_id, partial_count)` pairs. The reduce side just merges them. That's why `groupByKey` followed by manual counting is so much slower — it ships every value across the network before aggregating.

---

## Joins: the other big shuffle source

Joins are where shuffles hurt most in practice. The default join strategy is sort-merge: both sides are shuffled on the join key so matching rows land on the same executor, then sorted and merged. For two large tables, you're moving the entire dataset twice.

```python
# Sort-merge join — both sides shuffled, two Exchange nodes in the plan
shuffle_join = orders.join(customers, "customer_id")
shuffle_join.explain("formatted")
# → Exchange + Exchange + SortMergeJoin

# Broadcast join — zero shuffles
from pyspark.sql import functions as F
broadcast_join = orders.join(F.broadcast(customers), "customer_id")
broadcast_join.explain("formatted")
# → BroadcastHashJoin, no Exchange for the large side
```

The `broadcast()` hint ships the small table to every executor so the large table never moves. Spark's default threshold is 10MB; you can push it to several hundred MB safely depending on your executor memory.

What's changed: Adaptive Query Execution (AQE), which is on by default in Spark 3.x and all current Databricks runtimes, can do this conversion automatically. After the first stage finishes, AQE looks at the actual size statistics and — if one side turned out to be small — converts a planned sort-merge join into a broadcast join on the fly. You get the win without the hint, as long as the statistics reveal themselves at runtime.

![Broadcast vs. shuffle join notebook output](/images/2026/05/spark-broadcast-vs-shuffle.png)

The practical lesson: use explicit broadcast hints when you know your data shape. Trust AQE when you don't, but don't assume it will always fire — sometimes statistics aren't available until too late.

---

## Skew: when shuffles go wrong

Shuffles assume keys are roughly evenly distributed across partitions. When they're not, you get skew: one reducer task processes a disproportionate share of the data while the others finish quickly. Spark's stage doesn't complete until the last task finishes, so one straggler holds everything up.

The demo makes this concrete by generating a dataset where `user_id = 1` owns 40% of all rows. With 10 shuffle partitions and AQE disabled:

```python
spark.conf.set("spark.sql.shuffle.partitions", "10")
spark.conf.set("spark.sql.adaptive.enabled", "false")

skewed_agg = (
    skewed
    .groupBy("user_id")
    .agg(F.sum("value").alias("total_value"), F.count("*").alias("event_count"))
)
skewed_agg.write.mode("overwrite").parquet(skewed_out)
```

In the Spark UI, the Stages tab shows 10 tasks in the shuffle stage — nine finish quickly, one runs roughly 4× longer. The Input Size column makes it explicit: one task has a massive input partition; the others are uniformly small.

The classic mitigation is salting: append a random suffix to the hot key before the first aggregation, then strip it and aggregate a second time.

```python
SALT_BUCKETS = 10

# Pass 1: salt and partially aggregate
salted = (
    skewed
    .withColumn("salt", (F.rand(seed=17) * SALT_BUCKETS).cast("int"))
    .withColumn("salted_key", F.concat(F.col("user_id").cast("string"), F.lit("_"), F.col("salt").cast("string")))
    .groupBy("user_id", "salted_key")
    .agg(F.sum("value").alias("partial_sum"), F.count("*").alias("partial_count"))
)

# Pass 2: strip salt and finalize
desalted = (
    salted
    .groupBy("user_id")
    .agg(F.sum("partial_sum").alias("total_value"), F.sum("partial_count").alias("event_count"))
)
```

`user_id=1` now appears as `1_0`, `1_1`, …, `1_9` in pass 1. The hot key is spread across 10 partitions instead of one. Total CPU work may be similar or even slightly higher (two passes), but elapsed wall-clock time drops because the work is balanced across executors.

![Skew and salting notebook output](/images/2026/05/spark-skew-salting.png)

AQE's skew join handling can sometimes do this automatically — it detects oversized shuffle partitions and splits them without requiring manual salting. But it only works for joins, not arbitrary aggregations, and it requires the skew to be visible in post-shuffle statistics. For aggregation skew, salting is still often the right tool.

---

## AQE in depth

AQE deserves its own section because it's changed the tuning calculus meaningfully. In Spark 2.x and earlier, the optimizer planned the entire query upfront based on table statistics that were often stale or missing. You had to set `spark.sql.shuffle.partitions` correctly up front, handle skew manually, and add broadcast hints yourself.

AQE runs after each shuffle stage completes and re-plans downstream stages using actual data statistics. It does three things automatically:

1. **Partition coalescing**: if shuffle output produces many tiny partitions, AQE merges them to avoid task overhead
2. **Dynamic broadcast conversion**: if a join side turns out to be smaller than the broadcast threshold at runtime, AQE converts a sort-merge join to broadcast
3. **Skew join splitting**: if one shuffle partition is significantly larger than the median, AQE splits it across multiple tasks

```python
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "10485760")  # 10 MB

aqe_join = orders.join(customers, "customer_id")
aqe_join.explain("formatted")
# → AdaptiveSparkPlan wrapping the join
# physical plan may show BroadcastHashJoin even though you wrote plain .join()
```

Watch for `AdaptiveSparkPlan` in the explain output — that's the AQE wrapper. The inner plan may change between the time you call `explain` and the time the query actually runs.

![AQE in action notebook output](/images/2026/05/spark-aqe-in-action.png)

---

## Catalyst, Photon, and the Databricks stack

A quick layer-by-layer summary of what's actually running when you execute a Databricks query today:

**Catalyst** is Spark's query optimizer. It takes your DataFrame or SQL code through analysis (resolving column names), logical optimization (predicate pushdown, column pruning, constant folding, join reordering), physical planning (choosing join strategies, scan methods), and code generation (whole-stage codegen fuses operators within a stage into a single tight JVM method). You can see all four plans by calling `df.explain(True)`.

**Photon** is Databricks' native vectorized execution engine, written in C++. Catalyst still plans the query, but Photon takes over at the execution layer — processing data in columnar batches rather than row by row, using SIMD instructions, and completely bypassing the JVM for supported operators. This isn't the same thing as whole-stage codegen; codegen makes the JVM faster, Photon skips the JVM entirely.

When Photon encounters an unsupported operation — certain window functions, some UDF patterns, some data types — it transparently falls back to the Spark JVM runtime for that portion. You'll see hybrid plans in the Spark UI where some operators say "Photon" and others don't.

**Photon's implication for shuffle tuning**: Photon makes the non-shuffle portions of your query faster, which means shuffles dominate an even larger fraction of total time than they did on JVM-only Spark. Shuffle tuning matters *more* on Databricks, not less.

![Photon vs. JVM notebook output](/images/2026/05/spark-photon-vs-jvm.png)

**Predictive Query Execution (PQE)** is the newest addition, announced mid-2025. AQE improved on static planning by re-planning at stage boundaries. PQE goes further — it introduces a continuous feedback loop that can react *within* a running stage, before the shuffle completes. Combined with Photon Vectorized Shuffle, Databricks claims roughly 25% query speedup on top of existing gains, rolling out automatically for DBSQL Serverless warehouses.

**Delta Lake** sits underneath all of this. `OPTIMIZE` with `ZORDER BY`, and the newer Liquid Clustering, pre-cluster data on disk by the columns you commonly filter or join on. That enables file skipping at scan time and can let queries avoid shuffles via partition pruning before Catalyst even gets involved.

---

## What the demo covers

The [spark-shuffle-demo-diag](https://github.com/cicorias/spark-shuffle-demo-diag) repo runs on Azure Databricks using Databricks Asset Bundles with DBR 17.3 LTS Photon (Spark 4.0). All infrastructure is version-controlled, all data is synthetic and generated at runtime.

| Group | What you observe |
|-------|-----------------|
| 01 — Shuffle Fundamentals | `filter` vs. `groupBy` plan; `Exchange` node; stage count; DBFS partition files |
| 02 — Join Strategies | Sort-merge vs. broadcast; AQE auto-broadcast; plan differences |
| 03 — Skew & AQE | Straggler task in the Stages tab; salting two-pass; AQE skew split |
| 04 — Observability | `explain("formatted")`; DAG walkthrough; `dbutils.fs.ls()` on shuffle files |
| 05 — Photon vs. JVM | Photon operators in the query plan; UDF fallback cost; benchmark comparison |

Setup is `mise install` → auth → `databricks bundle deploy` → `databricks bundle run run_all`.

---

## Practical takeaways

The fundamentals haven't changed. What's different is how much the engine now handles automatically:

- **Filter and project before you join or aggregate.** You shuffle less data; everything downstream is cheaper.
- **Broadcast small dimension tables.** Use the explicit hint when you know the shape; let AQE handle it when you don't.
- **Watch `spark.sql.shuffle.partitions`.** The default of 200 is wrong for almost everyone. Target 100–200MB per partition. AQE's partition coalescing helps but doesn't replace getting this roughly right.
- **Read `EXPLAIN`.** Every stage boundary is a shuffle. If you see more stages than you expected, you have shuffles you weren't planning for. `df.explain("formatted")` is the fastest debugging tool in Spark.
- **Spot skew in the Spark UI.** A stage where 199 tasks finish in 30 seconds and one runs for 20 minutes is a skew problem. Check Input Size in the task list; salt the hot key or rely on AQE skew split.
- **On Databricks, check for Photon fallbacks.** If a query is slower than expected and you assumed Photon, look for operators in the query plan that don't have the Photon prefix — UDFs and certain window functions are common culprits.

Five years away and the core model is exactly what I remembered. The optimizer, the execution engine, and the self-tuning layer have all gotten better. The shuffle is still the expensive thing. It's still your job to understand where your stage boundaries are.
