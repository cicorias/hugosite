---
title: "Why you should never say “Turn ON Intranet Settings” in Internet Explorer IE"
date: 2014-10-26T11:45:12+0000
lastmod: 2014-10-26T11:45:12+0000
slug: "why-you-should-never-say-turn-on-intranet-settings-in-internet-explorer-ie"
aliases:
  - /why-you-should-never-say-turn-on-intranet-settings-in-internet-explorer-ie/
---

I recently checked into a hotel – connected to their guest wireless – and I start noticing odd things with some websites.

**UPDATE: corrected title to conform to the message – thanks Mark…**

If you’ve ever seen the following:

![](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/47/13/metablogapi/8078.image_3A514A17.png)

**NEVER say “Turn on Intranet Settings”.**

In my case, the hotel’s wireless (specifically their DHCP server) was returning a WPAD (Browser Proxy Autoconfiguration) with the following:

```
function FindProxyForURL(url, host)
{
  return "DIRECT";
}

```

Which for IE that means ALL sites will be mapped to the **Intranet** Zone automatically IF you’ve **“Turned ON Intranet Settings”.**  This is **bad, bad, bad.**

That means IE runs in Unprotected Mode for ALL internet sites.

If you have responded “incorrectly” – then you can reset it to auto as follows:

[![image](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/7752.image_thumb_32EBB646.png "image")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/7652.image_1BBDAB17.png)

Finally, if you want to see the message where IE WOULD HAVE mapped the zone to Intranet you can turn back on the warning via regedit:

```
Windows Registry Editor Version 5.00

[HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings]  

"WarnOnIntranet"=dword:00000001

```

See [http://blogs.msdn.com/b/ieinternals/archive/2012/06/05/the-local-intranet-security-zone.aspx](http://blogs.msdn.com/b/ieinternals/archive/2012/06/05/the-local-intranet-security-zone.aspx "http://blogs.msdn.com/b/ieinternals/archive/2012/06/05/the-local-intranet-security-zone.aspx")  for more information
