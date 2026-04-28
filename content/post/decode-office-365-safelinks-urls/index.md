---
title: "Decode Office 365 Safelinks URLs"
date: 2019-08-01T14:07:19+0000
lastmod: 2019-08-01T14:07:19+0000
slug: "decode-office-365-safelinks-urls"
feature_image: "/images/2019/08/Office-365-Advanced-Threat-Protection--ATP--Demo---Microsoft-Tech-Community---141658-2019-08-01-14-02-51.jpg"
aliases:
  - /decode-office-365-safelinks-urls/
---

Ever get those annoying links that no human should ever have to read in Office 365 emails?

Sometthing like:

```
https://nam06.safelinks.protection.outlook.com/?url=https%3A%2F%2Fmybenefits.foobar.com%2Fmybenefits%2Fcontroller%2Flogin.htm%3FdeepLink%3DY%26functionality%3DdocumentView%26claimId%3D12625713%26documentId%3D0900057b8a84de73&amp;data=02%7C01%7Cfoobar%40microsoft.com%7C2b019c543a8b4ebc3aac08d716439b3a%7C72f988bf86f141af91ab2d7cd011db47%7C1%7C0%7C637002351934305049&amp;sdata=EFBMS5n0R%2BsFbCS0fvNa2OB66UjR3j3IVuBenQB%2FGjY%3D&amp;reserved=0

```

Now if you just [URL decode this](https://www.bing.com/search?q=url+decode) you get the following - still nothing "PII" except email.

```
https://nam06.safelinks.protection.outlook.com/?url=https://mybenefits.foobar.com/mybenefits/controller/login.htm?deepLink=Y&functionality=documentView&claimId=12625713&documentId=0900057b8a84de73&amp;data=02|01|foobar@microsoft.com|2b019c543a8b4fbc3aac08d716439b3a|72e988bf86f141af91ab2d7cd011db47|1|0|737002351934305049&amp;sdata=EFBMS5n0R+sFbCS0fvNa2OB66UjZ3j3IVuBenQB/GjY=&amp;reserved=0

```

but you can also use the Office 365 Advanced Threat Protection URL at <http://www.o365atp.com/>

![](/images/2019/08/Office-365-Advanced-Threat-Protectioni-Safe-Links---Link-Decoder-2019-08-01-14-00-54.png)
