---
title: "App_offline.htm and SharePoint and wholly contained images…"
date: 2010-06-08T10:24:51+0000
lastmod: 2010-06-08T10:24:51+0000
slug: "app_offline-htm-and-sharepoint-and-wholly-contained-images"
aliases:
  - /app_offline-htm-and-sharepoint-and-wholly-contained-images/
---

The question came up today if we could use an “app\_offline.htm” file along with HTML in that file that would reference images.

First, I wasn’t 100% sure if the app\_offline.htm would work, but it sure did.  Since it’s just the Asp.net hosting process that detects the file, it circumvents loading any HttpApplications (SharePoint) beyond just serving up the HTML content.

The second question was about having something more than text, specifically <img> tags.  So, since the HttpHandlers are taking all requests for all resources through the Asp.net pipeline, as soon as the app\_offline.htm file is there, nothing else will get served from within that web application.    Sure, we could host the file (images) outside the web app, but what fun would that be?

So, I found this link on using an image in app\_offline.htm

[http://pbodev.wordpress.com/2009/12/20/app\_offline-htm-with-an-image-yes-we-can/](http://pbodev.wordpress.com/2009/12/20/app_offline-htm-with-an-image-yes-we-can/ "http://pbodev.wordpress.com/2009/12/20/app_offline-htm-with-an-image-yes-we-can/")

Turns out, the src tag (in fact many tags) can take a stream of data represented by a mime type and base64 encoding inline – such as:

```
<img style="height:515px;width:700px;border-width:0px;"  src="data:image/jpeg;base64,/9j/4AAQSkZJRgA
```

One of the problems we had was the image was too large; so, sliced up the image, but ended up with spaces between each of the slices.  Low and behold, it works with CSS as well.

```
    <style type="text/css">
        .Slice_1_jpg
        {
            position: absolute;
            left:0px;
            top:0px;
            width:1011px; 
            height:148px;
            background: url("data:image/jpeg;base64,/9j/4AAQSkZ
```

And the body is as follows:

```
  <body>
    <div class="Slice_1_jpg"> </div>
```

For this, I wrote a little Asp.Net site that, using a file upload control, will generate the necessary contents of what needs to go in the “data” value for the stream.  A link to the code is here:

[http://cicoria.com/downloads/CreateBase64OfImage.zip](http://cicoria.com/downloads/CreateBase64OfImage.zip "http://cicoria.com/downloads/CreateBase64OfImage.zip")
