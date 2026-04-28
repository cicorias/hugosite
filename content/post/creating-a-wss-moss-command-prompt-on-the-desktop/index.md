---
title: "Creating a WSS / MOSS Command Prompt on the Desktop"
date: 2008-07-24T11:13:25+0000
lastmod: 2008-07-24T11:13:25+0000
slug: "creating-a-wss-moss-command-prompt-on-the-desktop"
aliases:
  - /creating-a-wss-moss-command-prompt-on-the-desktop/
---

**UPDATED: 8/6/2008 - Minor issue on Path**

I've built quite a few WSS / MOSS machines and one task that I always seem to do is create a simple CMD shell prompt on the desktop (quick launch, etc.) that gives me easy access to STSADM and has the path set correctly.  So in the interest of saving time I've created a simple VBScript file located [here](http://cicoria.com/downloads/WSS30/WssCmdShellTool.zip) as well as the full listing below

[![wsscmd](https://msdnshared.blob.core.windows.net/media/TNBlogsFS/BlogFileStorage/blogs_msdn/scicoria/WindowsLiveWriter/c6a878d52dcc_E414/wsscmd_thumb.jpg)](https://msdnshared.blob.core.windows.net/media/TNBlogsFS/BlogFileStorage/blogs_msdn/scicoria/WindowsLiveWriter/c6a878d52dcc_E414/wsscmd_2.jpg)

> Set Shell = CreateObject("WScript.Shell")   
> Set Env = Shell.Environment("PROCESS")   
> DesktopPath = Shell.SpecialFolders("Desktop")   
> Set link = Shell.CreateShortcut(DesktopPath & "\WSS CMD.lnk")
>
> cssHive = Env("CommonProgramFiles") & "\Microsoft Shared\web server extensions\12"   
> currentPath = RTrim(Replace(WScript.ScriptFullName, WScript.ScriptName, ""))   
> envBatFile = "setWssPath.cmd"
>
> CreateBatFile currentPath & setWssPath & envBatFile, cssHive
>
> link.Arguments = "/k " & " " & Chr(34) & currentPath & envBatFile & Chr(34)   
> link.Description = "WSS Command Prompt"   
> link.HotKey = "CTRL+SHIFT+W"   
> link.IconLocation = "%SystemRoot%\system32\SHELL32.dll,94"   
> link.TargetPath = "%comspec%"   
> link.WindowStyle = 1   
> link.WorkingDirectory = cssHive   
> link.Save
>
> Sub CreateBatFile(fileName, cssHive)   
>     Set fso = CreateObject("Scripting.FileSystemObject")   
>     Set file = fso.CreateTextFile(fileName, True)   
>     file.WriteLine("@SET PATH=%PATH%;" & cssHive & "\bin")   
>     file.WriteLine("@ECHO WSS CMD Shell - Shawn Cicoria")
>
> End Sub
