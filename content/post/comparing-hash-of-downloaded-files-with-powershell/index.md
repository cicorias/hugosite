---
title: "Comparing Hash of downloaded Files with PowerShell"
date: 2014-04-17T22:54:24+0000
lastmod: 2014-04-17T22:54:24+0000
slug: "comparing-hash-of-downloaded-files-with-powershell"
aliases:
  - /comparing-hash-of-downloaded-files-with-powershell/
---

I can’t claim 99% of this – main credit to : [http://www.tinyint.com/index.php/2011/09/14/get-an-md5-or-sha1-checksum-with-powershell/](http://www.tinyint.com/index.php/2011/09/14/get-an-md5-or-sha1-checksum-with-powershell/ "http://www.tinyint.com/index.php/2011/09/14/get-an-md5-or-sha1-checksum-with-powershell/")

```
)

$fs = new-object System.IO.FileStream $File, “Open”, “Read”, “Read”;
$algo = [type]"System.Security.Cryptography.$Algorithm"
$crypto = $algo::Create()
$hash = [BitConverter]::ToString($crypto.ComputeHash($fs)).Replace("-", "")
$fs.Close()
return $hash

```
