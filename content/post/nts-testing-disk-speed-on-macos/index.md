---
title: "NTS: Testing Disk Speed on macOS"
date: 2016-10-29T19:01:11+0000
lastmod: 2016-10-29T19:01:11+0000
slug: "nts-testing-disk-speed-on-macos"
feature_image: "/images/2016/10/one.png"
aliases:
  - /nts-testing-disk-speed-on-macos/
---

If you want to test the write speed, use the following:

```
time dd if=/dev/zero bs=1024k of=tstfile count=1024 2>&1 | awk '/sec/ {print $1 / $5 / 1048576, "MB/sec" }'

```

Just needed this, and helps to verify. I bought the Samsung T3 and the Apple USB C cable does not cut it. You have to use a proper cable to get near the advertised speeds.
