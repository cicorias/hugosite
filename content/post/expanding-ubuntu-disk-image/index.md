---
title: "Expanding Ubuntu Disk Image"
date: 2022-07-01T22:47:13+0000
lastmod: 2022-07-01T22:47:13+0000
slug: "expanding-ubuntu-disk-image"
tags: ["utilities", "vm"]
feature_image: "/images/2022/07/ubuntu-logo14.png"
aliases:
  - /expanding-ubuntu-disk-image/
---

I don't know how many times I have to look this up, but if I'm ever in Iceland, gotta personally thank

![](http://linguist.is/wp-content/uploads/2017/01/121148352_10159131257891019_4390820463615991948_o.jpg)

1. Turn off the VM.
2. Use Hyper-V Manager to select the Settings of the Virtual Machine, select the Hard Drive option and Edit under Virtual hard disk. (If this option is disabled, you need to go back and delete any checkpoints for the VM in the Hyper-V Manager; just select the VM and right click the checkpoint in the checkpoint field below.)
3. Use the GUI to expand the drive to something reasonable, like 128 GB. Ubuntu now has space to expand into.
4. Start the VM again. Install Guest Utils:

```
sudo apt install cloud-guest-utils

```
> If not using English, override locale settings to avoid issues with non-English locales:

```
LC_ALL=C

```

1. Expand the sda1 partition into the free space:

```
sudo growpart /dev/sda 1

```
> (Note the space between sda and 1!)

1. Finally run resize2fs:

```
sudo resize2fs /dev/sda1

```
> (No space between sda and 1 here!)
