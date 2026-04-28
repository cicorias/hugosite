---
title: "A little bit more on the issue with “Not enough storage is available to complete the operation”"
date: 2009-01-16T12:15:27+0000
lastmod: 2009-01-16T12:15:27+0000
slug: "a-little-bit-more-on-the-issue-with-not-enough-storage-is-available-to-complete-the-operation"
aliases:
  - /a-little-bit-more-on-the-issue-with-not-enough-storage-is-available-to-complete-the-operation/
---

OK.  When the …\User Agent\Post Platform key (explained in the prior post) has too many items and the total length exceeds 260 characters, what happens is the javascript function windows.navigator.userAgent reports back as MSIE 6.0.

As follows – using the [http://www.fiddlertool.com/ua.aspx](http://www.fiddlertool.com/ua.aspx "http://www.fiddlertool.com/ua.aspx") test page:

#### With a HTTP\_USER\_AGENT string exceeding 260 characters:

[![image](https://msdnshared.blob.core.windows.net/media/TNBlogsFS/BlogFileStorage/blogs_msdn/scicoria/image_thumb_34761889.png "image")](https://msdnshared.blob.core.windows.net/media/TNBlogsFS/BlogFileStorage/blogs_msdn/scicoria/image_69269A91.png)

getComponentVersion says you are running Internet Explorer 7,0,6001,18000.

**window.navigator.userAgent:** [Mozilla/4.0 (compatible; MSIE 6.0)]   
**window.navigator.appMinorVersion:** [0]

#### With a string less than 260 characters

[![image](https://msdnshared.blob.core.windows.net/media/TNBlogsFS/BlogFileStorage/blogs_msdn/scicoria/image_thumb_254F13E2.png "image")](https://msdnshared.blob.core.windows.net/media/TNBlogsFS/BlogFileStorage/blogs_msdn/scicoria/image_048B50FB.png)

getComponentVersion says you are running Internet Explorer 7,0,6001,18000.

**window.navigator.userAgent:** [Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; WOW64; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; InfoPath.2; .NET CLR 3.5.21022; .NET CLR 1.1.4322; WWTClient2; .NET CLR 3.5.30729; .NET CLR 3.0.30618; Zune 3.0; MS-RTC LM 8; OfficeLivePatch.0.0)]   
**window.navigator.appMinorVersion:** [0]
