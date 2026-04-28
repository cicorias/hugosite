---
title: "Installing WCF CTP Extensions with VS 2005 after .NET 3.0 service packs...."
date: 2008-10-22T12:48:31+0000
lastmod: 2008-10-22T12:48:31+0000
slug: "installing-wcf-ctp-extensions-with-vs-2005-after-net-3-0-service-packs"
aliases:
  - /installing-wcf-ctp-extensions-with-vs-2005-after-net-3-0-service-packs/
---

If you're installing Visual Studio 2005 and need the WCF CTP Extensions, BUT you've already installed .NET 3.0 with service packs, the installer fails.

To override the check use the following:

msiexec /i vsextwfx.msi WRC\_INSTALLED\_OVERRIDE=1
