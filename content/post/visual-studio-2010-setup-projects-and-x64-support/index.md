---
title: "Visual Studio 2010 Setup Projects and x64 Support"
date: 2010-12-21T14:24:59+0000
lastmod: 2010-12-21T14:24:59+0000
slug: "visual-studio-2010-setup-projects-and-x64-support"
aliases:
  - /visual-studio-2010-setup-projects-and-x64-support/
---

I was taking the Windows Azure CmdLets project and getting it into an MSI just to make it easier to deploy in a nice package.  I ran into problems with the Setup project not being able to properly establish the right registry settings for an x64 environment.

Even though you set the target platform on the Setup project to x64 the InstallUtil.lib that get’s run is still x86.  In order to have it work property, you need to follow the steps identified here:

[http://msdn.microsoft.com/en-us/library/kz0ke5xt.aspx](http://msdn.microsoft.com/en-us/library/kz0ke5xt.aspx "http://msdn.microsoft.com/en-us/library/kz0ke5xt.aspx")

The section “64-bit managed custom actions throw a System.BadImageFormatException exception” covers the steps you need to follow, using the Orca MSI editor to replace the InstallUtilLib.dll from the one that the Setup Project embeds (x86) to a x64 version.

Now, works like a charm…

Resultant installer here:

[http://cicoria.com/Downloads/AzureManagementCmdletsInstall.msi](http://cicoria.com/Downloads/AzureManagementCmdletsInstall.msi "http://cicoria.com/Downloads/AzureManagementCmdletsInstall.msi")

The CmdLets are the same ones from the Training Kit – November 2010 release.
