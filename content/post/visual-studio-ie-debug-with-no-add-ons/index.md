---
title: "Visual Studio IE Debug with No Add-ons"
date: 2013-03-26T07:35:36+0000
lastmod: 2013-03-26T07:35:36+0000
slug: "visual-studio-ie-debug-with-no-add-ons"
aliases:
  - /visual-studio-ie-debug-with-no-add-ons/
---

Sometimes you need IE with no-adds.  For example, colleague of mine was crashing – won’t say which add-on caused it, but easily enough, add a choice to run IE with No-Addons in VS2012.

Just add an entry to your Browse with to

ProgramFiles(x86)\Internet Explorer\iexplore.exe

with the  -extoff parameter…

[![clip_image002](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/7737.clip_image002_thumb_5D01CE57.jpg "clip_image002")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/8814.clip_image002_4D423953.jpg)
