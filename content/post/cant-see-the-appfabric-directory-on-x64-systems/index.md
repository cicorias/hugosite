---
title: "Can’t see the AppFabric Directory on x64 systems…"
date: 2010-06-25T11:13:29+0000
lastmod: 2010-06-25T11:13:29+0000
slug: "cant-see-the-appfabric-directory-on-x64-systems"
aliases:
  - /cant-see-the-appfabric-directory-on-x64-systems/
---

This is one I have to jot down.

If you’re using tools like Reflector, or just want to open up any of the files in the c:\windows\system32\AppFabric directory, you’ll run into some issues – like, the tool that you’re using complaining that “can’t find c:\windows\system32\appfabric…”  errors.

On x64 systems, you need to replace the path with:

```
C:\Windows\SysNative\AppFabric
```

This is the FileSystem redirector virtual path as described here: [http://msdn.microsoft.com/en-us/library/aa384187%28VS.85%29.aspx](http://msdn.microsoft.com/en-us/library/aa384187%28VS.85%29.aspx "http://msdn.microsoft.com/en-us/library/aa384187%28VS.85%29.aspx")
