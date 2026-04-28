---
title: "Viewing the User Token from Visual Studio 2010 Debugger"
date: 2011-12-06T10:01:22+0000
lastmod: 2011-12-06T10:01:22+0000
slug: "viewing-the-user-token-from-visual-studio-2010-debugger"
aliases:
  - /viewing-the-user-token-from-visual-studio-2010-debugger/
---

When you’re debugging security related things, sometimes you need to take a look at the thread identities user token.

When you’re inside of Visual Studio 2010 – in the watch windows you enter ‘$user’  and you’ll get the same as when in windbg with !token –n

[![SNAGHTML6a3d635[6]](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/0842.SNAGHTML6a3d6356_thumb_7722AD63.png "SNAGHTML6a3d635[6]")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/2502.SNAGHTML6a3d6356_6D3DBBF8.png)
