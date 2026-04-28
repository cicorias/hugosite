---
title: "Fixing CocoaPods bad Dependancies"
date: 2016-08-17T12:00:25+0000
lastmod: 2016-08-17T12:00:25+0000
slug: "fixing-cocoapods-bad-dependancies"
feature_image: "/images/2016/08/CocoaPods-black-on-white1-r-w600-h400-q75-m1424447116.png"
aliases:
  - /fixing-cocoapods-bad-dependancies/
---

For some reason my CocoaPods was working just fine - until this morning. ...

So, this seems to cleanup and freshen real nice...

```
pod repo remove master
pod setup
pod install

```

Thanks to this Stack Overflow thread...  
<http://stackoverflow.com/questions/23006683/cocoapods-staying-on-analyzing-dependencies>
