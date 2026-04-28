---
title: "BizTalk 2009 Orchestration Fails to Find References on External Assemblies"
date: 2010-06-06T12:10:12+0000
lastmod: 2010-06-06T12:10:12+0000
slug: "biztalk-2009-orchestration-fails-to-find-references-on-external-assemblies"
aliases:
  - /biztalk-2009-orchestration-fails-to-find-references-on-external-assemblies/
---

If you’re developing BizTalk 2009 solutions (Orchestrations) and you’ve split your schemas out into alternative assemblies (projects) – sometimes you’ll get odd not found issues with some (if not all) of the types in those referenced assemblies.  You can try everything – recompile, de-gac, re-gac, – doesn’t matter.

Well there’s a hotfix for this:

[http://support.microsoft.com/kb/977428/en-us](http://support.microsoft.com/kb/977428/en-us "http://support.microsoft.com/kb/977428/en-us")

FIX: You experience various problems when you develop a BizTalk project that references another BizTalk project in Visual Studio on a computer that is running BizTalk Server 2009
