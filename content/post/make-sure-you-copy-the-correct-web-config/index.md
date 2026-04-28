---
title: "Make sure you copy the correct web.config…"
date: 2009-12-16T03:58:45+0000
lastmod: 2009-12-16T03:58:45+0000
slug: "make-sure-you-copy-the-correct-web-config"
aliases:
  - /make-sure-you-copy-the-correct-web-config/
---

During an installation issue, a client followed the TechNet article ([http://technet.microsoft.com/en-us/library/cc298447.aspx](http://technet.microsoft.com/en-us/library/cc298447.aspx "http://technet.microsoft.com/en-us/library/cc298447.aspx")) and those instructions are misleading.

It indicates to copy the “web.config” to the Layouts directory – what if fails to specify is it should be the “layoutsweb.config” file instead.

While following the article does get you passed the issue that brought you there in the first place, you eventually end up with issues on provisioned sites that reference anything in \_layouts are there are sections “<system.web>” that don’t make sense in a IIS path.

Just recopying that correct config file fixes all.
