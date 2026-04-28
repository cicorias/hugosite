---
title: "Differences when Running with OutputCache managed module under ASP.NET IIS7.x with Cache-control header"
date: 2011-03-14T13:39:36+0000
lastmod: 2011-03-14T13:39:36+0000
slug: "differences-when-running-with-outputcache-managed-module-under-asp-net-iis7-x-with-cache-control-header"
aliases:
  - /differences-when-running-with-outputcache-managed-module-under-asp-net-iis7-x-with-cache-control-header/
---

This post is to report some differences when using MVC or IHttpHandlers if you’re attempting to set the Cache-control : max-age or s-maxage value under IIS7.x using the HttpResponse.Cache methods.

**[UPDATE]: 2011-3-14 – The missing piece was calling  Response.Cache.SetSlidingExpiration(true) as follows:**

```
context.Response.Cache.SetCacheability(HttpCacheability.Public);
context.Response.Cache.SetMaxAge(TimeSpan.FromMinutes(5));
context.Response.ContentType = "image/jpeg";
context.Response.Cache.SetSlidingExpiration(true);
```

Under IIS7.x if you us one of the following 2 methods, you will only get a Cache-ability of “public”.

```
public ActionResult Image2()
{
    MemoryStream oStream = new MemoryStream();

    using (Bitmap obmp = ImageUtil.RenderImage("Respone.Cache.Setxx calls", 5, DateTime.Now))
    {
        obmp.Save(oStream, ImageFormat.Jpeg);
        oStream.Position = 0;
        Response.Cache.SetCacheability(HttpCacheability.Public);
        Response.Cache.SetMaxAge(TimeSpan.FromMinutes(5));
        return new FileStreamResult(oStream, "image/jpeg");
    }
}
```

Method 2 – which is just a plain old HttpHandler and really isn’t MVC3, but under the same MVC ASP.NET application, same result.

```
public class image : IHttpHandler
{

    public void ProcessRequest(HttpContext context)
    {
        using (var image = ImageUtil.RenderImage("called from IHttpHandler direct", 5, DateTime.Now))
        {
            context.Response.Cache.SetCacheability(HttpCacheability.Public);
            context.Response.Cache.SetMaxAge(TimeSpan.FromMinutes(5));
            context.Response.ContentType = "image/jpeg";
            image.Save(context.Response.OutputStream, ImageFormat.Jpeg);
        }            
    }

}
```

Using the following under MVC3 (I haven’t tried under earlier versions) will work by applying the OutputCacheAttribute to your Action:

```
[OutputCache(Location = OutputCacheLocation.Any, Duration = 300)]
public ActionResult Image1()
{
    MemoryStream oStream = new MemoryStream();

    using (Bitmap obmp = ImageUtil.RenderImage("called with OutputCacheAttribute", 5, DateTime.Now))
    {
        obmp.Save(oStream, ImageFormat.Jpeg);
        oStream.Position = 0;
        return new FileStreamResult(oStream, "image/jpeg");
    }
}
```

To remove the “OutputCache” module, you use the following in your web.config:

```
<system.webServer>
<validation validateIntegratedModeConfiguration="false"/>
<modules runAllManagedModulesForAllRequests="true">
  <!--<remove name="OutputCache"/>-->
</modules>
```
