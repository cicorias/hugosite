---
title: "SAML Request / Response decoding."
date: 2011-01-29T00:59:43+0000
lastmod: 2011-01-29T00:59:43+0000
slug: "saml-request-response-decoding"
aliases:
  - /saml-request-response-decoding/
---

When you’re working with Web SSO integration, sometimes it’s helpful to be able to decode the tokens that get passed around via the browser from the various participants in the trust – RP, STS, etc.

With SAML tokens, sometimes they’re simply base64 encoded when they’re in the POST body; other times they’re part of the query string, which they end up being base64encoded, deflated, then Url encoded.

I always end up putting together some simple tool that does this for me – so, this is an effort to make this more permanent.

It’s a simple WinForms application that is using NetFx 4.0.

[![image](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/5811.image_thumb_63732726.png "image")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/0118.image_5E04B682.png)

[Download](http://cicoria.com/downloads/base64tool.zip)
