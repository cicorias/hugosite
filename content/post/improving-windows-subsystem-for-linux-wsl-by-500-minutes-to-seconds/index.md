---
title: "Improving Windows Subsystem for Linux WSL by 500% - Minutes to Seconds"
date: 2018-08-25T10:43:54+0000
lastmod: 2018-08-25T10:43:54+0000
slug: "improving-windows-subsystem-for-linux-wsl-by-500-minutes-to-seconds"
feature_image: "https://www.cicoria.com/content/images/2018/08/image-1.png"
aliases:
  - /improving-windows-subsystem-for-linux-wsl-by-500-minutes-to-seconds/
---

# Performance of WSL and Disk IO

The core performance killer is related to Windows Defender, and a primary scenarios is running Node package installers that are pulling down 100s, perhaps 1000s of files during an `npm install <package>`.

For example, when I ran `nvm install --lts --latest-npm` it took about **5 minutes** on a Razer with NVMe storage. Once I made a small modification in Defender to exclude the `/rootfs` of that App Store installation directory in Windows Defender it took about **30 seconds** - I do have a Fios 1Gbps connection. That was even after cleaning the npm cache, etc.

# WSL Basics and new Linux Apps

In the current **Windows 10 1803** release, Linux Apps from the Microsoft App Store are now quite a bit simpler in distribution, and much more isolated. For example, you can side-by-side have **Ubuntu 16.04** and **Ubuntu 18.04** on the same machine.

Below is a section of my start menu tiles showing various flavors of Linux Store Apps

![Start menu tiles](https://cicoria.blob.core.windows.net/blog/images/wsl-performance/2018-08-25_10-06-44.png)

What this means is each Windows App gets a private space in the `C:\Program Files\WindowsApps` sub-directory. Normally you can't just navigate to that path without modifying permissions. But with this approach, you don't have to.

## Getting the Path of the Ubuntu / Linux App

You actually have to do this with each new update in the App Store of the Linux app. The logic to find a physical path of a Windows App is awfully convoluted, but possible. I just haven't had the need yet to fully automate.

First, do this if you haven't already run the App yet and initialized the `rootfs` as part of first run. After you install say Ubuntu 16.04 from the Windows App Store, start it up - then open up Windows Task Manager - you should see something like this, where I've expanded the **Ubuntu** App to show all the real processes associated with it:

![TaskManager](https://cicoria.blob.core.windows.net/blog/images/wsl-performance/taskmanager.png)

At this point, after a first run, you can navigate to the `/rootfs` for that App, and while you're there, highlight the whole Address Path and Ctrl+C.

![Rootfs](https://cicoria.blob.core.windows.net/blog/images/wsl-performance/rootfs.png)

Now, open up WIndows Defender -> Exclusions - and we just add that Path as a Folder Exclusion.

![Defender exclusion](https://cicoria.blob.core.windows.net/blog/images/wsl-performance/defender.png)
