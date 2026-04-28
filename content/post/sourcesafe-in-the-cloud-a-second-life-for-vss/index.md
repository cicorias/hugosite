---
title: "SourceSafe in the Cloud – a second life for VSS"
date: 2009-02-16T15:22:26+0000
lastmod: 2009-02-16T15:22:26+0000
slug: "sourcesafe-in-the-cloud-a-second-life-for-vss"
aliases:
  - /sourcesafe-in-the-cloud-a-second-life-for-vss/
---

> ***This post in no way endorses the use of Visual Source Safe, Mesh, or general supportability of this approach.  This is entirely at your own risk….***

Visual Source Safe (VSS) has been around for some time.  There have been a few 3rd parties, then Microsoft, that implemented some nice server side capabilities such as Source Off Site (SOS), VSSConnect, and now in VSS internet based access.

The issue with the server approach is that all of these requires some process to be running and hosting some part of VSS all the time.

What happened if you just used Mesh and shared the VSS DB folder (it’s just a folder) in Mesh and shared that way?

Well, I can say that for the past several weeks, I’ve been successfully working on a couple of different machines, doing check-in/out and it’s looking like no major issues so far.  Now, to be clear, this is just 1 user in a non-concurrent mode access the Mesh folder (when it’s local) from different machines.  Mesh gladly in the background syncs all the changes up to the “cloud” and when I’m online with the other machine those changes, and all status, etc. come down nicely…  I’ve even run analyze several times to just be sure..

[![image](https://msdnshared.blob.core.windows.net/media/TNBlogsFS/BlogFileStorage/blogs_msdn/scicoria/image_thumb_76511BD7.png "image")](https://msdnshared.blob.core.windows.net/media/TNBlogsFS/BlogFileStorage/blogs_msdn/scicoria/image_39106710.png)
