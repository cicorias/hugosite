---
title: "AD FS 2.0: Troubleshooting Event 364 and ThrowExceptionForHRInternal / NullReferenceException"
date: 2011-03-04T07:18:28+0000
lastmod: 2011-03-04T07:18:28+0000
slug: "ad-fs-2-0-troubleshooting-event-364-and-throwexceptionforhrinternal-nullreferenceexception"
aliases:
  - /ad-fs-2-0-troubleshooting-event-364-and-throwexceptionforhrinternal-nullreferenceexception/
---

Ran into a situation today where after AD FS federation server was installed, configured and up & running, “all of a sudden” it stopped working.

Turned out that another installer that affected the default web site, also seemingly affected the AppPools associated to all Applications under the Default Web site.

By changing the “Enable 32-bit Applications” either through IIS admin or via command line

**appcmd set apppool /apppool.name:MyAppPool /enable32BitAppOnWin64:false**

Back to normal…

[![SNAGHTML32c976](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/5611.SNAGHTML32c976_thumb_6AF0E491.png "SNAGHTML32c976")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/7774.SNAGHTML32c976_6D7A164F.png)
