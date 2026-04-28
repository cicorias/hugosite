---
title: "Using Virtual.Server COM interfaces on an x64 Machine and Visual Studio"
date: 2008-07-15T09:13:30+0000
lastmod: 2008-07-15T09:13:30+0000
slug: "using-virtual-server-com-interfaces-on-an-x64-machine-and-visual-studio"
aliases:
  - /using-virtual-server-com-interfaces-on-an-x64-machine-and-visual-studio/
---

Recently, I messed up a set of VHD files that were based upon differencing disks.  Basically, I killed the parent drive - so, any child drives are useless.

So, how do you know which drives are differencing disks and what is their parent?

One way is through the COM interfaces (that call into an out-of-process server).  Virtual Server must be installed and the service running for these interfaces to work.

However, on an X64 machine you won't be able, in Visual Studio 2005 or Visual Studio 2008 see the Typelib registered via the Add Reference -> COM tab.  Why? Because Visual Studio is 32 bit and the COM registration on x64 machines is not visible via the WOW64 Registry redirection.

So, a simple fix is to create (copy) the same sub key for win32.  A merge of the following will then allow you to set a reference and call into the interfaces

> Windows Registry Editor Version 5.00
>
> [HKEY\_CLASSES\_ROOT\TypeLib\{D7526A6D-CF83-48A4-87FD-4FBE2AEC5D93}\1.1\0\win32]   
> @="C:\\Program Files\\Microsoft Virtual Server\\vssrvc.exe"

What you then need to do is ensure you follow the steps in the MSDN article below to ensure proper COM initialization and setting of the apartment model to MTA instead of STA which is the default attribute applied via the VS templates.

[Connecting to the Virtual Server COM Object](http://msdn.microsoft.com/en-us/library/aa367595(VS.85).aspx)
