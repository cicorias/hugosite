---
title: "SharePoint 2007 and InfoPath 2010 Client – current install issues…"
date: 2009-11-17T05:24:20+0000
lastmod: 2009-11-17T05:24:20+0000
slug: "sharepoint-2007-and-infopath-2010-client-current-install-issues"
aliases:
  - /sharepoint-2007-and-infopath-2010-client-current-install-issues/
---

Ok, I’ve been bitten twice in the past week on this.  If you have InfoPath 2010 Beta installed and you’ve also got SharePoint 2007 running, at least with the latest SP2 and October CU, you run into an issue that surfaces in the logs as follows

> One or more types failed to load. Please refer to the upgrade log for more details

When you pull that log apart, you’ll see that it’s attempting to load a few types such as Microsoft.Office.InfoPath.Server.DocumentLifetime.XmlFormHost' from assembly 'Microsoft.Office.InfoPath.Server.

Which, they fail – removing InfoPath from the install works.
