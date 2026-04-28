---
title: "Faking SPContext–for testing only…"
date: 2011-09-21T10:54:44+0000
lastmod: 2011-09-21T10:54:44+0000
slug: "faking-spcontextfor-testing-only"
aliases:
  - /faking-spcontextfor-testing-only/
---

Keith Dahlby has a good post on creating a fake SPContext.  Here’s the link and the code

NOTE: This is not production safe code – use at own risk…

[http://solutionizing.net/2009/02/16/faking-spcontext/](http://solutionizing.net/2009/02/16/faking-spcontext/ "http://solutionizing.net/2009/02/16/faking-spcontext/")

```
public static SPContext FakeSPContext(SPWeb contextWeb)
{
  // Ensure HttpContext.Current
  if (HttpContext.Current == null)
  {
    HttpRequest request = new HttpRequest("", web.Url, "");
    HttpContext.Current = new HttpContext(request,
      new HttpResponse(TextWriter.Null));
  }

// SPContext is based on SPControl.GetContextWeb(), which looks here  

if(HttpContext.Current.Items["HttpHandlerSPWeb"] == null)  

HttpContext.Current.Items["HttpHandlerSPWeb"] = web;

return SPContext.Current;  

}

```
