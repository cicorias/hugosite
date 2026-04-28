---
title: "SharePoint 2010 and Claims Based Awareness"
date: 2009-11-23T03:51:37+0000
lastmod: 2009-11-23T03:51:37+0000
slug: "sharepoint-2010-and-claims-based-awareness"
aliases:
  - /sharepoint-2010-and-claims-based-awareness/
---

The industry it moving towards identity standards, and with the recent release of Windows Identity Foundation (fka Geneva), and the beta of SharePoint 2010, it’s important to take a look at the direction of how identity is being normalized into a “service” within the SharePoint object model.

With SPS 2010, the SPUser object is now a claims identity.  Identity management has been normalized to a approach that internally uses an STS that takes all “provider” or external STS identities, then creates a SPUser claims identity.  This can have implications for LOB application design.  Even Windows identities are presented within SPS as a claims identity after banging against the SP STS for claims transformation.

Venky Veeraraghavan has a great video up on Channel 9 on how WIF was used to create this model within SharePoint and how we get 1) Identities “In”, 2) Identities “within”, and 3) Identities “out” – specifically, when talking to downstream back-end LOB applications, DB, Web Services, etc.  These are all things WIF and claims based identity is moving the industry.

This is certainly how we all should be looking at identity management and authentication scenarios.

     [![Get Microsoft Silverlight](http://go.microsoft.com/fwlink/?LinkId=108181)](http://go.microsoft.com/fwlink/?LinkID=124807)
