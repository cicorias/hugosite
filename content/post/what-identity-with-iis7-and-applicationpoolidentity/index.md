---
title: "What Identity with IIS7 and ApplicationPoolIdentity?"
date: 2009-12-24T05:13:50+0000
lastmod: 2009-12-24T05:13:50+0000
slug: "what-identity-with-iis7-and-applicationpoolidentity"
aliases:
  - /what-identity-with-iis7-and-applicationpoolidentity/
---

With IIS7, we have a little bit more isolation with AppPool Identities

For example, if you’re using the the DefaultAppPool, if you need to assign permissions to NTFS, SQL, etc., what you’d use instead is as follows:

IIS APPPOOL\DefaultAppPool

Where “DefaultAppPool” ends up being the name of your AppPool as shown in IIS Manager…

That is if you’ve set the identity to the “ApplicationPoolIdentity” instead of something else, such as Network Service, Local System, or something other…
