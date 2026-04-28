---
title: "SharePoint 2013 Farm in Less than an Hour–New Azure Portal and Azure Templates"
date: 2014-07-14T02:31:56+0000
lastmod: 2014-07-14T02:31:56+0000
slug: "sharepoint-2013-farm-in-less-than-an-hournew-azure-portal-and-azure-templates"
aliases:
  - /sharepoint-2013-farm-in-less-than-an-hournew-azure-portal-and-azure-templates/
---

Soon, you’ll be able to author your own templates, but as of today, you can provision an 3 Machine SharePoint 2013 Farm – have it running in less than 1 hour with just a few clicks.

**For details take a look here:**

**SharePoint Server Farm** at <http://azure.microsoft.com/en-us/documentation/articles/virtual-machines-sharepoint-farm-azure-preview/>   
**SharePoint Server Farm Configuration Details** at <http://azure.microsoft.com/en-us/documentation/articles/virtual-machines-sharepoint-farm-config-azure-preview/>

Now, for some fun…

First, navigate to the new portal at <http://portal.azure.com>

Once there, choose “New”.

There you’ll get the new experience for Template based provisioning.  Click on “Show Everything” to see the full Gallery of Microsoft and non-Microsoft templates.

[![image](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/7384.image_thumb_1AC6E92F.png "image")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/0028.image_248C50A7.png)

After choosing a SP Farm, you set a few global settings, or you can choose to modify the template choices, like Machine size (A5 vs. A4, etc.).  Even account names, etc.

I chose the easy route.

[![image](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/6663.image_thumb_05D7F76D.png "image")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/6758.image_2EE005B8.png)

After a bit, and if you chose to “Add to Start Board” you’ll see your farm provisioning notifications, and eventually your finished Farm Tile.

[![image](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/8741.image_thumb_07A84D34.png "image")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/6278.image_4535AAFD.png)

[![image](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/4087.image_thumb_5714CF7B.png "image")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/3173.image_5BF78337.png)

The following shows the individual VM status (I shut mine down to save some $).  But easy enough to restart when I need it.

Remember, that while it’s COLD you only pay for the actual non-zero’s bits in the Page Blobs for the VHD storage. So, a 60 GB disk really only may be using 5 GB etc.

[![image](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/8540.image_thumb_4DBB9AF8.png "image")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/7635.image_2B64057F.png)
