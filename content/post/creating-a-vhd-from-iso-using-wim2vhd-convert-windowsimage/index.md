---
title: "Creating a VHD from ISO using WIM2VHD Convert-WindowsImage …"
date: 2015-12-07T05:05:04+0000
lastmod: 2015-12-07T05:05:04+0000
slug: "creating-a-vhd-from-iso-using-wim2vhd-convert-windowsimage"
aliases:
  - /creating-a-vhd-from-iso-using-wim2vhd-convert-windowsimage/
---

This script here helps in creating VHD’s on the fly. Recently I needed to quickly create some VHDX from an ISO that are “arm-able” for some labs.

The tool  I used is:

> ###### [Convert-WindowsImage.ps1](https://gallery.technet.microsoft.com/scriptcenter/Convert-WindowsImageps1-0fe23a8f) — WIM2VHD for Windows 10 (also Windows 8 and 8.1)

> Convert-WindowsImage is the new version of WIM2VHD designed specifically for Windows 8 and above. Written in PowerShell, this command-line tool allows you to rapidly create sysprepped VHDX and VHDX images from setup media for Windows 7/Server 2008 R2, Windows 8/8.1/Server 2012/R2

[https://gallery.technet.microsoft.com/scriptcenter/Convert-WindowsImageps1-0fe23a8f](https://gallery.technet.microsoft.com/scriptcenter/Convert-WindowsImageps1-0fe23a8f "https://gallery.technet.microsoft.com/scriptcenter/Convert-WindowsImageps1-0fe23a8f")

Here’s the basic script I used…

```

$iso = 'E:\users\shawn\Downloads\en_windows_server_2012_r2_with_update_x64_dvd_6052708.iso'
$workdir = 'e:\temp\iso'
$vhdpath = 'e:\temp\iso\thevhd.vhdx'

# Load (aka "dot-source) the Function

. .\Convert-WindowsImage.ps1

# Prepare all the variables in advance (optional)

$ConvertWindowsImageParam = @{  

SourcePath          = $iso  

RemoteDesktopEnable = $True  

Passthru            = $True  

Edition    = "ServerDataCenter"  

VHDFormat = "VHDX"  

SizeBytes = 60GB  

WorkingDirectory = $workdir  

VHDPath = $vhdpath  

VHDPartitionStyle = 'GPT'  

}

$VHDx = Convert-WindowsImage @ConvertWindowsImageParam

```
