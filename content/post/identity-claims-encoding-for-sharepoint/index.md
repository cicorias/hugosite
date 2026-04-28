---
title: "Identity Claims Encoding for SharePoint"
date: 2011-06-30T03:50:59+0000
lastmod: 2011-06-30T03:50:59+0000
slug: "identity-claims-encoding-for-sharepoint"
aliases:
  - /identity-claims-encoding-for-sharepoint/
---

Just to remind myself, the list of claim types and their encodings are listed here at the bottom.

[http://msdn.microsoft.com/en-us/library/gg481769.aspx](http://msdn.microsoft.com/en-us/library/gg481769.aspx "http://msdn.microsoft.com/en-us/library/gg481769.aspx")

Where for example:

i:0#.w|contoso\scicoria

‘i’ = identity, could be ‘c’ for others

# == SPClaimTypes.UserLogonName

. == Microsoft.IdentityModel.Claims.ClaimValueTypes.String

Table for reference:

Table 1. Claim types encoding

| Character | Claim Type |
| --- | --- |
| ! | SPClaimTypes.IdentityProvider |
| ” | SPClaimTypes.UserIdentifier |
| # | SPClaimTypes.UserLogonName |
| $ | SPClaimTypes.DistributionListClaimType |
| % | SPClaimTypes.FarmId |
| & | SPClaimTypes.ProcessIdentitySID |
| ‘ | SPClaimTypes.ProcessIdentityLogonName |
| ( | SPClaimTypes.IsAuthenticated |
| ) | Microsoft.IdentityModel.Claims.ClaimTypes.PrimarySid |
| \* | Microsoft.IdentityModel.Claims.ClaimTypes.PrimaryGroupSid |
| + | Microsoft.IdentityModel.Claims.ClaimTypes.GroupSid |
| - | Microsoft.IdentityModel.Claims.ClaimTypes.Role |
| . | System.IdentityModel.Claims.ClaimTypes.Anonymous |
| / | System.IdentityModel.Claims.ClaimTypes.Authentication |
| 0 | System.IdentityModel.Claims.ClaimTypes.AuthorizationDecision |
| 1 | System.IdentityModel.Claims.ClaimTypes.Country |
| 2 | System.IdentityModel.Claims.ClaimTypes.DateOfBirth |
| 3 | System.IdentityModel.Claims.ClaimTypes.DenyOnlySid |
| 4 | System.IdentityModel.Claims.ClaimTypes.Dns |
| 5 | System.IdentityModel.Claims.ClaimTypes.Email |
| 6 | System.IdentityModel.Claims.ClaimTypes.Gender |
| 7 | System.IdentityModel.Claims.ClaimTypes.GivenName |
| 8 | System.IdentityModel.Claims.ClaimTypes.Hash |
| 9 | System.IdentityModel.Claims.ClaimTypes.HomePhone |
| < | System.IdentityModel.Claims.ClaimTypes.Locality |
| = | System.IdentityModel.Claims.ClaimTypes.MobilePhone |
| > | System.IdentityModel.Claims.ClaimTypes.Name |
| ? | System.IdentityModel.Claims.ClaimTypes.NameIdentifier |
| @ | System.IdentityModel.Claims.ClaimTypes.OtherPhone |
| [ | System.IdentityModel.Claims.ClaimTypes.PostalCode |
| \ | System.IdentityModel.Claims.ClaimTypes.PPID |
| ] | System.IdentityModel.Claims.ClaimTypes.Rsa |
| ^ | System.IdentityModel.Claims.ClaimTypes.Sid |
| \_ | System.IdentityModel.Claims.ClaimTypes.Spn |
| ` | System.IdentityModel.Claims.ClaimTypes.StateOrProvince |
| a | System.IdentityModel.Claims.ClaimTypes.StreetAddress |
| b | System.IdentityModel.Claims.ClaimTypes.Surname |
| c | System.IdentityModel.Claims.ClaimTypes.System |
| d | System.IdentityModel.Claims.ClaimTypes.Thumbprint |
| e | System.IdentityModel.Claims.ClaimTypes.Upn |
| f | System.IdentityModel.Claims.ClaimTypes.Uri |
| g | System.IdentityModel.Claims.ClaimTypes.Webpage |

### Table 2. Claim value types encoding

|  |  |
| --- | --- |
| **Character** | **Claim Type** |
| ! | Microsoft.IdentityModel.Claims.ClaimValueTypes.Base64Binary |
| “ | Microsoft.IdentityModel.Claims.ClaimValueTypes.Boolean |
| # | Microsoft.IdentityModel.Claims.ClaimValueTypes.Date |
| $ | Microsoft.IdentityModel.Claims.ClaimValueTypes.Datetime |
| % | Microsoft.IdentityModel.Claims.ClaimValueTypes.DaytimeDuration |
| & | Microsoft.IdentityModel.Claims.ClaimValueTypes.Double |
| ‘ | Microsoft.IdentityModel.Claims.ClaimValueTypes.DsaKeyValue |
| ( | Microsoft.IdentityModel.Claims.ClaimValueTypes.HexBinary |
| ) | Microsoft.IdentityModel.Claims.ClaimValueTypes.Integer |
| \* | Microsoft.IdentityModel.Claims.ClaimValueTypes.KeyInfo |
| + | Microsoft.IdentityModel.Claims.ClaimValueTypes.Rfc822Name |
| - | Microsoft.IdentityModel.Claims.ClaimValueTypes.RsaKeyValue |
| . | Microsoft.IdentityModel.Claims.ClaimValueTypes.String |
| / | Microsoft.IdentityModel.Claims.ClaimValueTypes.Time |
| 0 | Microsoft.IdentityModel.Claims.ClaimValueTypes.X500Name |
| 1 | Microsoft.IdentityModel.Claims.ClaimValueTypes.YearMonthDuration |
