---
title: "Disabling HyperV on Surface Pro 3 So Connected Standby will work or not work–depending on your mood"
date: 2014-06-23T00:19:51+0000
lastmod: 2014-06-23T00:19:51+0000
slug: "disabling-hyperv-on-surface-pro-3-so-connected-standby-will-work-or-not-workdepending-on-your-mood"
aliases:
  - /disabling-hyperv-on-surface-pro-3-so-connected-standby-will-work-or-not-workdepending-on-your-mood/
---

If you’re received your SP3 and you enabled HyperV you may have noticed that Connected Standby (new to x64) will then be disabled.

You’ll get this is you install Visual Studio 2013 with the Windows Phone emulator support in VS2013.

First step is to give you an option to “boot” or “restart” Windows in a mode with HyperV on or off so connected standby will “not work” or “work” (opposite of HyperV setting").

## Set HyperV as Default

```
C:\WINDOWS\system32>Bcdedit /copy {default} /d "HyperVisor Off"
The entry was successfully copied to {22393409-9568-11e2-be59-3c970e7cc5fa}.

C:\WINDOWS\system32>bcdedit /set {22393409-9568-11e2-be59-3c970e7cc5fa} hypervisorlaunchtype off  

The operation completed successfully.

```

Courtesy of Scott Hanselman – an easy UI way to restart your machine in your Choice.

<http://www.hanselman.com/blog/SwitchEasilyBetweenVirtualBoxAndHyperVWithABCDEditBootEntryInWindows81.aspx>

*In order to access the new boot menu, I select Settings (Windows Key + C) then Power, and Restart****but******hold down shift******on the keyboard while clicking Restart with the mouse.***

Note that the “Other Operating System” will be the one that just got copied.
