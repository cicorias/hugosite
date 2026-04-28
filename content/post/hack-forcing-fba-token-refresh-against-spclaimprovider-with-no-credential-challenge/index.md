---
title: "HACK: Forcing FBA Token Refresh against SPClaimProvider with No Credential Challenge"
date: 2011-06-15T09:48:33+0000
lastmod: 2011-06-15T09:48:33+0000
slug: "hack-forcing-fba-token-refresh-against-spclaimprovider-with-no-credential-challenge"
aliases:
  - /hack-forcing-fba-token-refresh-against-spclaimprovider-with-no-credential-challenge/
---

The approach takes advantage of the SP 2010 OOB Session Token handler and FBA claims provider implementation that during a period of token lifetime, if there is activity during the period of time that can be defined as "EW" in the image in the section "Background" below, that the **SPSecurityTokenManager** will, with the FBA provider, reissue a Session Token with new SessionToken **ValidTo** and **ValidFrom** times without forcing a re-challenge for user credentials (username and password).

Additionally, it takes advantage of the ability to provide an event handler, on the **SessionAuthentcationModule** (**SPSessionAuthenticationModule**) to cause a reissue of the token temporarily with an expiry time (**ValidTo**) that will cause a **SPSessionToken** cache miss – thus forcing the re-issue by the **SPSecurityTokenManager**.

**General Approach**

The following is a contrived example and uses a rudimentary approach for determine how/when to indicate that the token should be "refreshed" This is done by hooking into the WIF Session Authentication Module's (SAM) Event "**SessionSecurityTokenReceived**".

The approach taken, and shown on the internet in several posts is to subclass the **HttpApplication** implementation.

The approach I recommend is to leverage the ability of any **HttpApplication** by ways of built in ability to identify all **HttpModules** loaded for that ASP.NET application (SP included) and determine if there are Event handlers specified by ways of the **Global.asax** in the Root of the SP IIS Site. This is handled by the **System.Web.HttpApplication.HookupEventHandlersForApplicationAndModules** method.

**Note:** There are alternatives that I've also tested that work – 1 approach is to register a new **HttpModule**, then in that **HttpModule** is to register "1" time a handler for the SAM's **SessionSecurityTokenReceived** event. This requires a method of indicating at the application level that a handler has already been registered.

**Scenario Supported**

The general scenario is:

1. User is already logged onto the site with a valid token
2. At time required to force a Claims refresh, user will click a link or system will determine how to initiate an **HttpRequest** that will call the logic required for forcing the refresh
3. System receives request
4. **SessionAuthenticationModule** raises event that custom code will handle

   1. **This is done by HttpRequest inspection – the sample looks for a Url that contains "RefreshToken.aspx" – there are other means to provide a similar approach.**
5. Custom code identifies the SP **LogonTokenCacheExpirationWindow**
6. Using **LogonTokenCacheExpirationWindow**, custom code forces a re-issue of token that has a **ValidTo** that will fall into the **LogonTokenCacheExpirationWindows** – eg.

```
DateTime newValidTo = DateTime.UtcNow.Add(logonWindow); 
```

1. System (SP Session Cache) determines that the token requires a re-issue
2. System calls **SPSecurityToken** Manager – to reissue all claims for user, bypassing the Logon credentials prompt
3. During the **SPSecurityToken** manager re-issue any custom **SPClaimProvider** types loaded are also called – using FBA and **SPClaimProvider** will make a call to its **FillClaimsForEntity** inside of the SP STS.
4. Session continues with new **SessionToken** using configuration based values for **ValidFrom**, **ValidTo** as defined in the **SPSecurityTokenConfig**.

**Sample Code for Event Handler**

The sample code uses another class to contain the code; your implementation could just as easily keep this in the **global.asax** – however, I'm of the belief that the **global.asax** should be kept as pristine as possible.

The following code is placed in an assembly that is resolvable through normal fusion – that is, it could be a private assembly. I've chosen GAC in the sample project just for the ease of development.

The code below handles the event and just looks for a page (Url) that contains a well-known request string. This could be anything, but ensure that it's not a common page and based upon the application needs, how your logic will determine a need to refresh all claims.

```
<%@ Assembly Name="Microsoft.SharePoint" %>
<%@ Assembly Name="RefreshClaimsSample, Version=1.0.0.0, Culture=neutral, PublicKeyToken=329ca2a6e4eeb8c6" %>
<%@ Application Language="C#" Inherits="Microsoft.SharePoint.ApplicationRuntime.SPHttpApplication" %>
<%@ Import Namespace="Microsoft.IdentityModel.Web" %>
<%@ Import Namespace="Microsoft.IdentityModel.Tokens" %>
<%@ Import Namespace="Microsoft.SharePoint.IdentityModel" %>

<script runat="server">
    void SessionAuthentication_SessionSecurityTokenReceived(object sender, SessionSecurityTokenReceivedEventArgs e) 
    {
        RefreshClaimsSample.SampleRefreshClaims.ForceRefreshClaims(sender, e);
    }
</script>
```
```
public static void ForceRefreshClaims(object sender, SessionSecurityTokenReceivedEventArgs e)
{
    if (HttpContext.Current.Request.Url.AbsoluteUri.Contains("RefreshClaims.aspx"))
    {
        SessionAuthenticationModule sam = sender as SessionAuthenticationModule;
        var logonWindow = SPSecurityTokenServiceManager.Local.LogonTokenCacheExpirationWindow;

        DateTime newValidTo = DateTime.UtcNow.Add(logonWindow);

        e.SessionToken = sam.CreateSessionSecurityToken(
            e.SessionToken.ClaimsPrincipal,
            e.SessionToken.Context,
            e.SessionToken.ValidFrom,
            newValidTo,
            e.SessionToken.IsPersistent);

        e.ReissueCookie = true;
    }
}
```

**Wiring up Event Handler**

In the SP **Global.asax** provided a method signature that matches the event from the SAM.

The requirements are that the signature is as follows:

**void <*moduleNameFromConfig*>\_<*eventName*> ( *eventArgsType* )**

Where:

1. moduleNameFromConfig – must match the name attribute from the module as specified in the [/system.webServer/modules/add/@name](mailto:/system.webServer/modules/add/@name) element.
2. eventName – must match the event name as defined in the HttpModule's public event
3. eventArgsType – must match the event arguments type that is defined for the event.

[![SNAGHTML7380ba9](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/6507.SNAGHTML7380ba9_thumb_636E297B.png "SNAGHTML7380ba9")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/6102.SNAGHTML7380ba9_2C744B42.png)

**Background**

[![image](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/7026.image_thumb_47E92778.png "image")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/3465.image_4F7496E5.png)

In the above diagram, the settings:

- TL = FormsTokenLifeTime
- EW = LogonTokenCacheExpirationWindow

These settings are obtained and modified via PowerShell under the SPSecurityT0kenServiceConfig set of cmdlets.

For the following samples, assume the following:

- TL = 10 Minutes
- EW = 4 Minutes

TL – EW = 6 Minutes

[Solution Zip](http://cicoria.com/downloads/RefreshClaimsSln.zip)
