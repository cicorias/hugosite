---
title: "This version of the enterprise library cannot be installed side by side with version 4.0 on x64"
date: 2009-05-22T08:56:40+0000
lastmod: 2009-05-22T08:56:40+0000
slug: "this-version-of-the-enterprise-library-cannot-be-installed-side-by-side-with-version-4-0-on-x64"
aliases:
  - /this-version-of-the-enterprise-library-cannot-be-installed-side-by-side-with-version-4-0-on-x64/
---

When upgrading to Enterprise Library 4.1 on an x64 machine, even though you’ve run the 4.0 uninstaller, and even removed the registry key, you’ll still end up with an installer complaining that you can’t do side-by-side install.  The issue is the key is actually under the Wow node for x86 compatability – just remove this key…
```
HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Microsoft\Enterprise Library v4
```
