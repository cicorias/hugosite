---
title: "Host named site collections and Web Application Extensions"
date: 2013-08-14T05:55:40+0000
lastmod: 2013-08-14T05:55:40+0000
slug: "host-named-site-collections-and-web-application-extensions"
aliases:
  - /host-named-site-collections-and-web-application-extensions/
---

The question came up about whether the mix of an SharePoint 2013 extended web application that may have different authentication providers, could also support Host Named Site Collections (HNSC).

Well, they can.  The documentation isn’t that clear, never seen it explicitly called out.

But, just from a foundation of setting up a web application, extending it, then establishing a HNSC that is addressable from 2 different SP Zones (Extended zone), these are the simple steps:

#1   
New-SPWebApplication -Name 'Wingtip Public HNSC' -port 8000 -ApplicationPool WingtipHnscAppPool -ApplicationPoolAccount (Get-SPManagedAccount 'wingtip\svc\_spcontent') -AuthenticationProvider (New-SPAuthenticationProvider –UseWindowsIntegratedAuthentication)

#1.1 - create a root site collection....   
New-SPSite '<http://WINGTIPSERVER:8000'> -Name 'Portal' -Description 'Portal on root' -OwnerAlias 'wingtip\administrator' -language 1033 -Template 'STS#0'

#2   
Get-SPWebApplication '<http://WINGTIPSERVER:8000'> | New-SPWebApplicationExtension -Name "Internet Site" -Zone "Internet" -Port 80 -URL "<http://internet.wingtip.com">

#3   
New-SPSite '<http://hnsc1.wingtip.com:8000'> -HostHeaderWebApplication '<http://WINGTIPSERVER:8000’> -Name 'HNSC1' -Description 'HNSC 1' -OwnerAlias 'wingtip\administrator' -language 1033 -Template 'STS#0'

#4   
Set-SPSiteUrl (Get-SPSite '<http://hnsc1.wingtip.com:8000')> –Url '<http://p-hnsc1.wingtip.com'> –Zone Internet
