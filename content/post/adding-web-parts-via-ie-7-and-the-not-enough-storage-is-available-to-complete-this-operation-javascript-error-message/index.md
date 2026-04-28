---
title: "Adding Web Parts via IE 7 and the “Not enough storage is available to complete this operation” javascript Error Message…"
date: 2009-01-15T10:39:00+0000
lastmod: 2009-01-15T10:39:00+0000
slug: "adding-web-parts-via-ie-7-and-the-not-enough-storage-is-available-to-complete-this-operation-javascript-error-message"
aliases:
  - /adding-web-parts-via-ie-7-and-the-not-enough-storage-is-available-to-complete-this-operation-javascript-error-message/
---

Recently, installed a bunch of new Windows Live components such as Messenger, etc.

That update extended my HTTP\_USER\_AGENT string to beyond 260 characters, which unfortunately IE then, when asked via javascript, reports itself back as IE 6 – this causes the Modal dialog boxes in SharePoint for things like adding web parts to zones to report a message that “Not enough storage is available to complete this operation”.

So, since this is an x64 machine, I need to trim down the string which is taken from the following registry key:

> HKEY\_LOCAL\_MACHINE\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Internet Settings\5.0\User Agent\Post Platform

My key was the following:

> Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; WOW64; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; InfoPath.2; .NET CLR 3.5.21022; .NET CLR 1.1.4322; WWTClient2; .NET CLR 3.5.30729; .NET CLR 3.0.30618; Zune 3.0; MS-RTC LM 8; OfficeLiveConnector.1.3; OfficeLivePatch.0.0)

For now, I’ll take out the OfficeLiveConnector (which I’m NOT using now) from the AG
