---
title: "Are these 2 strings equal?"
date: 2011-01-07T08:03:18+0000
lastmod: 2011-01-07T08:03:18+0000
slug: "are-these-2-strings-equal"
aliases:
  - /are-these-2-strings-equal/
---

I spent way too many hours on this one. I was going through full configuration of ADFS v2 with WCF active client scenarios and using self generated certificates, had all things lined up perfectly.  Using the certificate snap in I just copied the thumbprint into the IdentityModel section (trusted issuers) in my service config.

```
var one = "‎ecb8fd950978d94ae21d4f073227fdc2718bdb96";
var two = "ecb8fd950978d94ae21d4f073227fdc2718bdb96";
```

What ended up is in the first, there’s a buried nonprintable series of characters (â€Ž – or E2 80 8E in 0x format).

2 lessons, turn on tracing sooner and don’t trust Copy & Paste – all the time.  I ended up creating a quick Issuer Name Registry class so I could debug and finally saw the issue.

```
namespace MyService
{
    public class IssuerValidator : ConfigurationBasedIssuerNameRegistry
    {

        public IssuerValidator() :base()
        {

        }

        public IssuerValidator(XmlNodeList xml) : base(xml) { }
        public override string GetIssuerName(System.IdentityModel.Tokens.SecurityToken securityToken)
        {
            X509SecurityToken token = securityToken as X509SecurityToken;
            if (token == null)
            {
                return "who cares";
            }
            else
            {
                return token.Certificate.Thumbprint;
            }
        }
    }
```

I do have a utility I wrote to navigate the cert store and emit the thumbprint to avoid these issues, I just didn’t have it available on my machine at the time.
