---
title: "Additional Mime Types in Visual Studio 2010 Development Web Server"
date: 2011-10-06T11:40:13+0000
lastmod: 2011-10-06T11:40:13+0000
slug: "additional-mime-types-in-visual-studio-2010-development-web-server"
aliases:
  - /additional-mime-types-in-visual-studio-2010-development-web-server/
---

While the development server in Visual Studio 2010 is great for most work, it does have 1 shortcoming in that if you start adding content types that are not part of the base set of known Mime types built in, you won’t affect the proper header response that is emitted to the client/browser.

For example MP4 files, out of the box the development web server emits application/octet-stream or something like that.  What we really need is video/mp4.

Now, with IIS Express, you can easily switch over to use that and just add the correct mapping to the section of the web.config when you’re running in integrated mode.  Such as follows:

```
<system.webServer>
  <modules runAllManagedModulesForAllRequests="true" />
  <staticContent>
    <mimeMap fileExtension=".mp4" mimeType="video/mp4" />
    <mimeMap fileExtension=".m4v" mimeType="video/m4v" />
  </staticContent>
</system.webServer>
```

However, with the Visual Studio 2010 built in Web Development server, you can’t affect the mime type support through configuration.

For this a simple NuGet package is available that provides a simple HttpModule to affect the ContentType on the response headers.  it reads the Web.config for the site and will honor the section above – this all happens only when NOT running in Integrated Pipeline mode.

[![image](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/4075.image_thumb_3EEB7533.png "image")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/0842.image_43CE28EF.png)

[![SNAGHTML6f59550](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/4087.SNAGHTML6f59550_thumb_68130D71.png "SNAGHTML6f59550")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/1348.SNAGHTML6f59550_3040C94E.png)

Sample Solution and Source here: [SampleMimeHelper.zip](http://cicoria.com/downloads/SampleMimeHelper.zip)

The HttpModule makes use of dynamically loading via the [PreApplicationStartMethod](http://msdn.microsoft.com/en-us/library/system.web.preapplicationstartmethodattribute.aspx) and the [DynamicModuleHelper](http://msdn.microsoft.com/en-us/library/microsoft.web.infrastructure.dynamicmodulehelper.dynamicmoduleutility.registermodule.aspx) utility method that is part of the Microsoft.Web.Infrastructure namespace.

```
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Diagnostics;
using System.Configuration;
using System.Web.Configuration;
using System.Xml.Linq;
using Microsoft.Web.Infrastructure.DynamicModuleHelper;

[assembly: PreApplicationStartMethod(typeof(MimeHelper), "Start")]

/// <summary>
/// Summary description for MimeHelper
/// </summary>
public class MimeHelper : IHttpModule
{
    static Dictionary<string, string> s_mimeMappings;
    static object s_lockObject = new object();

    public static void Start()
    {
        if ( ! HttpRuntime.UsingIntegratedPipeline)
            DynamicModuleUtility.RegisterModule(typeof(MimeHelper));
    }

    static string GetMimeType(HttpContext context)
    {
        var ext = VirtualPathUtility.GetExtension(context.Request.Url.ToString());
        if (string.IsNullOrEmpty(ext)) return null;

        CreateMapping(context.ApplicationInstance);

        string mimeType = null;
        s_mimeMappings.TryGetValue(ext, out mimeType);

        return mimeType;

    }

    static void CreateMapping(HttpApplication app)
    {
        if (null == s_mimeMappings)
        {
            lock (s_lockObject)
            {
                if (null == s_mimeMappings)
                {
                    string path = app.Server.MapPath("~/web.config");
                    XDocument doc = XDocument.Load(path);

                    var s = from v in doc.Descendants("system.webServer").Descendants("staticContent").Descendants("mimeMap")
                            select new { mimeType = v.Attribute("mimeType").Value, fileExt = v.Attribute("fileExtension").Value };

                    s_mimeMappings = new Dictionary<string, string>();
                    foreach (var item in s)
                    {
                        s_mimeMappings.Add(item.fileExt.ToString(), item.mimeType.ToString());
                    }
                }
            }
        }
    }

    public void Dispose() { }

    public void Init(HttpApplication context)
    {
        context.EndRequest += new EventHandler(context_EndRequest);
    }

    void context_EndRequest(object sender, EventArgs e)
    {
        try
        {
            HttpApplication app = sender as HttpApplication;
            string mimeType = GetMimeType(app.Context);

            if (null == mimeType) return;

            app.Context.Response.ContentType = mimeType;
        }
        catch (Exception ex)
        {
            Debug.WriteLine(ex.Message);
        }
    }
}
```
