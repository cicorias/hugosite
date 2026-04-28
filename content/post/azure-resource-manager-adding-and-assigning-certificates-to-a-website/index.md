---
title: "Azure Resource Manager – Adding and Assigning Certificates to a Website"
date: 2015-01-31T06:30:55+0000
lastmod: 2015-01-31T06:30:55+0000
slug: "azure-resource-manager-adding-and-assigning-certificates-to-a-website"
aliases:
  - /azure-resource-manager-adding-and-assigning-certificates-to-a-website/
---

## Overview

This post is going to cover working with Azure Resource Manager using the REST interfaces [1] and specifically the “**Microsoft.Web/sites**” and “**Microsoft.Web/certificates**” providers.

You can review the list of Resource Providers by issuing an authenticated REST call to the Uri below, replacing {**subscriptionId**} with your tenant id.

[https://management.azure.com/subscriptions/{**subscriptionId**}/providers?api-version=2015-0101](https://management.azure.com/subscriptions/%7btenantId%7d/providers?api-version=2015-0101) [2]

For this sample, I’m going to make use of the Active Directory Authentication Library for .NET – primarily to make the REST calls for acquiring an Access Token [3]. You don’t have to use these libraries, but for this sample and to abbreviate the token dance with AAD, I’m using them.

It’s important to note that Certificates are now part of the Resource Group itself, and can be assigned to multiple web sites within that Resource Group.

## Basic Steps

The basic steps for adding a certificate and assigning it to an Azure Website are as follows.

> ***Note***: All of these preparation steps can be done via script or REST calls as well; this sample is just demonstrating certificate upload and assignment to an existing Azure Web Site that already has DNS names (custom) assigned to them. You will also incur additional charges for the custom domain and SSL as warned during the portal method – you will not see warnings via code. Please review pricing information to understand the impact.

### Preparation

1. Using an AAD credential that is part of the AAD Domain that the Resource Group is part of – for this example, I add a credential for the AAD user store.

2. Creation of an Application in the AAD Domain for the Resource Group

3. Assigning permissions to the credential for the Resource Group via RBAC

4. Have a Web site running already with custom DNS names already assigned; this will be in a Resource Group that is protected by Role Based Access Control (RBAC)

5. Creation of a SSL Certificate – for this I used ‘makecert.exe’ and created a wildcard certificate

### Uploading and Assigning Certificate

6. Make a call to the /certificates resource provider to ‘ADD (PUT)’ a new Certificate to the Resource Group

7. Make a call to the /sites resource provider to ‘Update (PUT)’ the assignment of the cer5iridate to the DNS name

And that’s it. So, for steps 1 – 5, let’s review some of the setup steps:

1. Adding an AAD Credential for this sample – since we’re going to use Username / Password authentication to acquire a token, I’ll need the Password. This will require an initial sign on. The easiest way to do this is once you create a user, just login via a private browser sessions with that credential to <https://portal.azure.com> or <https://manage.windowsazure.com>

2. Creation of an Application in your AAD domain – same one where the credential is.

> 1) Sign in to the Azure management portal <https://manage.windowsazure.com>.
>
> 2) Click on Active Directory in the left hand nav.
>
> 3) Click the directory tenant where you wish to register the sample application.
>
> 4) Click the Applications tab.
>
> 5) In the drawer, click Add.
>
> 6) Click "Add an application my organization is developing".
>
> 7) Enter a friendly name for the application, for example "AADDemoCertificates", select "Native Client Application", and click next.
>
> 8) For the sign-on URL, enter the base URL for the sample, you’ll need this for the sample later: <https://localhost:8080/login>
>
> After done, we need to retrieve the ClientID; for that app:
>
> 9) In the Azure portal, click configure
>
> 10) Retrieve the ClientID and save it

3. Next, in the “New Portal” - <https://portal.azure.com> we need to assign the user permissions to the respective Resource Group

> 1) Click Browse
>
> 2) Find “Resource Groups”
>
> 3) Locate the Resource Group that the Azure Web Site is in that we will be assigning the certificate to.
>
> 4) In the “Blade” go to the bottom tile labeled “Access” and click on “Owner”
>
> 5) Another blade opens showing any existing Owners
>
> 6) Click on “+ Add”
>
> 7) You should see existing Users in the domain; find the User or enter the ‘user@domain’ in the Search box
>
> 8) Select that user, then click “Select” at the bottom of the blade – this will add that user to the group

4. Looking at your Web site in Azure – ensure and jot down:

> a. Name of the Resource Group (should be same as above step)
>
> b. Name of the Site
>
> c. DNS names – add a custom DNS domain – see the Azure portal for instructions
>
> i. This is under “Custom Domains and SSL” – you have to choose a “Basic” plan or higher for Custom Domains and SSL

5. For making a self-signed cert, these are the commands I used:

```
REM make the root
makecert -n "CN=Development Test Authority" -cy authority -a sha1 -sv "DevelopmentTestAuthority.pvk" -r "DevelopmentTestAuthority.cer"

REM makecert -n "CN=*.cicoriadev.net" -ic "DevelopmentTestAuthority.cer" -iv "DevelopmentTestAuthority.pvk" -a sha1 -sky exchange -pe -sv "wildcard.cicoriadevnet.pvk" "wildcard.cicoriadevnet.cer"

makecert -n "CN=*.cicoriadev.net" -ic "DevelopmentTestAuthority.cer" -iv "DevelopmentTestAuthority.pvk" -a sha1 -sky exchange -pe -sv "wildcard.cicoriadevnet.pvk" "wildcard.cicoriadevnet.cer"

pvk2pfx -pvk "wildcard.cicoriadevnet.pvk" -spc "wildcard.cicoriadevnet.cer" -pfx "wildcard.cicoriadevnet.pfx" -pi pass@word1

```

