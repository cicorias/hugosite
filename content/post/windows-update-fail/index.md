---
title: "Windows Update Fail Microsoft-OneCore-DeveloperMode-Desktop-Package Error = 0x800F081F-0x20003"
date: 2018-12-03T12:49:13+0000
lastmod: 2018-12-03T12:49:13+0000
slug: "windows-update-fail"
feature_image: "/images/2018/12/image.png"
aliases:
  - /windows-update-fail/
---

First - **WHY WHY WHY** doesn't the installer just deal with this error? What's clear from the message, or at least to me, is that the Developer Mode package added in "Developer Mode" is some sort of problem.

First I tried DISM to repiar.

```
C:\WINDOWS\system32> DISM.exe /Online /Cleanup-image /Restorehealth

Deployment Image Servicing and Management tool
Version: 10.0.17134.1

Image Version: 10.0.17134.441

[==========================100.0%==========================] The restore operation completed successfully.
The operation completed successfully.
C:\WINDOWS\system32>

```

Then I just disabled developer mode under "Updates -> For Developers" putting the setting back to "Sideload Apps".

Finally, and this is important, under "Apps and Features -> Manage optional features" - find "Windows Developer Mode" and uninstall it.

Again, this should "just work" and the installer shouldn't have these issues as it's an os update. WTF
