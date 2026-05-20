---
title: "Building a PostgreSQL LLM Extension with Rust Background Workers"
date: 2026-05-20T12:17:00-04:00
slug: "building-a-postgresql-llm-extension-with-rust-background-workers"
draft: false
tags: ["postgresql", "rust", "llm", "pgrx", "extensions"]
summary: "A walkthrough of pg_llm_bgw, a PostgreSQL 18 extension written in Rust with pgrx that exposes a SQL-callable llm_ask() function, proxying prompts to OpenAI, Azure OpenAI, or Anthropic through a static background worker and shared memory."
aliases:
  - /building-a-postgresql-llm-extension-with-rust-background-workers/
feature_image: "/images/2026/05/building-a-postgresql-llm-extension-with-rust-background-wor-hero.jpg"
---

## Overview

[pg_llm_bgw](https://github.com/cicorias/postgres-llm-extension-bw.git) is a PostgreSQL 18 extension written in Rust using [pgrx](https://github.com/pgcentralfoundation/pgrx) 0.18. It registers a **static background worker** at postmaster start and exposes a SQL-callable function `llm_ask(prompt text) RETURNS text` that proxies prompts to an LLM responses API through a shared-memory slot guarded by an LWLock.

```text
┌────────────┐  prompt   ┌──────────────────┐  HTTP   ┌─────────┐
│  SQL       │ ────────> │ shared memory    │ ──────> │   LLM   │
│  backend   │           │ (LlmShared +     │         │ (block- │
│ llm_ask()  │ <──────── │  PgLwLock)       │ <────── │  ing)   │
└────────────┘  response └──────────────────┘         └─────────┘
                               ▲ latch wake
                               │
                        ┌──────┴───────┐
                        │ bgw_main()   │   static BGW, always running
                        └──────────────┘
```

The design keeps the HTTP call off the SQL backend process entirely. The background worker handles the network I/O, and the calling backend simply waits on the shared-memory response slot.

## Why a Background Worker?

PostgreSQL backends (the processes serving your SQL sessions) should not make long-running blocking network calls. A background worker solves this by:

1. Running as a separate OS process managed by the postmaster
2. Surviving individual backend disconnects
3. Centralizing credentials and connection pooling in one place
4. Allowing future enhancements like request queuing and batching

## Architecture

The extension is structured into four Rust modules:

| Module     | Responsibility |
|------------|---------------|
| `lib.rs`   | `_PG_init` (registers shared memory + BGW), `llm_ask()` and `llm_provider()` SQL functions |
| `bgw.rs`   | Background worker main loop: polls shared memory, dispatches to `call_llm()` |
| `shmem.rs` | `LlmShared` struct with `LlmRequest` / `LlmResponse` fixed-size buffers + `PgLwLock` |
| `llm.rs`   | Multi-provider blocking HTTP client (OpenAI, Azure OpenAI, Anthropic) |

### Shared Memory Layout

Communication between the SQL backend and the BGW uses a single shared-memory slot:

```rust
pub const PROMPT_CAPACITY: usize = 4096;
pub const RESPONSE_CAPACITY: usize = 16384;

#[derive(Copy, Clone, Default)]
#[repr(C)]
pub struct LlmShared {
    pub request: LlmRequest,
    pub response: LlmResponse,
}

pub static LLM_SHARED: PgLwLock<LlmShared> =
    unsafe { PgLwLock::new(c"pg_llm_bgw_shared") };
```

The `PgLwLock` ensures safe concurrent access. The SQL backend writes the prompt, sets `ready = true`, then polls for `done = true`. The BGW detects the ready flag, makes the HTTP call, writes the response back, and sets `done`.

### Background Worker Registration

In `_PG_init`, the extension registers itself as a static BGW:

```rust
BackgroundWorkerBuilder::new("pg_llm_bgw")
    .set_type("pg_llm_bgw")
    .set_library("pg_llm_bgw")
    .set_function("bgw_main")
    .set_start_time(BgWorkerStartTime::RecoveryFinished)
    .set_restart_time(Some(Duration::from_secs(10)))
    .enable_spi_access()
    .load();
```

The BGW starts after recovery finishes and auto-restarts after 10 seconds if it crashes.

### Multi-Provider LLM Client

The `llm.rs` module follows LangChain-style environment variable conventions for provider resolution:

1. If `LLM_PROVIDER` is explicitly set, it wins
2. Otherwise auto-detect by env-var presence: `AZURE_OPENAI_ENDPOINT` > `ANTHROPIC_API_KEY` > `OPENAI_API_KEY`
3. Fallback: OpenAI (fails fast with a clear error if no key is configured)

You can check the resolved provider from SQL:

```sql
SELECT llm_provider();  -- → 'openai' | 'azure_openai' | 'anthropic'
```

## Prerequisites

| Tool | Purpose |
|------|---------|
| [mise](https://mise.jdx.dev) | Tool version manager (provides PG 18.4) |
| Rust 1.80+ | Extension language |
| libclang | Required by pgrx bindgen |
| cargo-pgrx 0.18.0 | PostgreSQL extension build tooling |

## Getting Started

```bash
# Install tools
mise install

# One-time pgrx registration
mise run pgrx-init

# Full bootstrap: build → install → preload → restart → create extension
mise run bootstrap
```

After bootstrap, the cluster runs on port **28818**, the BGW is alive, and you can call:

```sql
SELECT llm_ask('Explain PostgreSQL background workers in one sentence');
```

## Configuring a Provider

Export the relevant environment variables, then restart the cluster:

```bash
# OpenAI
export OPENAI_API_KEY=sk-...
mise run pg-restart

# Azure OpenAI
export AZURE_OPENAI_ENDPOINT=https://my-resource.openai.azure.com
export AZURE_OPENAI_DEPLOYMENT=gpt-4o
export AZURE_OPENAI_API_KEY=...
mise run pg-restart

# Anthropic
export ANTHROPIC_API_KEY=sk-ant-...
mise run pg-restart
```

The BGW inherits the postmaster's environment, so env vars must be set before starting the cluster.

## pgrx 0.18 Lessons Learned

A few gotchas encountered while building this extension with pgrx 0.18:

- `pg_module_magic!()` only accepts the no-arg form (despite older docs)
- Use `check_for_interrupts!()` macro, not `pg_sys::CHECK_FOR_INTERRUPTS`
- BGW main signature requires `#[pg_guard] #[unsafe(no_mangle)] pub extern "C-unwind"`
- Shared memory registration uses `PgLwLock::new(c"name")` with a C-string literal
- `BackgroundWorkerBuilder` chains to `.load()` directly (no separate register step)

## What's Next

The current implementation is a working scaffold. Planned improvements include:

1. Replace the 1ms spin-poll in `llm_ask` with a proper `WaitLatch`/`SetLatch` round-trip
2. Expand the single request slot into a ring buffer for concurrent sessions
3. Promote env-var config to PostgreSQL GUCs (`ALTER SYSTEM SET`)
4. Full Azure AAD credential support with token auto-refresh
5. Add an `llm_request` table + trigger for async fire-and-poll usage
6. `pgvector`-compatible embedding functions through the same BGW/HTTP pattern

## Source

The full source is available at [github.com/cicorias/postgres-llm-extension-bw](https://github.com/cicorias/postgres-llm-extension-bw).
