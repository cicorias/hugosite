---
title: "Scala Using with OpenTelemetry Span to automatically end the Span Block"
date: 2022-08-03T18:24:46+0000
lastmod: 2022-08-03T18:30:54+0000
slug: "scala-using-with-opentelemetry-span-to-automatically-end-the-span-block"
tags: ["opentelemetry", "scala", "instrumentation", "observability"]
feature_image: "https://www.cicoria.com/content/images/2022/08/Untitled-1.png"
aliases:
  - /scala-using-with-opentelemetry-span-to-automatically-end-the-span-block/
---

Past couple of years, I've been spending quite a bit of time with [OpenTelemetry](https://opentelemetry.io/) (OTEL). As always, always looking for shortcuts in code.

One of the things that is always just annoying is that [`span.end(`](https://opentelemetry.io/docs/instrumentation/java/manual/#create-spans)`)` just doesn't mesh well with "close" or "release" etc. all the time. So, things like try-resource and Scala's Using won't understand it without some help.

So, this little bit of code using implicit support in Scala (I'm still on Scala 2.13 much) will help that along.

First need to define the implicit type of class for Span to make it `Releaseable`

```scala
import scala.util.Using
import io.opentelemetry.api.trace.Span
  
implicit val releaseable: Using.Releasable[Span] = s => {
    s.end()
}
```

>Note: Obviously, or perhaps not so obvious, is that can be put in a separate class and imported.

Then, just wrap it in a using and release gets called and at the end of the block whatever you define in the wrap above – for Span we need the `end()` called.

```scala
Using{Span.current()}(s => {
	s.addEvent("doing some span stuff")
})
```
