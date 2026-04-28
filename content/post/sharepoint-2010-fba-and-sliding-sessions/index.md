---
title: "SharePoint 2010 FBA and Sliding Sessions"
date: 2011-06-10T09:41:28+0000
lastmod: 2011-06-10T09:41:28+0000
slug: "sharepoint-2010-fba-and-sliding-sessions"
aliases:
  - /sharepoint-2010-fba-and-sliding-sessions/
---

This is to provide a little bit of explanation on the implementation of FBA authentication with SP 2010. There have been blog posts that indicate there are no sliding sessions, but with a little manipulation and understanding of some of the settings, there is somewhat of support for sliding sessions and re-issuance of tokens. The current model provides for a little trade-off on performance as re-requests to the FBA providers and also any SP Custom Claim providers can have impact on overall performance.

The following diagram represents the initial static view of the SP 2010 Security Token Service Configuration settings that control the management of Tokens issued under Forms Based Authentication (FBA) authentication.

The current SP 2010 April 2011 CU’s does support a level of sliding sessions as long as a request (user activity) occurs in the window of time after token issuance (logon or re-issuance) defined in the “EW” segment below.

[![image](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/3806.image_thumb_18F27D4E.png "image")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/5531.image_3ABE55DF.png)

In the above diagram, the settings:

- TL = FormsTokenLifeTime
- EW = LogonTokenCacheExpirationWindow

These settings are obtained and modified via PowerShell under the SPSecurityT0kenServiceConfig set of cmdlets.

For the following samples, assume the following:

- TL = 10 Minutes
- EW = 4 Minutes
- TL – EW = 6 Minutes

Example 1:

1. User Logon occurs
2. User is Inactive for 11 minutes (> 10 minutes)
3. At next request: System Presents Forms based logon (or identity selector) to user forcing re-authentication **(All Claims Providers Called)**

Example 2:

1. User Logon occurs
2. User is Inactive for 3 minutes
3. User issues Request
4. Token is NOT updated as request occurred in the “TL – EW” window
5. User remains Inactive for 8 more minutes (> 7 or more than 3 + 7 = 10, which is the original window
6. At next request: System Presents Forms based logon (or identity selector) to user forcing re-authentication **(All Claims Providers Called)**

Example 3:

1. User Logon occurs
2. User is inactive for 8 minutes
3. User issues Request
4. System attempts to re-issue token, skipping password check
5. System re-issues new Token with updated ValidFrom / ValidTo timestamp based upon current clock **(All Claims Providers Called)**
6. Entire “window” is now shifted based upon existing configured values

Note in the above scenarios that the **“(All Claims Providers Called)”** indicates that the Claims Providers registered for the Web Application / Site are then called; any custom SPClaimProvider implementations will have the method FillClaimsForEntity called at that time
