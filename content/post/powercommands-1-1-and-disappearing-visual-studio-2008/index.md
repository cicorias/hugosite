---
title: "PowerCommands 1.1 and disappearing Visual Studio 2008"
date: 2008-11-24T11:39:31+0000
lastmod: 2008-11-24T11:39:31+0000
slug: "powercommands-1-1-and-disappearing-visual-studio-2008"
aliases:
  - /powercommands-1-1-and-disappearing-visual-studio-2008/
---

If youre running Visual Studio 2008 SP1 and you're also a [PowerCommands](http://code.msdn.microsoft.com/PowerCommands) fan you might run into the issue that VS just crashes with no exception box and only the following error in the Application event log:

.NET Runtime version 2.0.50727.3053 - Fatal Execution Engine Error (000007FEF63D203F) (0)

To correct, you need to have an assembly redirection put into the devenv.exe.config file (which .NET will use for configuration information while running in VS..

       <dependentAssembly>   
                <assemblyIdentity name="Microsoft.PowerCommands" publicKeyToken="null" culture="neutral"/>   
                <codeBase version="1.1.0.0" href="C:\Program Files (x86)\PowerCommands\Microsoft.PowerCommands.dll"/>   
            </dependentAssembly>

More is posted here:

<http://social.msdn.microsoft.com/Forums/en-US/vssetup/thread/e2434065-9921-4861-b914-9cc9d6c55553/>

PowerCommands 1.1

[http://code.msdn.microsoft.com/PowerCommands](http://code.msdn.microsoft.com/PowerCommands "http://code.msdn.microsoft.com/PowerCommands")
