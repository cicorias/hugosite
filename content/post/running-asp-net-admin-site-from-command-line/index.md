---
title: "Running ASP.NET admin site from command line"
date: 2013-09-26T12:29:48+0000
lastmod: 2013-09-26T12:29:48+0000
slug: "running-asp-net-admin-site-from-command-line"
aliases:
  - /running-asp-net-admin-site-from-command-line/
---

Great tip from Dominic Baer.

<http://leastprivilege.com/2012/06/28/managing-asp-net-membership-and-roles-without-visual-studio/>

& ‘C:\Program Files (x86)\Common Files\microsoft shared\DevServer\10.0\WebDev.WebServer40.EXE’ /path:”C:\Windows\   
Microsoft.NET\Framework64\v4.0.30319\ASP.NETWebAdminFiles” /port:8080 /vpath:”/asp.netwebadminfiles”

Afterwards you can navigate to the site using this URL:

<http://localhost:8080/asp.netwebadminfiles/default.aspx?applicationPhysicalPath=>*path*&applicationUrl=*/vdir*
