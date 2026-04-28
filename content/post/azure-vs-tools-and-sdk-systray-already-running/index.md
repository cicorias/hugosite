---
title: "Azure VS Tools and SDK - systray already running…"
date: 2011-03-02T13:25:47+0000
lastmod: 2011-03-02T13:25:47+0000
slug: "azure-vs-tools-and-sdk-systray-already-running"
aliases:
  - /azure-vs-tools-and-sdk-systray-already-running/
---

If you are getting a message when you start the Compute Emulator “Systray already running…” from within Visual Studio one fix is to check what the image name is loading is.

For some reason, on 2 of my machines the image was loading with the 8.3 format.  This caused the logic in the VS tools to not find the process.

So, to fix, I just did a little copy/rename magic.

```
C:\Program Files\Windows Azure SDK\v1.3\bin>copy csmonitor.exe csmonitor-a.exe
        1 file(s) copied.
C:\Program Files\Windows Azure SDK\v1.3\bin>del csmonitor.exe

C:\Program Files\Windows Azure SDK\v1.3\bin>copy csmonitor-a.exe csmonitor.exe  

1 file(s) copied.

```

If you bring up task manager and see something like CSMON~1.EXE in the Image Name column, you probably have this issue.
