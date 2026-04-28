---
title: "Using S2S for On-Premises Access with Forms Based Access (FBA) in SharePoint 2013"
date: 2013-05-03T02:16:14+0000
lastmod: 2013-05-03T02:16:14+0000
slug: "using-s2s-for-on-premises-access-with-forms-based-access-fba-in-sharepoint-2013"
aliases:
  - /using-s2s-for-on-premises-access-with-forms-based-access-fba-in-sharepoint-2013/
---

The below diagram represents the flow and interaction when a user, from an external application, makes a OAuth protected call to a SharePoint site. This approach allows for delegated authentication, and since the SharePoint and the external application “can” (they don’t have to) share the Identity Store, we maintain the integrity of the “only 1 identity”.

Note, you can run this without sharing that identity store. In fact, since this is a S2S “High-Trust” approach, all SharePoint cares about is that the external application is “registered” along with a public certificate that will coincide with the signed OAuth token that will appear on the CSOM requests into SharePoint. This certificate, along with the application is registered in SharePoint with the Token Issuer (use the New-SPTrustedSecurityTokenIssuer – and make sure you look up the “-IsTrustBroker” flag).

[![image](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/8547.image_thumb_1352C462.png "image")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/4834.image_34463709.png)
