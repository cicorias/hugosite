---
title: "Building a Mini URL Service – Part 2 – The Algorithm"
date: 2009-05-05T04:22:00+0000
lastmod: 2009-05-05T04:22:00+0000
slug: "building-a-mini-url-service-part-2-the-algorithm"
aliases:
  - /building-a-mini-url-service-part-2-the-algorithm/
---

[Part 1](http://cicoria.com/CS1/blogs/cedarlogic/archive/2009/05/04/building-a-mini-url-service-part-1.aspx) – Part 2

The first order of business is what URL shortening approach should be used to take some very long URL, which in IE7 is limited to 2,083 characters ([KB208427](http://support.microsoft.com/kb/208427)) and provide a nice compact link.

The first part of the link (protocol + server + port) is generally controlled by what domain name you can get – for me, my little demo is <http://MyMiniUrl.net>. The rest of the URL – the path is something in your control.

Doing a search I came across a few approaches but settled on a [Base 62](http://en.wikipedia.org/wiki/Base_62) approach that uses a sequence generation maintained in the persistence tier. The idea is to generate a unique sequential number, then convert that numeric to a Base 62 representation. For the sequence generation, I just relied on the DB layer (MySql or MS SQL) to generate this from an identity column.

Once that identity value is generated, it gets run through a Base 62 conversion to a string representation. That string along with the identity (from the DB), the full Long URL, and a cryptographic hash of the Long URL is stored in the DB. The basic DB table schema is as follows (for MySQL):

|  |  |  |
| --- | --- | --- |
| Column | Type | Description |
| urlId | Bigint(20) | Identity column |
| miniUrl | Char(12) | Shortened “path” of the URL |
| fullUrlHash | Char(32) | Crypto hash of Full URL using MD5 |
| fullUrl | Varchar(4096) | Full URL provided |

The indices are as follows:

- Primary – index on urlID
- fullUrlHash – Unique index
- miniUrl – I left this as “not unique” given my persistence pattern starts off with this value as null.

So, when the URL service is asked to create a short URL, it first checks to see if the URL was already generated. To do that the UrlService uses the basic pattern:

1. Checks the URL pattern to a matching regular expression (in the config file)
2. Generates a MD5 hash of the full URL
3. Checks to see if the hash already exists doing a SQL lookup on the hashed value of the full URL
   1. If exists, just return the existing shortened URL
   2. If doesn’t exist
      1. Insert new Long URL, Hash of URL
      2. Get new identity key
      3. Convert new identity key to Base 62
      4. Return short URL using Base 62 representation

Now, for the Base 62 algorithm, I looked around at a few approaches, and [Chris](http://www.shrinkrays.net/About.aspx) had a good post on various approaches as well – [Friendly Unique Id generation](http://www.shrinkrays.net/articles/friendly-unique-id-generation/part-2.aspx).

Starting with his code, I also found another approach located [here](http://javaconfessions.com/2008/09/convert-between-base-10-and-base-62-in_28.html), then finalized on the following:

```
while (fromValue != 0)
{
    mod = (int)(fromValue % baseNum); //should be safe
    toValue = baseDigits.Substring(mod, 1) + toValue;
    fromValue = fromValue / baseNum;
}

return toValue;

```

The basic approach is to loop through the source value, grab the remainder, convert that remainder to Base 62 and append it to a string return value, until there’s nothing left.

So, in terms of “string” vs. StringBuilder performance, I also tried using StringBuilder in place of string concatenation, but performance, in a loop of a billion iterations was far better (about 60%) just with simple string concatenation. Now, I’m not too concerned with garbage collection at this point, I just wanted something quick and efficient – and in the end correct.
