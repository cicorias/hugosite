---
title: "Wildcard Certificates and IIS7"
date: 2009-12-23T08:29:30+0000
lastmod: 2009-12-23T08:29:30+0000
slug: "wildcard-certificates-and-iis7"
aliases:
  - /wildcard-certificates-and-iis7/
---

Let’s face it, during development, managing all the certificates if you’re doing anything with validating SSL/TLS traffic is a pain.

Now with Windows Identity Foundation (fka Geneva) we really have to get crackin on getting used to managing certificates, setting up SSL sites, etc.

So, here’s great post on setting up IIS7 to use wildcard certificates…

[http://blog.mikeobrien.net/PermaLink,guid,12d9628c-a350-4f7b-a573-9d05429b54e8.aspx](http://blog.mikeobrien.net/PermaLink,guid,12d9628c-a350-4f7b-a573-9d05429b54e8.aspx "http://blog.mikeobrien.net/PermaLink,guid,12d9628c-a350-4f7b-a573-9d05429b54e8.aspx")

This gives you 1 certificate rooted at some common domain (eg.    mydev.local) where all sites would be site1.mydev.local, site2.mydev.local, etc.  The CN in the certificate ends up being \*.mydev.local – just wire up in your hosts file (..\drivers\etc\hosts) and you’re golden…
