---
title: "Getting the MVC3 assemblies as part of your Windows Azure deployment"
date: 2011-04-15T02:12:39+0000
lastmod: 2011-04-15T02:12:39+0000
slug: "getting-the-mvc3-assemblies-as-part-of-your-windows-azure-deployment"
aliases:
  - /getting-the-mvc3-assemblies-as-part-of-your-windows-azure-deployment/
---

There have been several techniques that have been posted on getting the MVC3 reference assemblies deployed as part of your Windows Azure Solution.

[http://blog.smarx.com/posts/asp-net-mvc-in-windows-azure](http://blog.smarx.com/posts/asp-net-mvc-in-windows-azure "http://blog.smarx.com/posts/asp-net-mvc-in-windows-azure")

This is something I learned today is in Visual Studio 2010 SP1.

If you open up the context menu for the project, you’ll see “Add Deployable Dependencies”.  When you select the parts you need it adds the \_bin\_deployableAssemblies to the project and a copy.  With Vs2010 SP1, the build targets have been updated to ensure these are emitted to your /bin path as required.

More on the targets approach here from Scott Hanselman [http://www.hanselman.com/blog/BINDeployingASPNETMVC3WithRazorToAWindowsServerWithoutMVCInstalled.aspx](http://www.hanselman.com/blog/BINDeployingASPNETMVC3WithRazorToAWindowsServerWithoutMVCInstalled.aspx "http://www.hanselman.com/blog/BINDeployingASPNETMVC3WithRazorToAWindowsServerWithoutMVCInstalled.aspx")

[![image](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/5488.image_thumb_3271DFE8.png "image")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/3247.image_0BD37968.png)
