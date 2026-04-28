---
title: "Issues with OneDrive for business and Document Cache–Don’t mix C2R and MSI installs"
date: 2014-09-24T06:36:00+0000
lastmod: 2014-09-24T06:36:00+0000
slug: "issues-with-onedrive-for-business-and-document-cachedont-mix-c2r-and-msi-installs"
aliases:
  - /issues-with-onedrive-for-business-and-document-cachedont-mix-c2r-and-msi-installs/
---

With the latest updates to Office, an issue that rears it’s ugly head if you’ve mixed both C2R and MSI installs of any Office product (2013).  That means Office, Visio, Project, SharePoint designer, and OneDrive for Business Sync Client.

If you get into this mess, try to uninstall all the C2R or MSI – then get them all consistent;

#1 – can’t mix click-to-run and MSI installs on the same machine:

If any are mixed, you need to uninstall.

To start fresh:

1. Run <http://support.microsoft.com/kb/2739501>

a. Both MSI then C2R

2. Run ROIScan to ensure nothing is left:

a. <http://gallery.technet.microsoft.com/office/68b80aba-130d-4ad4-aa45-832b1ee49602>

3. Once you’re all clean:

a. C2R

i. Use the <https://portal.office.com/OLS/MySoftware.aspx>

ii. SharePoint designer is under “Tools”

iii. Visio is there if your org has a license..

b. MSI

i. Get them all in FULL downloads from MSDN, or wherever you obtain your installs from

Finally, for MSI installs, run this post 9/14/14 update. http://support.microsoft.com/kb/2889931/en-us

# for internal, step #1 – in toolbox there is OffScrub
