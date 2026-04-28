---
title: "Use an Action delegate to time a method…"
date: 2011-09-21T08:14:58+0000
lastmod: 2011-09-21T08:14:58+0000
slug: "use-an-action-delegate-to-time-a-method"
aliases:
  - /use-an-action-delegate-to-time-a-method/
---

I wanted an ability to be able to simply time methods and write to a log/trace sink and a very simple approach that I ended up using was to provide a method that takes an Action delegate which would be the method that is to be timed.

The following is what I came up with (this is my reminder…)

```
private static void TestMethod1()
{
    LoggingHelper.TimeThis(&quot;doing something&quot;, () =&gt;
    {
        Console.WriteLine(&quot;This is the Real Method Body&quot;);
        Thread.Sleep(100);
    });
}

```
