---
title: "Azure Functions - Local Development Logging"
date: 2016-06-14T16:00:19+0000
lastmod: 2016-06-14T16:00:19+0000
slug: "azure-functions-local-development-logging"
feature_image: "/images/2016/06/AzureFunctions.png"
aliases:
  - /azure-functions-local-development-logging/
---

## Azure Functions

One nice feature of Azure Functions is that you can run your functions and develop locally. This is for C#, Node.JS, Python, Batch,etc. If you haven't seen this [Develop Azure Functions Locally](https://azure.microsoft.com/en-us/documentation/articles/functions-run-local/).

But, by default, you won't get any `log.write` messages for any debugging. And, it would be nice to not litter your app with `Console.WriteLine(...)` stuff. The fix is really simple, and just a setting on the `host.json`.

## Enabling Console Log

If you want to enable logging, just set a `tracing` field on the `host.json` in the root as follows:

```json
{
  "functions": ["TimerTrigger-CSharp"],
  "id": "5a709861cab44e68bfed5d2c2fe7fc0c",
  "tracing": {"consoleLevel": "verbose"}
}

```

These come from [`System.Diagnostics.TraceLevel`](https://msdn.microsoft.com/en-us/library/system.diagnostics.tracelevel)

| Value | Does |
| --- | --- |
| Error | error-handling messages |
| Info | info, warnings, errors |
| Off | nada |
| Verbose | ALL |
| Warning | warnings & errors |
