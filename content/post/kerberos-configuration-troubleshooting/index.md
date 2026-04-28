---
title: "Kerberos Configuration Troubleshooting"
date: 2009-02-26T03:17:42+0000
lastmod: 2009-02-26T03:17:42+0000
slug: "kerberos-configuration-troubleshooting"
aliases:
  - /kerberos-configuration-troubleshooting/
---

I wanted to post about one of the best tools I’ve found for getting Kerberos properly configured and in the process getting some great HOWTO information on Kerberos, how it works, etc.

When working with SharePoint, and the plan is to have your site run under Kerberos, I recommend using this tool before actually provisioning the Web App.  You can do it later, but you’d have to “stop” the WSS provisioned Web App before using this tool.  Why?  Because the IIS site you use for testing must use the DNS name of the Web App – that ultimately is the key to Kerberos – getting all the SPN (servicePrincipalName) set for the right AD Principals.

Basically, before actually creating or extending your web app in SharePoint, which would provision the Web App in IIS, you setup an standard IIS ASP.NET Virtual Host in IIS using the same DNS name as the eventual SharePoint Web App, set the App Pool to the Principal that going to be the App Pool for the Web App, then, put the DeleConfig files in the IIS site and hit the default page; gives fantastic diagnostic information on if Kerberos is setup correctly.  I'd suggest this as a first step...

[http://blogs.iis.net/brian-murphy-booth/archive/2007/03/09/delegconfig-delegation-configuration-reporting-tool.aspx](http://blogs.iis.net/brian-murphy-booth/archive/2007/03/09/delegconfig-delegation-configuration-reporting-tool.aspx "http://blogs.iis.net/brian-murphy-booth/archive/2007/03/09/delegconfig-delegation-configuration-reporting-tool.aspx")

[http://www.iis.net/downloads/default.aspx?tabid=34&g=6&i=1434](http://www.iis.net/downloads/default.aspx?tabid=34&g=6&i=1434 "http://www.iis.net/downloads/default.aspx?tabid=34&g=6&i=1434")
