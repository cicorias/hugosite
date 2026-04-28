---
title: "Thanks Jukka – MOSS 2007 SP2 Upgrade Failure – Solution!"
date: 2009-04-30T11:49:29+0000
lastmod: 2009-04-30T11:49:29+0000
slug: "thanks-jukka-moss-2007-sp2-upgrade-failure-solution"
aliases:
  - /thanks-jukka-moss-2007-sp2-upgrade-failure-solution/
---

During an upgrade, the psconfig command fails with

> Failed to upgrade SharePoint Products and Technologies.
>
> An exception of type Microsoft.SharePoint.Upgrade.SPUpgradeException was thrown.

Quick live search and I find on Jukka’s blog the answer:

[http://blogs.msdn.com/jukka/archive/2009/04/30/error-during-sharepoint-sp2-install.aspx](http://blogs.msdn.com/jukka/archive/2009/04/30/error-during-sharepoint-sp2-install.aspx "http://blogs.msdn.com/jukka/archive/2009/04/30/error-during-sharepoint-sp2-install.aspx")

Specifically, a feature was not installed, and quickly installing using the stsadm command Jukku provides, it then works…
