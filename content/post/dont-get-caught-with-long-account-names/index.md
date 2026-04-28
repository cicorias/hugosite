---
title: "Don’t get caught with long Account Names!!"
date: 2010-01-07T01:27:22+0000
lastmod: 2010-01-07T01:27:22+0000
slug: "dont-get-caught-with-long-account-names"
aliases:
  - /dont-get-caught-with-long-account-names/
---

This has bitten me a couple of times.

This error surfaced yesterday when running a scripted install with psconfig.exe – the error that appears in the log is:

> **LookupAccountName failed to get the SID for account <domain>\LONG AC NAME > 20 chars**

When setting up SharePoint, we usually have a bunch of service accounts that generally are setup by different teams that manage the Active Directory accounts – well, that’s how it should work, but that’s another story.

Many times organizations will have naming standards.  These naming standards, well, that’s up the the organization and frankly I don’t always agree with them given the ability to have containers in LDAP/AD, but that’s a long discussion.

Sometimes (actually many times) these standards generate long account names.  Can be 20+ characters or more.  The thing is, when you setup an account in AD, it will truncate the “samAccountName” attribute for the user object based upon the Distinguished Name of the account.  So, it usually chops off the end of the string.  I’m not quite sure what it does if if finds a collision with an existing samAccountName and if it has some algorithm to generate a unique on the fly version that doesn’t collide – not my problem…

So, what you just need to do is get the real samAccountName from AD and rerun your script, command, etc. with the corrected <domain>\samAccountName parameter and all is good!!
