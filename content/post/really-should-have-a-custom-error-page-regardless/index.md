---
title: "Really should have a custom error page regardless…"
date: 2010-09-19T12:39:34+0000
lastmod: 2010-09-19T12:39:34+0000
slug: "really-should-have-a-custom-error-page-regardless"
aliases:
  - /really-should-have-a-custom-error-page-regardless/
---

Throughout the blogosphere there’s been reports of an issue with ASP.NET that will bring a site to it’s knees – or so, it’s been overblown and reported as such.

Microsoft has released an advisory [here](http://www.microsoft.com/technet/security/advisory/2416728.mspx) that discusses the matter.

The workaround for now is something that any public website should’ve been doing anyway.  That is, implement a custom error handling page and suppress revealing detailed errors.  This is a normal part of a security audit and if you follow the STRIDE threat modeling you should have this as part of your checklist of things that you should ensure your following.

[1] [http://www.microsoft.com/technet/security/advisory/2416728.mspx](http://www.microsoft.com/technet/security/advisory/2416728.mspx "http://www.microsoft.com/technet/security/advisory/2416728.mspx")
