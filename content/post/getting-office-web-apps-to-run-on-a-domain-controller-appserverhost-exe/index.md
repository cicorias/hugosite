---
title: "Getting Office Web Apps to run on a Domain controller - AppServerHost.exe"
date: 2011-04-14T14:50:55+0000
lastmod: 2011-04-14T14:50:55+0000
slug: "getting-office-web-apps-to-run-on-a-domain-controller-appserverhost-exe"
aliases:
  - /getting-office-web-apps-to-run-on-a-domain-controller-appserverhost-exe/
---

I recall we had a similar issue when running document conversion services.

If you’re attempting Word or PowerPoint viewing and you see errors in the event log regarding AppServerHost.exe – you need to enable non-sandboxing.

[http://blogs.msdn.com/b/opal/archive/2010/04/25/faq-sharepoint-2010-rtm-installation.aspx](http://blogs.msdn.com/b/opal/archive/2010/04/25/faq-sharepoint-2010-rtm-installation.aspx "http://blogs.msdn.com/b/opal/archive/2010/04/25/faq-sharepoint-2010-rtm-installation.aspx")

Open SharePoint 2010 Management Shell, then run:

#Enable Word Web App:

$e = Get-SPServiceApplication | where {$\_.TypeName.Equals("Word Viewing Service Application")}   
$e.WordServerIsSandboxed = $false   
$e.WordServerIsSandboxed

#Enable PowerPoint Web App - you need to answer "Y" for each command:

Get-SPPowerPointServiceApplication | Set-SPPowerPointServiceApplication -EnableSandboxedViewing $false   
Get-SPPowerPointServiceApplication | Set-SPPowerPointServiceApplication -EnableSandboxedEditing $false

On the server, use Notepad to open c:\windows\system32\inetsrv\config\applicationHost.config.  Add the line below at the end of the dynamicTypes section.   
<add mimeType="application/zip" enabled="false" />
