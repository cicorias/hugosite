---
title: "Fiddler and Direct Access"
date: 2013-12-16T06:10:13+0000
lastmod: 2013-12-16T06:10:13+0000
slug: "fiddler-and-direct-access"
aliases:
  - /fiddler-and-direct-access/
---

Fiddler puts some stuff in the registry that breaks Direct Access.

The following will cleanup after Fiddler runs

reg delete HKLM\SYSTEM\CurrentControlSet\Services\iphlpsvc\Parameters\ProxyMgr /va /f