## Sample Code

For the sample code, you’ll see a call via the AADL library to use a Username & Password for obtaining an AuthenticationResult object – which contains an AccessToken. Note that the resource URI that the token is generated for is <https://management.azure.com/> .

### Adding a Certificate via REST

The sample code makes use of JSON.NET and anonymous objects for creating the PUT HTTP request bodies. Here is what the shape of the PUT request looks like for ‘adding’ a certificate to a Resource Group.

#### Request

```
PUT https://management.azure.com/subscriptions/{subscriptionId}/
   resourceGroups/{resourceGroupName/providers/
   Microsoft.Web/certificates/{resourceName}?api-version=2014-11-01

Content-Type: application/json  

Authorization: Bearer {accessToken}  

Content-Length: 3675

{  

"name": "{resourceName}",  

"type": "Microsoft.Web/certificates",  

"location": "{location}",  

"properties" : {  

"pfxBlob": {base64ByteArrayOfPfx},  

"password": "pass@word1"  

}  

}

```

### Replacement Parameters

**subscriptionId** – this is the subscription that the Resource Group (and it’s web site) is contained within

**resourceGroupName** – this is the name of the resource group

**resourceName** – this is what the friendly name of the certificate WILL be – this is a PUT request, but the resourceName must be on the Uri in addition to the json request body – and they must match

**accessToken** – this is the token obtained from the AADL library call

**location** – for my sample, I used “East US” – which is the Azure Region. Note that not all Resource Providers are available or registered for your subscription in all regions. Review the response from the /providers REST call prior in this post to see what is available for each region, along with the ‘api-version’ that is supported.

**base64ByteArrayOfPfx** – this the pfx file in bytes, then converted to base64

**password**- this is the password of the pfx file that was used during pfx creation

#### Response

The HTTP Response code is a 200 – this a content body that dumps out the certificate information. I’ve abbreviated most of the response in the following. Make note of the thumbprint if you haven’t already as this is what the assignment will use, along with the Site name, to bind the SSL certificate to the web site.

```
{
    "id": "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Web/certificates/{resourceName}",
    "name": "{resourceName}",
    "type": "Microsoft.Web/certificates",
    "location": "{location}",
    "properties": {
        "friendlyName": "",
        "subjectName": "*.cicoriadev.net",
        "hostNames": [
            "*.cicoriadev.net"
        ],
        "pfxBlob": null,
        "siteName": null,
        "selfLink": null,
        "issuer": "Development Test Authority",
        "issueDate": "2015-01-27T22:34:57+00:00",
        "expirationDate": "2039-12-31T23:59:59+00:00",
        "thumbprint": "DEA5DED6142EDECCDF952F4D431ED772F01D22D1",
    }
}

```

## Assigning a Certificate via REST

For the assignment, we make use of the Resource Manager “Microsoft.Web/sites”.

### Request

```
PUT https://management.azure.com/subscriptions/{subscriptionId}/
   resourceGroups/{resourceGroupName/providers/
   Microsoft.Web/sites/{resourceName}?api-version=2014-11-01

Content-Type: application/json  

Authorization: Bearer {accessToken}  

Content-Length: 567

{  

"name": "{resourceName}",  

"type": "Microsoft.Web/sites",  

"location": "{location}",  

"properties" : {  

"hostNameSslStates": [  

{  

"name": "azw.cicoriadev.net",  

"sslState": 1,  

"thumbprint": "DEA5DED6142EDECCDF952F4D431ED772F01D22D1",  

"toUpdate": 1,  

}  

]  

}  

}

```

### Replacement Parameters

**subscriptionId** – this is the subscription that the Resource Group (and it’s web site) is contained within

**resourceGroupName** – this is the name of the resource group

**resourceName** – this is what the friendly name of the certificate WILL be – this is a PUT request, but the resourceName must be on the Uri in addition to the json request body – and they must match

**accessToken** – this is the token obtained from the AADL library call

**location** – for my sample, I used “East US” – which is the Azure Region. Note that not all Resource Providers are available or registered for your subscription in all regions. Review the response from the /providers REST call prior in this post to see what is available for each region, along with the ‘api-version’ that is supported.

**Thumbprint** – this would be the thumbprint known for that certificate in Azure – again, it should always be the same locally, but if you have any issues assigning, this must match what Azure knows in /certificates.

### Response

The Response should show you the chosen site DNS name with the thumbprint associated, similar to the following:

```
        "hostNameSslStates": [
            {
                "name": "azw.cicoriadev.net",
                "sslState": 1,
                "ipBasedSslResult": null,
                "virtualIP": null,
                "thumbprint": "DEA5DED6142EDECCDF952F4D431ED772F01D22D1",
                "toUpdate": null,
                "toUpdateIpBasedSsl": null,
                "ipBasedSslState": 0,
                "hostType": 0
            },

```

## Sample Solution and Source Code

The source code is located on github: <http://bit.ly/azrmsamples> - or direct <https://github.com/cicorias/AzureResourceManagerSamples>

[1] Azure Resource Manager REST API Reference <https://msdn.microsoft.com/en-us/library/azure/dn790568.aspx>

[2] Listing All Resource Providers <https://msdn.microsoft.com/en-us/library/azure/dn790524.aspx>

[3] Active Directory Authentication Library for .NET – github <https://github.com/AzureAD/azure-activedirectory-library-for-dotnet>
