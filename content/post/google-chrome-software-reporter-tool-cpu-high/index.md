---
title: "Google Chrome Software Reporter Tool CPU High"
date: 2020-05-11T14:08:56+0000
lastmod: 2020-05-11T14:08:56+0000
slug: "google-chrome-software-reporter-tool-cpu-high"
feature_image: "/images/2020/05/image-3.png"
aliases:
  - /google-chrome-software-reporter-tool-cpu-high/
---

Anyone else has this software reporter tool and High CPU? First, I don't like the fact there's nothing in Chrome settings to disable this.

Secondly, why is it so poorly written for Windows that it slams the CPU?

To disable, as there is a policy:

via cmd line in an Adminstrator Elevated session:

```
reg add hklm\SOFTWARE\Policies\Google\Chrome /v ChromeCleanupEnabled /t REG_DWORD /d 0
reg add hklm\SOFTWARE\Policies\Google\Chrome /v ChromeCleanupReportingEnabled/t REG_DWORD /d 0

```

Or put the following in a `*.reg` file and just open it, but in an Administrator elevated session.

```
Windows Registry Editor Version 5.00

[HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Google\Chrome]
"ChromeCleanupEnabled"=dword:00000000
"ChromeCleanupReportingEnabled"=dword:00000000

```

You can see these policies here:  
<https://www.chromium.org/administrators/policy-list-3#ChromeCleanupEnabled>  
<https://www.chromium.org/administrators/policy-list-3#ChromeCleanupReportingEnabled>
