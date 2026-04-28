---
title: "Hosted Service as a Windows Azure CDN Origin Tips"
date: 2011-07-10T06:26:34+0000
lastmod: 2011-07-10T06:26:34+0000
slug: "hosted-service-as-a-windows-azure-cdn-origin-tips"
aliases:
  - /hosted-service-as-a-windows-azure-cdn-origin-tips/
---

The Windows Azure Content Delivery Network (CDN) helps improve the solution experience by putting content closer to the end-user, enhances availability, geo-distribution, scalability, lower latency delivery, and performance. If that’s the goal we want to be sure that when we instantiate the source of this content at the origin it’s as CDN friendly as we need.

In Windows Azure, when you’re running under IIS7.x /ASP.NET you have to be aware of the inherent behavior associated with Output Caching as it is part of the standard deployment of IIS7.x.

Some of that inherent behavior affects how cache-friendly your content (Http Response) will be as the CDN directly consumes your Hosted Service endpoint ( http[s]://yourservice:80|443/cdn ) on behalf of your users.

If you don’t understand how your solution emits these HTTP headers, you will end up with NO caching – defeating the purpose of the CDN (in fact making performance worse) and additional costs incurred.

The areas we’ll briefly take a look at here are:

- Working with the ASP.NET OutputCache module for CDN Friendly HTTP Headers
- Vary:\* Headers
- Compressed content with the CDN
- Use of IIS Virtual Application / Directories under Windows Azure
- Provide your own OutputCache module implementation

## Working with the ASP.NET OutputCache Module

### Default behavior

The following code is an example of what developers generally provided with anticipation that the HTTP headers, specifically the Cache-control header will be emitted with a CDN friendly HTTP header – or any cache for that matter.

```
using (var image = ImageUtil.RenderImage(…))
 {
     context.Response.Cache.SetMaxAge(TimeSpan.FromMinutes(Constants.MA));
     context.Response.Cache.SetCacheability(HttpCacheability.Public);
     context.Response.ContentType = "image/jpeg";
     image.Save(context.Response.OutputStream, ImageFormat.Jpeg);
     context.Response.OutputStream.Flush();
 }
```

Under ASP.NET 3.5/4.x, this will result in the following

[![image](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/4744.image_thumb_49E648BF.png "image")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/3000.image_1D3D8EE6.png)

```
---request begin---
GET /image/0.jpg HTTP/1.0
User-Agent: Wget/1.11.4
Accept: */*
Host: az30993.vo.msecnd.net
Connection: Keep-Alive
---response begin---
HTTP/1.0 200 OK
Cache-Control: public
Content-Type: image/jpeg
Server: Microsoft-IIS/7.5
X-AspNet-Version: 4.0.30319
X-Powered-By: ASP.NET
Date: Fri, 08 Jul 2011 11:26:01 GMT
Content-Length: 6976
X-Cache: MISS from cds168.ewr9.msecn.net
Connection: keep-alive
```

With that set of headers, you will encounter a cache MISS on every request – with a read-through to the Hosted Service origin. You might not notice the impact right away as it can get picked up by the OutputCache module – but you’ve defeated the purpose of the CDN – and made the request performance worse.

The sample solution with this post provides a set of test scenarios for manipulating the HttpResponse under a standard IHttpHandler and under MVC3. If you take a look at the code you’ll see that 3 things are done to help diagnose the situation.

1. Request Logger – this is a simple request logger that captures requests for the purposes of providing a simple view against the incoming requests (could have used IIS logs, but this is a simple way to get the requests I’m interested in and display them)
2. Kernel caching is disabled via the web.config – with this enabled requests won’t make it into your ASP.NET pipeline when it’s a cache hit – giving you a false positive on understanding if and when CDN requests are “leaking” through and not being cached at the CDN
3. OOB OutputCache module is removed, then re-added – this ensures it’s lower in the module list at request time allowing the Request Logger to be higher up in the call chain so I’m sure to capture the inbound requests – if they’re cached or not in the OutputCache module

##### Set SlidingExpiration on Response

The easiest fix is to ensure you set SlidingExpiration to true on the response. This will ensure that the Cache-control header will contain your desired “public, max-age=xxxx”

```
public void ProcessRequest(HttpContext context)
{
    using (var image = ImageUtil.RenderImage(…)
    {
       context.Response.Cache.SetCacheability(HttpCacheability.Public);
       context.Response.Cache.SetMaxAge(TimeSpan.FromMinutes(Config.MaxAge));
       context.Response.ContentType = "image/jpeg";
       context.Response.Cache.SetSlidingExpiration(true);
       image.Save(context.Response.OutputStream, ImageFormat.Jpeg);
    }
}
```

##### Set an explicit Expires on the Response

```
public void ProcessRequest(HttpContext context)
{
    using (var image = ImageUtil.RenderImage(…)
    {
      context.Response.Cache.SetCacheability(HttpCacheability.Public);
      context.Response.Cache.SetExpires(DateTime.Now.AddMinutes(Config.MA));
      context.Response.ContentType = "image/jpeg";
      image.Save(context.Response.OutputStream, ImageFormat.Jpeg);
      context.Response.OutputStream.Flush();
    }
}
```

##### Use Downstream as the location when using the MVC OutputCache Attribute

```
[OutputCache(CacheProfile = "CacheDownstream")]
public ActionResult Image3()
{
    MemoryStream oStream = new MemoryStream();
    using (Bitmap obmp = ImageUtil.RenderImage(…)
    {
       obmp.Save(oStream, ImageFormat.Jpeg);
       oStream.Position = 0;
       return new FileStreamResult(oStream, "image/jpeg");
    }
}

//web.config
 <caching>
      <outputCacheSettings>
        <outputCacheProfiles>
          <add name="CacheDownstream" 
               location="Downstream" 
               duration="1000" 
               enabled="true"/>
        </outputCacheProfiles>
      </outputCacheSettings>
```

##### Append a query string

Providing a query string on the request affects the Cache-control header. Even if you add just a “?” after the URL path, the OutputCache module will then emit your intended max-age.

##### Disable OutputCache module – via config

You can do this by removing it from the ASP.NET pipeline altogether, or remove it in the sub-path where /cnd is located (or Virtual Application – see section later). This disables all Output caching for all requests.

##### Disable OutputCache module – via code – per request

You can also choose to bypass the OutputCache by affecting the Response with the following code

```
public void ProcessRequest(HttpContext context)
{
    using (var image = ImageUtil.RenderImage(…)
    {
       context.Response.Cache.SetCacheability(HttpCacheability.Public);
       context.Response.Cache.SetMaxAge(TimeSpan.FromMinutes(Config.MA));
       context.Response.Cache.SetNoServerCaching();
       context.Response.ContentType = "image/jpeg";
       image.Save(context.Response.OutputStream, ImageFormat.Jpeg);
       context.Response.OutputStream.Flush();
    }
}
```

##### Implement your own OutputCache module

You can take a look at the links in the section on implementing your own OutputCache module to get an idea on the implementation effort, but the reasoning why you would want to is varied – which I’ll cover a couple of reasons in that section.

### Vary:\* Headers and Caching

Ensure you’re not emitting Vary:\* by headers at all if you want to take advantage of caching – either with the Windows Azure CDN or not – as the specification indicates responses with Vary:\* should not be cached and only handled at the origin.

From RFC2616: "A Vary header field-value of "\*" always fails to match and subsequent requests on that resource can only be properly interpreted by the origin server."

### Compressed content with the CDN

One of the reasons you would want to move your origin from Windows Azure Storage to a Hosted Service is to take advantage of compression. As part of IIS7.x, you can ensure that static and dynamic compression is enabled for your content – this will then cascade through to the Windows Azure CDN and provide an overall better experience for your end users.

### Use of IIS Virtual Application / Directories under Windows Azure

Today, using Hosted Service as an origin to Windows Azure CDN requires a production deployment of your service listening at the path http[s]://yourserviceDnsName:80|443/cdn. Currently we do not support Hosted Services as origins in staging.

All that is required is that your service provide responses under the /cdn path. You can achieve this with a WebRole that has a directory (path) under your main site.

What happens if you need (or desire) to isolate that path (/cdn)? Under Windows Azure, you can take advantage of IIS Virtual Applications / Directories under your main WebRole.

The following Service Definition illustrates the approach by taking advantage of the Full IIS model and the VirtualApplication element. The key to the approach here for your solution in the development fabric is to ensure the physical directory is relative to the MainWeb path.

```
<ServiceDefinition name="TR13VirtualApp" xmlns="http://schemas.microsoft.com/ServiceHosting/2008/10/ServiceDefinition">
  <WebRole name="MainWeb" vmsize="ExtraSmall">
    <Sites>
      <Site name="Web">
        <VirtualApplication name="cdn" physicalDirectory="../MainWebCdn" />
        <Bindings>
          <Binding name="Endpoint1" endpointName="Endpoint1" />
        </Bindings>
      </Site>
    </Sites>
    … 
```

This results in a deployment up on Windows Azure as the following – with a single site, and 2 application pools:

[![image](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/3286.image_thumb_7954B78B.png "image")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/5153.image_08D7C95B.png)

Simple VS2010 Solution is also provided at the end of the post and the following links provide further detail:

#### Creating Virtual Applications / Directories

The Windows Azure Training kit contains a sample walkthrough that demonstrates the approach.

<http://msdn.microsoft.com/en-us/wazplatformtrainingcourse_advancedwebandworkerrolesvs2010lab_topic2.aspx>

Additionally, Wade Wegner goes into a bit of detail as well.

<http://www.wadewegner.com/2011/02/running-multiple-websites-in-a-windows-azure-web-role/>

### Why provide your own OutputCache module implementation?

So, what would make you want to write your own OutputCache module implementation? Recall that the Service model when you have many instances in your Windows Azure Role may result in different host instances servicing requests.

[![image](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/1856.image_thumb_2F762FDB.png "image")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/5165.image_182B2B6A.png)

#### If that content is VERY expensive to produce….

You now have N (# of instances) producing possibly exact or similar replicas of your content. Not exactly a desirable effect if your transaction costs are high (maybe you’re reaching out to external services, or on premise mainframes, etc.)

#### Take advantage of Windows Azure AppFabric Caching

Either replacing the OutputCache module with your own implementation, or leveraging your own request model (that will still work with or bypass the OutputCache module) you can instantiate a single copy of that content in AppFabric Caching – thereby reducing the overall cost associated with repetitive content creation. Whatever your choice, ensure to factor in operational costs of AppFabric to see if it meets your economic model.

[![image](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/4263.image_thumb_2C80CB28.png "image")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/8473.image_27125A84.png)

#### Implement your own OutputCache

The following links provide some guidance on replacing OutputCache module – which can be done at the /cdn path level if required.

##### Custom OutputCacheProvider

The following is a sample implementation of a custom OutputCache module under NetFx 4.0.

<http://weblogs.asp.net/gunnarpeipman/archive/2009/11/19/asp-net-4-0-writing-custom-output-cache-providers.aspx>

##### ASP.NET 4.0 Caching Overview

Check out the following link on ASP.NET 4.0 caching in general to get an idea of OutputCache module.

<http://msdn.microsoft.com/en-us/library/ms178597.aspx>

### Solution Files

[CDN Test Solution](http://cicoria.com/downloads/waz/CdnTest.zip)

[Virtual App Sample](http://cicoria.com/downloads/waz/VirtualApp.zip)
