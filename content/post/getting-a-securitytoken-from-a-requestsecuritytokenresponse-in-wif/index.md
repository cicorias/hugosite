---
title: "Getting a SecurityToken from a RequestSecurityTokenResponse in WIF"
date: 2012-03-22T10:23:04+0000
lastmod: 2012-03-22T10:23:04+0000
slug: "getting-a-securitytoken-from-a-requestsecuritytokenresponse-in-wif"
aliases:
  - /getting-a-securitytoken-from-a-requestsecuritytokenresponse-in-wif/
---

When you’re working with WIF and WSTrustChannelFactory when you call the Issue operation, you can also request that a RequestSecurityTokenResponse as an out parameter.

However, what can you do with that object?  Well, you could keep it around and use it for subsequent calls with the extension method CreateChannelWithIssuedToken – or can you?

```
public static T CreateChannelWithIssuedToken<T>(this ChannelFactory<T> factory, SecurityToken issuedToken);
```

As you can see from the method signature it takes a SecurityToken – but that’s not present on the RequestSecurityTokenResponse class.

However, you can through a little magic get a GenericXmlSecurityToken by means of the following set of extension methods below – just call

rstr.GetSecurityTokenFromResponse() – and you’ll get a GenericXmlSecurityToken as a return.

```
public static class TokenHelper
{

    /// <summary>
    /// Takes a RequestSecurityTokenResponse, pulls out the GenericXmlSecurityToken usable for further WS-Trust calls
    /// </summary>
    /// <param name="rstr"></param>
    /// <returns></returns>
    public static GenericXmlSecurityToken GetSecurityTokenFromResponse(this RequestSecurityTokenResponse rstr)
    {
        var lifeTime = rstr.Lifetime;
        var appliesTo = rstr.AppliesTo.Uri;
        var tokenXml = rstr.GetSerializedTokenFromResponse();
        var token = GetTokenFromSerializedToken(tokenXml, appliesTo, lifeTime);
        return token;
    }

    /// <summary>
    /// Provides a token as an XML string.
    /// </summary>
    /// <param name="rstr"></param>
    /// <returns></returns>
    public static string GetSerializedTokenFromResponse(this RequestSecurityTokenResponse rstr)
    {
        var serializedRst = new WSFederationSerializer().GetResponseAsString(rstr, new WSTrustSerializationContext());
        return serializedRst;
    }

    /// <summary>
    /// Turns the XML representation of the token back into a GenericXmlSecurityToken.
    /// </summary>
    /// <param name="tokenAsXmlString"></param>
    /// <param name="appliesTo"></param>
    /// <param name="lifetime"></param>
    /// <returns></returns>
    public static GenericXmlSecurityToken GetTokenFromSerializedToken(this string tokenAsXmlString, Uri appliesTo, Lifetime lifetime)
    {
        RequestSecurityTokenResponse rstr2 = new WSFederationSerializer().CreateResponse(
        new SignInResponseMessage(appliesTo, tokenAsXmlString),
        new WSTrustSerializationContext());
        return new GenericXmlSecurityToken(
            rstr2.RequestedSecurityToken.SecurityTokenXml,
            new BinarySecretSecurityToken(
                rstr2.RequestedProofToken.ProtectedKey.GetKeyBytes()),
            lifetime.Created.HasValue ? lifetime.Created.Value : DateTime.MinValue,
            lifetime.Expires.HasValue ? lifetime.Expires.Value : DateTime.MaxValue,
            rstr2.RequestedAttachedReference,
            rstr2.RequestedUnattachedReference,
            null);
    }

}
```
