---
title: "Turning off the Visual Studio “Attach to process” security warning…"
date: 2012-04-12T02:00:57+0000
lastmod: 2012-04-12T02:00:57+0000
slug: "turning-off-the-visual-studio-attach-to-process-security-warning"
aliases:
  - /turning-off-the-visual-studio-attach-to-process-security-warning/
---

When you’re urnning under x64 you have to affect 1 addition spot in the registry to disable this warning – which clearly should only be done by folks that know what they’re doing.

NOTE: affecting the registry can be harmful – do so at your own risk.

Windows Registry Editor Version 5.00

```
Windows Registry Editor Version 5.00

[HKEY_CURRENT_USER\Software\Microsoft\VisualStudio\10.0\Debugger]  

"DisableAttachSecurityWarning"=dword:00000001

[HKEY_CURRENT_USER\Software\Wow6432Node\Microsoft\VisualStudio\10.0\Debugger]  

"DisableAttachSecurityWarning"=dword:00000001

```
