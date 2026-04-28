---
title: "Know what Process is calling your SPClaimProvider"
date: 2011-06-06T02:54:36+0000
lastmod: 2011-06-06T02:54:36+0000
slug: "know-what-process-is-calling-your-spclaimprovider"
aliases:
  - /know-what-process-is-calling-your-spclaimprovider/
---

If you’re writing a custom SharePoint Claims Provider ([SPClaimProvider](http://msdn.microsoft.com/en-us/library/microsoft.sharepoint.administration.claims.spclaimprovider.aspx)) in order to augment claims, it’s important to also understand what process is executing your specific code path.  In the situation where you are making calls to a DB or service endpoint you will need to understand which process actually makes that call.

In situations when running in a Trusted Subsystem model, you’ll also need to [RunWithElevated](http://msdn.microsoft.com/en-us/library/microsoft.sharepoint.spsecurity.runwithelevatedprivileges.aspx) in order to have that code path execute in the context of the Windows Principal for that process.

The following table illustrates for the abstract members of the [SPClaimProvider](http://msdn.microsoft.com/en-us/library/microsoft.sharepoint.administration.claims.spclaimprovider.aspx) class when implemented and where they execute:

|  |  |  |  |
| --- | --- | --- | --- |
| Method / Property | Web App | SP STS | Timer, PS (Feature Activation Code) |
| FillClaimTypes | X |  | X |
| FillClaimValueTypes |  |  | X |
| FillClaimsForEntity |  | X |  |
| FillEntityTypes | X |  |  |
| FillHierarchy | X |  |  |
| FillResolve | X |  |  |
| FillResolve | X |  |  |
| FillSchema | X |  |  |
| FillSearch | X |  |  |
| Name | X | X | X |
| SupportsEntityInformation |  | X |  |
| SupportsHierarchy | X |  |  |
| SupportsResolve | X |  |  |
| SupportsSearch | X |  | X |

So, if you have your persistence in a SQL DB, and your using Windows Authentication (and using [RunWithElevated](http://msdn.microsoft.com/en-us/library/microsoft.sharepoint.spsecurity.runwithelevatedprivileges.aspx)) you’ll need to grant (or have) to the appropriate SQL permissions; generally, I’ve just granted “datareader”.
