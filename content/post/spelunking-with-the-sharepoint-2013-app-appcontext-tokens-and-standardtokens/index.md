---
title: "Spelunking with the SharePoint 2013 App AppContext Tokens and StandardTokens"
date: 2013-04-28T10:30:13+0000
lastmod: 2013-04-28T10:30:13+0000
slug: "spelunking-with-the-sharepoint-2013-app-appcontext-tokens-and-standardtokens"
aliases:
  - /spelunking-with-the-sharepoint-2013-app-appcontext-tokens-and-standardtokens/
---

When writing SharePoint 2013 Provider hosted (autohosted too), SharePoint 2013 Apps provide an App context token, along with other information as part of the initial transition to the provider.  That token, and supporting “tokens” (part of the {standardtoken}) are useful to understand what you have and what you can do wit them.

In the interest of having a simple MVC4 based site, that provides simple Model binding of the SP 2013 App context transition, the sample app in the github repository provides some simple token information, along with a couple CSOM calls back to the SP 2013 environment.

This is purely for getting a better understanding of what’s part of the SP 2013 AppContext, the JwT token, and a simple way to manage this under an MVC4 ASP.NET app.

Here are a couple screen shots:

Source code located here: [https://github.com/cicorias/sharepointApps/tree/master/jwtSamples/jwtTokenDump](https://github.com/cicorias/sharepointApps/tree/master/jwtSamples/jwtTokenDump "https://github.com/cicorias/sharepointApps/tree/master/jwtSamples/jwtTokenDump")

Note that there is a hack in there that allows use of HttpSession for keeping the token around.  I didn’t want to much complexity with a cache provider.

[![SNAGHTML117c637e](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/5037.SNAGHTML117c637e_thumb_0ECE8150.png "SNAGHTML117c637e")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/7674.SNAGHTML117c637e_16C623B2.png)

[![SNAGHTML117c9326](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/0245.SNAGHTML117c9326_thumb_4634927E.png "SNAGHTML117c9326")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/5554.SNAGHTML117c9326_7C198798.png)

[![SNAGHTML117cbfc1](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/0257.SNAGHTML117cbfc1_thumb_19AB6298.png "SNAGHTML117cbfc1")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/2620.SNAGHTML117cbfc1_616CEB7F.png)

[![SNAGHTML117ce589](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/3858.SNAGHTML117ce589_thumb_5F4FECB6.png "SNAGHTML117ce589")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/3377.SNAGHTML117ce589_0B00B6B3.png)
