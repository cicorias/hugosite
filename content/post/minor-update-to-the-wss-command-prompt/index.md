---
title: "Minor update to the WSS Command Prompt…"
date: 2009-11-11T06:59:32+0000
lastmod: 2009-11-11T06:59:32+0000
slug: "minor-update-to-the-wss-command-prompt"
aliases:
  - /minor-update-to-the-wss-command-prompt/
---

Take the following and paste into a VBS file – then run.

Still need to choose the Link, then set the “Run as administrator” when UAC is on…

```
Set Shell = CreateObject("WScript.Shell") 
Set Env = Shell.Environment("PROCESS") 
DesktopPath = Shell.SpecialFolders("Desktop") 
Set link = Shell.CreateShortcut(DesktopPath & "\WSS CMD.lnk")

cssHive = Env("CommonProgramFiles") & "\Microsoft Shared\web server extensions\12"  

currentPath = RTrim(Replace(WScript.ScriptFullName, WScript.ScriptName, ""))  

envBatFile = "setWssPath.cmd"

CreateBatFile currentPath & setWssPath & envBatFile, cssHive

link.Arguments = "/k " & " " & Chr(34) & currentPath & envBatFile & Chr(34)  

link.Description = "WSS Command Prompt"  

link.HotKey = "CTRL+SHIFT+W"  

link.IconLocation = "%SystemRoot%\system32\SHELL32.dll,94"  

link.TargetPath = "%comspec%"  

link.WindowStyle = 1  

link.WorkingDirectory = cssHive  

link.Save  

Sub CreateBatFile(fileName, cssHive)  

Set fso = CreateObject("Scripting.FileSystemObject")  

Set file = fso.CreateTextFile(fileName, True)  

file.WriteLine("@SET PATH=%PATH%;" & cssHive & "\bin")  

file.WriteLine("@ECHO WSS CMD Shell - Shawn Cicoria")  

file.WriteLine("CD " & cssHive)

End Sub

```
