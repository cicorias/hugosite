---
title: "AppFabric – where are all the monitoring events?"
date: 2010-06-10T10:28:37+0000
lastmod: 2010-06-10T10:28:37+0000
slug: "appfabric-where-are-all-the-monitoring-events"
aliases:
  - /appfabric-where-are-all-the-monitoring-events/
---

When you’ve just gone through a setup of AppFabric and you’ve got some WF/WCF things happening, if you start looking at the Dashboard and you see nothing, it might be as simple as restarting SQL Agent.

I generally don’t reboot my system for several days and after installing AppFabric the SQL Agent jobs didn’t start firing right away.  Yes, even running a boot to VHD, you can still put the machine to sleep (just logoff and click on Sleep)…

So, after spending time looking through the SQL monitoring DB that AppFabric was configured to use, I saw a bunch of records in the [AppFabric\_Monitoring].[dbo].[ASStagingTable] table.  This table is the stopping point before the SQL Agent job (or Service Broker in SQL Express) pushes the items to their final resting place.

This post goes through a few things to check on AppFabric monitoring

[http://social.technet.microsoft.com/wiki/contents/articles/appfabric-items-to-check-when-configuring-appfabric-monitoring.aspx](http://social.technet.microsoft.com/wiki/contents/articles/appfabric-items-to-check-when-configuring-appfabric-monitoring.aspx "http://social.technet.microsoft.com/wiki/contents/articles/appfabric-items-to-check-when-configuring-appfabric-monitoring.aspx")

Of course, during development you might want to clean up regularly

For that there’s the PowerShell command

Clear-AsMonitoringSqlDatabase -Database AppFabric\_Monitoring
