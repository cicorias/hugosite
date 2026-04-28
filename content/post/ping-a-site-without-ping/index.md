---
title: "Ping a site without Ping"
date: 2023-01-10T18:05:55+0000
lastmod: 2023-01-10T18:06:11+0000
slug: "ping-a-site-without-ping"
draft: true
aliases:
  - /ping-a-site-without-ping/
---

```
(echo >/dev/tcp/a210298d2musea2stvsu1.blob.core.windows.net/443) &>/dev/null && echo "open" || echo "closed"

(echo >/dev/tcp/a210298d2musea2stasu1.blob.core.windows.net/443) &>/dev/null && echo "open" || echo "closed"

eastus2-3.in.applicationinsights.azure.com/

(echo >/dev/tcp/eastus2-3.in.applicationinsights.azure.com/443) &>/dev/null && echo "open" || echo "closed"

eastus2.livediagnostics.monitor.azure.com/
(echo >/dev/tcp/eastus2.live
```
