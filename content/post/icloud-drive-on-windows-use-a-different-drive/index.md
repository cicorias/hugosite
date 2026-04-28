---
title: "iCloud drive on Windows - use a different drive."
date: 2016-07-27T20:59:40+0000
lastmod: 2016-07-27T20:59:40+0000
slug: "icloud-drive-on-windows-use-a-different-drive"
feature_image: "https://www.cicoria.com/content/images/2016/07/icloud-08-700x393.png"
aliases:
  - /icloud-drive-on-windows-use-a-different-drive/
---

I just installed iCloud for Windows as I have quite a bit up on iCloud now, and even paying for the 100GB plan.

Problem is I want the drive to be on my data disk - which is E:. Of course iCloud is far behind in offering options to control that.

But we can deal with this using a Symbolic Link:

```
mklink /D c:\Users\shawn\iCloudDrive e:\Users\Shawn\iCloud
symbolic link created for c:\Users\shawn\iCloudDrive <<===>> e:\Users\Shawn\iCloud

```

Ran this, and iCloud is non-the-wiser.
