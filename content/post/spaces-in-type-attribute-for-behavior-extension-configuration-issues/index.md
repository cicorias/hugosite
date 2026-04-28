---
title: "Spaces in type attribute for Behavior Extension Configuration Issues"
date: 2010-06-10T13:03:42+0000
lastmod: 2010-06-10T13:03:42+0000
slug: "spaces-in-type-attribute-for-behavior-extension-configuration-issues"
aliases:
  - /spaces-in-type-attribute-for-behavior-extension-configuration-issues/
---

If you’ve deployed your WCF Behavior Extension, and you get a Configuration Error, it might just be you’re lacking a space between your “Type” name and the “Assembly” name.

You'll get the following error message:

> **Verify that the extension is registered in the extension collection at system.serviceModel/extensions/behaviorExtensions**

[![image](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/6813.image_thumb_6C87A8DE.png "image")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/4341.image_10708039.png)

So, if you’ve entered as below without

```
<system.serviceModel>
  <extensions>
    <behaviorExtensions>
      <add name="appFabricE2E"
           type="Fabrikam.Services.AppFabricE2EBehaviorElement,Fabrikam.Services, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null"/>
    </behaviorExtensions>
  </extensions> 
```

The following will work – notice the additional space between the Type name and the Assembly name:

```
<system.serviceModel>
  <extensions>
    <behaviorExtensions>
      <add name="appFabricE2E"
           type="Fabrikam.Services.AppFabricE2EBehaviorElement, Fabrikam.Services, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null"/>
    </behaviorExtensions>
  </extensions> 
```
