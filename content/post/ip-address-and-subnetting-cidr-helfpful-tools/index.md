---
title: "IP Address and Subnetting CIDR Helpful Tools - ipcalc cli"
date: 2023-04-30T16:31:21+0000
lastmod: 2023-04-30T16:31:21+0000
slug: "ip-address-and-subnetting-cidr-helfpful-tools"
tags: ["bash", "utilities"]
feature_image: "https://www.cicoria.com/content/images/2023/04/ipcalc.png"
aliases:
  - /ip-address-and-subnetting-cidr-helfpful-tools/
---

How often are you subnetting, or just trying to get valid sets of CIDR (classless inter-domain routing) addresses?

For that there are a bunch of online tools, but the one tool I prefer is the ipcalc command line tool.  The Linux man page is here: [ipcalc man | Linux Command Library](https://linuxcommandlibrary.com/man/ipcalc)

It's also available on macOS using Homebrew via `brew install ipcalc` – and there is an online-version here: <http://jodies.de/ipcalc>

Full source is here: [ipcalc / ipcalc · GitLab](https://gitlab.com/ipcalc/ipcalc)

![](https://www.cicoria.com/content/images/2023/04/image.png)

An example might be, lets say you have a segment that needs to have 16 addresses per subnet. Just ask `ipcalc 10.0.0.0/16 -s 14`

![](https://www.cicoria.com/content/images/2023/04/image-1.png)
