---
title: "Making a Win7 Bootable USB device."
date: 2009-05-04T02:21:04+0000
lastmod: 2009-05-04T02:21:04+0000
slug: "making-a-win7-bootable-usb-device"
aliases:
  - /making-a-win7-bootable-usb-device/
---

I have an old Toshiba that has no optical drive.  To install Win7, I needed a bootable USB stick.  Here are the basic steps

0. Download Win7 [http://www.microsoft.com/windows/windows-7/](http://www.microsoft.com/windows/windows-7/ "http://www.microsoft.com/windows/windows-7/")

1. Get a USB stick – need a 4 gig one here – the ISO is about 2.5 GIG

2. Format the USB as NTFS (use quick – no need for sector check) – it MUST be NTFS

3. Run DISKPART from an elevated command prompt

4. Make the new USB volume “ACTIVE”

5. Extract the Win7 ISO somewhere (not the USB) – you can use [ImgBurn](http://www.imgburn.com/), [IsoBuster](http://www.isobuster.com/), [WinRar](http://www.rarlab.com/) or some tool that can extract direct from an ISO – or mount with Daemon tools or similar, then copy the files from there.  We need to extract first as we’ll need to run a quick program off of the Win7 ISO

6. On the recent Win7 extract, change to the BOOT subdirectory

7. Run BOOTSECT /NT60 <targetDrive:>

       where , <targetDrive> is the drive the USB stick is mounted as….

8. Copy all the files from step 5 above to the ROOT of the USB stick (with subdirectories of course)

Now, you may be able to skip step 5 copying files across and running BOOTSECT directly – I hadn’t but doesn’t necessarily mean it won’t work.

del.icio.us Tags: [Win7](http://del.icio.us/popular/Win7),[USB](http://del.icio.us/popular/USB),[Installation](http://del.icio.us/popular/Installation)
