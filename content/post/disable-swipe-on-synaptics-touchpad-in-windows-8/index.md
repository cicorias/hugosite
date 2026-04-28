---
title: "Disable swipe on synaptics touchpad in Windows 8"
date: 2013-01-28T23:20:00+0000
lastmod: 2013-01-28T23:20:00+0000
slug: "disable-swipe-on-synaptics-touchpad-in-windows-8"
aliases:
  - /disable-swipe-on-synaptics-touchpad-in-windows-8/
---

If you're using a touchpad on a laptop, like me with some fat fingers, the swip action is actually quite intrusive.  you can turn if off with the following

Disable swipe on Trackpad

```
Windows Registry Editor Version 5.00  [HKEY_CURRENT_USER\Software\Synaptics\SynTPEnh\ZoneConfig\TouchPadPS2\Right Edge Pull]  "ActionType"=dword:00000000  [HKEY_CURRENT_USER\Software\Synaptics\SynTPEnh\ZoneConfig\TouchPadPS2\Left Edge Pull]  "ActionType"=dword:00000000  [HKEY_CURRENT_USER\Software\Synaptics\SynTPEnh\ZoneConfig\TouchPadPS2\Right Edge Pull Extended Zone]  "ActionType"=dword:00000000  [HKEY_CURRENT_USER\Software\Synaptics\SynTPEnh\ZoneConfig\TouchPadPS2\Top Edge Pull]  "ActionType"=dword:00000000
```

 Re-enable:

```
   Windows Registry Editor Version 5.00 [HKEY_CURRENT_USER\Software\Synaptics\SynTPEnh\ZoneConfig\TouchPadPS2\Right Edge Pull] "ActionType"=dword:00000002 [HKEY_CURRENT_USER\Software\Synaptics\SynTPEnh\ZoneConfig\TouchPadPS2\Left Edge Pull] "ActionType"=dword:00000002 [HKEY_CURRENT_USER\Software\Synaptics\SynTPEnh\ZoneConfig\TouchPadPS2\Right Edge Pull Extended Zone] "ActionType"=dword:00000002 [HKEY_CURRENT_USER\Software\Synaptics\SynTPEnh\ZoneConfig\TouchPadPS2\Top Edge Pull] "ActionType"=dword:00000002
```
