---
title: "Taking advantage of Windows Azure CDN and Dynamic Pages in ASP.NET - Caching content from hosted services"
date: 2011-03-11T07:59:34+0000
lastmod: 2011-03-11T07:59:34+0000
slug: "taking-advantage-of-windows-azure-cdn-and-dynamic-pages-in-asp-net-caching-content-from-hosted-services"
aliases:
  - /taking-advantage-of-windows-azure-cdn-and-dynamic-pages-in-asp-net-caching-content-from-hosted-services/
---

With the updates to Windows Azure CDN announced this week [[1](http://blogs.msdn.com/b/windowsazure/archive/2011/03/09/now-available-updated-windows-azure-sdk-and-windows-azure-management-portal.aspx)] I wanted to help illustrate the capability with a working sample that will serve up dynamic content from an ASP.NET site hosted in a WebRole.

First, to get a good overview of the capability you can read the [Overview of the Windows Azure CDN [2]](http://msdn.microsoft.com/en-us/library/ff919703.aspx) content on MSDN.

When you setup the ability to cache content from a hosted service, the requirement is to provide a path to your role’s DNS endpoint that ends in the path “/cdn”.  Additionally, you then map CDN to that service.

[![SNAGHTML520b6ac](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/3201.SNAGHTML520b6ac_thumb_153F3780.png "SNAGHTML520b6ac")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/0552.SNAGHTML520b6ac_4953D6D3.png)

What WAZ CDN does, is allow you to then map that through the CDN to your host.  The CDN will then make a request to your host on your client’s behalf.

The requirement is still that your client, and any Url’s that are to be serviced through the CDN and this capability have to use the CDN DNS name and not your host – no different than what CDN does for Blob storage.

The following 2 URL’s are samples of how the client needs to issue the requests.

**Windows Azure hosted service URL**: http: //myHostedService.cloudapp.net/cdn/music.aspx   - for regular “dynamic” content

**Windows Azure CDN URL**: http: //<identifier>.vo.msecnd.net/music.aspx   - for CDN “cachable” content.

The first URL path’s the request direct to your host into the Azure datacenter.  The 2nd URL paths the request through the CDN infrastructure, where CDN will make the determination to request the content on behalf of the client to the Azure datacenter and your host on the **/cdn** path.

The big advantage here is you can apply logic to your content creation.  What’s important is emitting the CDN friendly headers that allow CDN to request and re-request only when you designate based upon it’s rules of “staleness” as described in the overview page.

With IIS7.5 there is an underlying issue when the Managed Module “OutputCache” is enabled that in order to emit a good header for your content, you’ll need to remove, and in my sample, helps provide CDN friendly headers.  You get IIS 7.5 when running under OS Family “2” in your service configuration.

**NOTE: Re: IIS7.x and OutputCache handling of Cache-control header**

**[UPDATE]: 2011-3-14 – The missing piece was calling  Response.Cache.SetSlidingExpiration(true) as follows:**

```
Response.Cache.SetCacheability(HttpCacheability.Public);  
Response.Cache.SetMaxAge(TimeSpan.FromMinutes(5));  
Response.ContentType = "image/jpeg";  
Response.Cache.SetSlidingExpiration(true); 
```

By default, and when the OutputCache managed module is loaded, if you use the HttpResponse.CachePolicy to set the Http Headers for “max-age” when the HttpCacheability is “Public”, you will NOT get the “max-age” emitted as part of the “Cache-control:” header.  Instead, the OutputCache module will remove “max-age” and just emit “public”.  It works ok when Cacheability is set to “private”.

To work around the issue and ensure your code as follows emits the full max-age along with the public option, you need to remove as follows:

```
<system.webServer> 
  <modules runAllManagedModulesForAllRequests="true"> 
    <remove name="OutputCache"/> 
  </modules> 
</system.webServer> 
```
```
Response.Cache.SetCacheability(HttpCacheability.Public);
Response.Cache.SetMaxAge(TimeSpan.FromMinutes(rv));
```

**UPDATE: 2011-3-13 – CDN will also respect the s-maxage Cache-control value part of the header.  This can be set with the HttpResponse.Cache.SetProxyMaxAge method – similar to SetMaxAge.**

In the attached solution, the way I approached it was to have a VirtualApplication under the root site that has it’s own web.config  - this VirtualApplication is the /cdn of the site and when deployed to Azure as a Web Role will surface as a distinct IIS Application – along with a separate AppDomain.

The CDN Sample is a simple Web Forms site that the /default landing page contains 3 IFrames to host:

1. Content direct from the host @   <http://xxxx.cloudapp.net/cdn>

2. Content via the CDN @ <http://azxxx.vo.msecnd.net>

3. Simple list of recent requests – showing where the request came from.

[![CDNSampleTest](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/8463.CDNSampleTest_thumb_4BCCE2C4.png "CDNSampleTest")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/1134.CDNSampleTest_3415AB5E.png)

When you run the sample the first time you hit the page, both the Host and the CDN will cause 2 initial requests to hit the host.  You won’t see the first requests in the list because of timing – but if you refresh, you’ll see that the list will show that you have 2 requests initially.

1. sourced direct from the Browser to the HOST

2. sourced via the CDN

The picture above shows the call-outs of each of those requests – green rows showing requests coming direct to the HOST, yellow showing the CDN request.  The IP addresses of the green items are direct from the client, where the CDN is from the CDN data center.

As you refresh the page (hit Ctrl+F5 to force a full refresh and avoid “304 – not changed”) you’ll see that the request to the HOST get’s processed direct; but the request to the CDN endpoint is serviced direct from the CDN and doesn’t incur any additional request back to the HOST.

The following is the Headers from the CDN response

```
(Status-Line)    HTTP/1.1 200 OK
Age    13
Cache-Control    public, max-age=300
Connection    keep-alive
Content-Length    6212
Content-Type    image/jpeg; charset=utf-8
Date    Fri, 11 Mar 2011 20:47:14 GMT
Expires    Fri, 11 Mar 2011 20:52:01 GMT
Last-Modified    Fri, 11 Mar 2011 20:47:02 GMT
Server    Microsoft-IIS/7.5
X-AspNet-Version    4.0.30319
X-Powered-By    ASP.NET
```

The following are the Headers from the HOST response

```
(Status-Line)    HTTP/1.1 200 OK
Cache-Control    public, max-age=300
Content-Length    6189
Content-Type    image/jpeg; charset=utf-8
Date    Fri, 11 Mar 2011 20:47:15 GMT
Last-Modified    Fri, 11 Mar 2011 20:47:02 GMT
Server    Microsoft-IIS/7.5
X-AspNet-Version    4.0.30319
X-Powered-By    ASP.NET
```

You can see that with the CDN request, the countdown (age) starts for aging the content.

The full sample is located here:

**Update: 2011-3-13: Project has been updated a bit; more Compute Emulator friendly – 1 thing to note, since it’s using a VirtualApplication to debug the /cdn part, you have to attach manually to the w3wp.exe on your development machine.**

[CDNSampleSite.zip](http://cicoria.com/downloads/waz/CDNSampleSite.zip)

[1] [http://blogs.msdn.com/b/windowsazure/archive/2011/03/09/now-available-updated-windows-azure-sdk-and-windows-azure-management-portal.aspx](http://blogs.msdn.com/b/windowsazure/archive/2011/03/09/now-available-updated-windows-azure-sdk-and-windows-azure-management-portal.aspx "http://blogs.msdn.com/b/windowsazure/archive/2011/03/09/now-available-updated-windows-azure-sdk-and-windows-azure-management-portal.aspx")

[2] [http://msdn.microsoft.com/en-us/library/ff919703.aspx](http://msdn.microsoft.com/en-us/library/ff919703.aspx "http://msdn.microsoft.com/en-us/library/ff919703.aspx")
