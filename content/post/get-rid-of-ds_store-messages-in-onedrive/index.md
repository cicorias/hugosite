---
title: "Get rid of .DS_Store messages in OneDrive"
date: 2019-04-30T16:17:38+0000
lastmod: 2019-04-30T16:17:38+0000
slug: "get-rid-of-ds_store-messages-in-onedrive"
feature_image: "/images/2019/04/ca00213e-0be3-4256-9088-144edc6d2ff4-squashed.png"
aliases:
  - /get-rid-of-ds_store-messages-in-onedrive/
---

For some odd reason, actually not odd, just another annoyance. OneDrive starts complaining about the DS\_Store files.

doh.

```
find /users/username/onedrivepath/ -name ".DS_Store" -depth -exec rm {} \;

```
