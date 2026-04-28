---
title: "Cleaning up IIS Express sites v2"
date: 2015-07-01T13:18:11+0000
lastmod: 2015-07-01T13:18:11+0000
slug: "cleaning-up-iis-express-sites-v2"
aliases:
  - /cleaning-up-iis-express-sites-v2/
---

This one deals with a single site…

Again, I’m a tidy person.

```
$appCmd = "C:\Program Files (x86)\IIS Express\appcmd.exe"
$result = Invoke-Command -Command {& $appCmd 'list' 'sites' '/text:SITE.NAME' }

function deleteSite($site){

Invoke-Command -Command {& $appCmd 'delete' 'site'  $site }  

}

if ($result -is [system.array]){  

for ($i=0; $i -lt $result.length; $i++)  

{  

deleteSite($result[$i])  

}  

}  

else {  

deleteSite($result)  

}

```
