---
title: "Cheap and easy IP blocking in Azure Web Apps"
date: 2015-07-01T11:07:42+0000
lastmod: 2015-07-01T11:07:42+0000
slug: "cheap-and-easy-ip-blocking-in-azure-web-apps"
aliases:
  - /cheap-and-easy-ip-blocking-in-azure-web-apps/
---

Sometimes you just need to resort to something simple.

I don’t recommend this in anyway for a real security plan / hardening. You should be using something proper if you’re under these kinds of malicious attacks.

But, in Azure Web Apps you can add IP Address blocking via the IIS “Dynamic IP Restrictions” Module [[1](http://www.iis.net/downloads/microsoft/dynamic-ip-restrictions)].

**While I think this is the “wrong” way to do this** (a real firewall should be in place), I was able to “block” IP addresses in Azure Web Apps (site) by using an **applicationHost.xdt** transform like so:

This becomes a “site” extension – and is deployed as a Site Extension <https://github.com/projectkudu/kudu/wiki/Azure-Site-Extensions>

This modifies the **applicationHost.config** for your Web App. <https://azure.microsoft.com/en-us/documentation/articles/web-sites-transform-extend/>

```
<?xml version="1.0"?>
<configuration xmlns:xdt="http://schemas.microsoft.com/XML-Document-Transform">
  <system.webServer>
    <security>
      <ipSecurity allowUnlisted="true" xdt:Transform="Replace">
         <add  ipAddress="191.237.6.194"/>
      </ipSecurity>
    </security>
  </system.webServer>
</configuration>
```

[1] [http://www.iis.net/downloads/microsoft/dynamic-ip-restrictions](http://www.iis.net/downloads/microsoft/dynamic-ip-restrictions "http://www.iis.net/downloads/microsoft/dynamic-ip-restrictions")
