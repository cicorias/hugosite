---
title: "Creating Wildcard Certificates with makecert.exe"
date: 2011-06-28T14:14:24+0000
lastmod: 2011-06-28T14:14:24+0000
slug: "creating-wildcard-certificates-with-makecert-exe"
aliases:
  - /creating-wildcard-certificates-with-makecert-exe/
---

Be nice to be able to make wildcard certificates for use in development with makecert – turns out, it’s real easy.  Just ensure that your CN=  is the wildcard string to use.

The following sequence generates a CA cert, then the public/private key pair for a wildcard certificate

```
REM make the CA
rem CA Certificate:
makecert -r -pe -n "CN=AA Contoso Test Root Authority" -ss CA -sr CurrentUser -a sha1 -sky signature -cy authority -sv CA.pvk CA.cer -len 2048

REM now make the server wildcard cert  

makecert -pe -n "CN=*.contosotest.com" -a sha1 -len 2048 -sky exchange -eku 1.3.6.1.5.5.7.3.1 -ic CA.cer -iv CA.pvk -sp "Microsoft RSA SChannel Cryptographic Provider" -sy 12 -sv wildcard.pvk wildcard.cer

pvk2pfx -pvk wildcard.pvk -spc wildcard.cer -pfx wildcard.pfx

```
