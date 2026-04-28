---
title: "Office 365 SharePoint and PDF files…"
date: 2013-06-08T06:38:53+0000
lastmod: 2013-06-08T06:38:53+0000
slug: "office-365-sharepoint-and-pdf-files"
aliases:
  - /office-365-sharepoint-and-pdf-files/
---

Recently, O365 added some server side rendering of PDF files.  Problem is if you have PDF files and an anonymous site, if a user clicks the PDF link, it will then try to authenticate that users.  Which defeats the purpose of anonymous.

You’ll need to change the links as follows:

Append either to the following (1st opens in the server side PDF reader; 2nd downloads to the client to read.

?Web=1

?Web=0

to the end of the URL.
