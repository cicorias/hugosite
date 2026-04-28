---
title: "No, your local admin account is NOT a SQL sysadmin – automatically"
date: 2010-01-25T02:36:13+0000
lastmod: 2010-01-25T02:36:13+0000
slug: "no-your-local-admin-account-is-not-a-sql-sysadmin-automatically"
aliases:
  - /no-your-local-admin-account-is-not-a-sql-sysadmin-automatically/
---

There have been many times that I’ve been handed a SQL instance that doesn’t allow me to do much with it even though the IT Admin for the machine have indicated they’ve done the install and your AD account is part of the Local Admin group.

By default, in SQL 2008 local admin’s are not part of the sysadmin role – unless you’re running in single user mode.

So, this article has a quick HOWTO on getting access back so you can go on your merry sysadmin way…

[http://technet.microsoft.com/en-us/library/dd207004.aspx](http://technet.microsoft.com/en-us/library/dd207004.aspx "http://technet.microsoft.com/en-us/library/dd207004.aspx")

The trick is, restart with the “-m;” parameter, make the change, the change it back (don’t forget that part).  Also, make sure all the other services aren’t running when you need to make this change, otherwise, they connect as THE single user.
