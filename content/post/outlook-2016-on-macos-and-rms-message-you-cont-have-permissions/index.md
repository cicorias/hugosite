---
title: "Outlook 2016 on macOS and RMS Message - You don't have permissions"
date: 2016-10-07T23:03:48+0000
lastmod: 2016-11-19T15:03:34+0000
slug: "outlook-2016-on-macos-and-rms-message-you-cont-have-permissions"
feature_image: "/images/2016/10/Bullshit_free-2.jpg"
aliases:
  - /outlook-2016-on-macos-and-rms-message-you-cont-have-permissions/
---

I have way too many things in dogfood. This is just a reminder on some RMS issues that I've been having lately on OS X (macOS) and Outlook 2016.

Courtesy JPoon.

```
(a) Close all (!) Office Programs
(b) Delete:
   rm -r ~/Library/Containers/com.microsoft.RMS-XPCService 
   rm ~/Library/Group\ Containers/UBF8T346G9.Office/DRM.plist
      and/or
   rm ~/Library/Group\ Containers/UBF8T346G9.Office/DRM_Evo.plist
(c) clearing your credentials by searching Keychain Access for "adal" and removing all entries.

```
