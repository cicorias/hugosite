---
title: "Getting a user’s SID via PowerShell…"
date: 2013-07-01T03:58:00+0000
lastmod: 2013-07-01T03:58:00+0000
slug: "getting-a-users-sid-via-powershell"
aliases:
  - /getting-a-users-sid-via-powershell/
---

For future ref…

```
$user = New-Object System.Security.Principal.NTAccount("contoso", "user") 
$sid = $user.Translate([System.Security.Principal.SecurityIdentifier]) 
$sid.Value
```
