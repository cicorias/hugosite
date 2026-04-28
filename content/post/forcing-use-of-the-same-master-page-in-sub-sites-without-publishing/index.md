---
title: "Forcing use of the same Master Page in sub-sites without Publishing"
date: 2011-06-02T05:19:59+0000
lastmod: 2011-06-02T05:19:59+0000
slug: "forcing-use-of-the-same-master-page-in-sub-sites-without-publishing"
aliases:
  - /forcing-use-of-the-same-master-page-in-sub-sites-without-publishing/
---

This seems to come up a few times.  The following sample script in PS applies a common master page across all SPWebs in a site collection.

```
$site = Get-SPSite http://fba.contosotest.com/dv1
$site | Get-SPWeb -limit all | ForEach-Object { $_.MasterUrl = "/dv1/_catalogs/masterpage/custom_v4.master";$_.Update() }
$site.Dispose()
```

Thanks to Phil Childs - [http://get-spscripts.com/2010/09/changing-master-page-on-sharepoint.html](http://get-spscripts.com/2010/09/changing-master-page-on-sharepoint.html "http://get-spscripts.com/2010/09/changing-master-page-on-sharepoint.html")
