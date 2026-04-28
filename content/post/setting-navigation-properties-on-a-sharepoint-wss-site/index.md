---
title: "Setting Navigation properties on a SharePoint (WSS) Site…"
date: 2009-01-24T10:01:29+0000
lastmod: 2009-01-24T10:01:29+0000
slug: "setting-navigation-properties-on-a-sharepoint-wss-site"
aliases:
  - /setting-navigation-properties-on-a-sharepoint-wss-site/
---

Recently, I was going through setting up some sample navigation approaches for SharePoint.  The first step was in creating a bunch of Child Sites and some basic hierarchical structure. For that I used a great tool from [IDevFactory called SWAT](http://www.idevfactory.com/products/swat/default.aspx) just to create some empty Team Sites.

The one issue with that tool is it doesn’t allow setting a few options globally.

What I wanted was to have under the Navigation options to have the “Show Subsites” enabled.  In addition to a few other navigation settings.  Just as shown below:

[![image](https://msdnshared.blob.core.windows.net/media/TNBlogsFS/BlogFileStorage/blogs_msdn/scicoria/image_thumb_426E9479.png "image")](https://msdnshared.blob.core.windows.net/media/TNBlogsFS/BlogFileStorage/blogs_msdn/scicoria/image_078761B0.png)

To do that you need to access the AllProperties collection on the SPWeb object and add or update any existing entries.  What I came up with is the following:

```

```
   37 private static void SetNavigation(SPWeb childWeb)
```

```
   38 {
```

```
   39     if (childWeb.IsRootWeb == false)
```

```
   40     {
```

```
   41         SPNavigation spNav = childWeb.Navigation;
```

```
   42         childWeb.Navigation.UseShared = true;
```

```
   43         childWeb.Description = childWeb.Name + " description...";
```

```
   44 
```

```
   45         SetAllPropr(childWeb, "__IncludeSubSitesInNavigation", "True");
```

```
   46         SetAllPropr(childWeb, "__InheritCurrentNavigation", "False");
```

```
   47         SetAllPropr(childWeb, "__IncludePagesInNavigation", "False");
```

```
   48         SetAllPropr(childWeb, "__NavigationShowSiblings", "False");
```

```
   49         SetAllPropr(childWeb, "__NavigationOrderingMethod", "2");
```

```
   50     }
```

```
   51 }
```

```
   52 
```

```
   53 static void SetAllPropr(SPWeb web, string key, object value)
```

```
   54 {
```

```
   55 
```

```
   56     if (web.AllProperties.Contains(key))
```

```
   57         web.AllProperties.Remove(key);
```

```
   58 
```

```
   59     web.AllProperties.Add(key, value);
```

```
   60 }
```

```

The full standalone console project is located [here](http://cicoria.com/downloads/wss30/SetChildSiteNavigation.zip)
