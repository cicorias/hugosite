---
title: "Cleaning up IIS Express Sites"
date: 2013-03-08T04:00:51+0000
lastmod: 2013-03-08T04:00:51+0000
slug: "cleaning-up-iis-express-sites"
aliases:
  - /cleaning-up-iis-express-sites/
---

Over time, you may end up with lots of sites running in IIS Express.  I like things neat and tidy, and periodically, I’ll run a little cleanup command as follows:

From PowerShell:

```
$appCmd = "C:\Program Files (x86)\IIS Express\appcmd.exe"

$result = Invoke-Command -Command {& $appCmd 'list' 'sites' '/text:SITE.NAME' }

for ($i=0; $i -lt $result.length; $i++)  

{  

Invoke-Command -Command {& $appCmd 'delete' 'site'  $result[$i] }  

}

```
