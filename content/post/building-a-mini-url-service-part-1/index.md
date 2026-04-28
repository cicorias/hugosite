---
title: "Building a Mini URL Service – Part 1"
date: 2009-05-04T10:23:00+0000
lastmod: 2009-05-04T10:23:00+0000
slug: "building-a-mini-url-service-part-1"
aliases:
  - /building-a-mini-url-service-part-1/
---

This set of posts is about a "Mini URL" service that I created initially to help provide a means to automate shortening of URL's for sending in emails to users in SharePoint. If you've used SharePoint and at times you need to send a link to a List or Document item one way is to "right-click" the item (whether it's a folder, list item, or document) then if it's IE choose "Copy Shortcut". You can then just past that into an email and send over to your recipient.

Recently, I also noticed that even the White House Tweets (<https://twitter.com/whitehouse> ) are using another well known URL shortening service. A quick look around and you'll see that there are quite a few out there now.

So, I stripped what I built into very basic ASP.NET Web Site and created a service that is now hosted at [GoDaddy](http://godaddy.com/) at [http://MyMiniUrl.net](http://myminiurl.net/). This intended as a pure demo project and the full SharePoint integration won't initially be made available until I work out some minor issues – mostly related to "packaging". But for now, I wanted to just document some of the initial steps, challenges, and work-around that I encountered building this along with some of the decisions (trade-offs) I made along the way.

The initial technical goals of the service are as follows:

1. Provide a very basic redirection service for short URL – i.e. <http://myminiurl.net/B>
2. Hosted on [IIS7](http://www.iis.net/)
3. Hosted on GoDaddy with their form of "Application/Domain" mapping – you'll see a minor challenge here later related to how Request.ApplicationPath, the tilde (“~”) don’t work as expected…
4. Provide Persistence tier independence through Provider model [<system.data/DbProviderFactories>](http://msdn.microsoft.com/en-us/library/system.data.common.dbproviderfactories.aspx)

   1. MS SQL
   2. MySQL
   3. Future ([SQL Lite](http://sqlite.phxsoftware.com/))
5. Pluggable [HttpModule](http://msdn.microsoft.com/en-us/library/zec9k340(VS.85).aspx) for incorporating into existing web sites

The SharePoint integration aspect, not yet provided here, is implemented as an ECB (Edit Control Block) menu option that allows immediate automated generation (or lookup if the URL has been shortened already) then presentation of a quick Application page that allows the user to specify an email or pick from People Picker to send out.

[![image](https://msdnshared.blob.core.windows.net/media/TNBlogsFS/BlogFileStorage/blogs_msdn/scicoria/WindowsLiveWriter/BuildingaMiniURLServicePart1_C6CB/image_thumb_1.png "image")](https://msdnshared.blob.core.windows.net/media/TNBlogsFS/BlogFileStorage/blogs_msdn/scicoria/WindowsLiveWriter/BuildingaMiniURLServicePart1_C6CB/image_4.png)

Again, I've not published that part of this yet until I address a few issues.

del.icio.us Tags: [SharePoint](http://del.icio.us/popular/SharePoint),[Development](http://del.icio.us/popular/Development)
