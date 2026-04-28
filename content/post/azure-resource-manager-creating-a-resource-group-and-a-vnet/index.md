---
title: "Azure Resource Manager– Creating a Resource Group and a VNET"
date: 2015-02-09T08:48:23+0000
lastmod: 2015-02-09T08:48:23+0000
slug: "azure-resource-manager-creating-a-resource-group-and-a-vnet"
aliases:
  - /azure-resource-manager-creating-a-resource-group-and-a-vnet/
---

**NOTE:** Azure Resource manager is in Preview. Thus, anything posted here may change. However, the approach for identifying what resources are available updatable, and registered for Subscriptions should be the same.

In a prior [post](http://cicoria.com/cs1/blogs/cedarlogic/archive/2015/01/31/azure-resource-manager-adding-and-assigning-certificates-to-a-website.aspx) I walked through adding an SSL certificate then associating that certificate with an Azure Websites. While some sample C# code was provided, for this post it will entirely via using a REST tool – [Fiddler](http://www.telerik.com/download/fiddler) or [PostMan](https://chrome.google.com/webstore/detail/postman-rest-client/fdmmgilgnpjigdojojpjoooidkmcomcm?hl=en) suffices for this.

## Getting a Token

I’m not going to go into the token acquisition process here. The easiest way to obtain a token for this walkthrough is to just open a session to <https://portal.azure.com> then view the network traffic as you open up some Blades – for example, open up the “Resource Group” blade – look for an “**Authorization**” header.  It should show up as “**Bearer ….**”.  It’s a JWT which if you’d like (**WARNING** **you’re giving your token to a 3rd party to decipher**) [http://jwt.io/](http://jwt.io/ "http://jwt.io/")  - this site is managed by the <http://auth0.com> folks.

If you want to decode this yourself, note that the JWT token is presented in 3 parts, separated by a ‘.’ and each part base64 encoded. The parts are header, payload, and signature.

## Getting your subscription ID

In the prior post and the sample code here: [http://bit.ly/azrmsamples](http://bit.ly/azrmsamples "http://bit.ly/azrmsamples")  there’s some sample code in helper classes to list subscription ID’s for a login. I’m not reviewing that here.

You can logon to the <https://portal.azure.com> and then go to subscriptions. Click on the subscription that you will be using and then you’ll see a lower case Guid for that subscription.

## Available Providers and Capabilities

Not everything is available now, but, you can do a GET request as follows to see what sub-capabilities within that Resource Provider is available.

```
GET https://management.azure.com/subscriptions/<subscriptionId>/providers?api-version=2015-01-01

Authorization: Bearer <token>

```

You can take a look at the results from 1 of my subscriptions here:

[https://gist.github.com/cicorias/604286f96c833f246a37](https://gist.github.com/cicorias/604286f96c833f246a37 "https://gist.github.com/cicorias/604286f96c833f246a37")

### Resource Provider – Microsoft

From the response, let’s look at the Virtual Network provider and it’s manageable resources:

```
            "id": "/subscriptions/<subscriptionId>/providers/Microsoft.ClassicNetwork",
            "namespace": "Microsoft.ClassicNetwork",
            "resourceTypes": [
                {
                    "resourceType": "virtualNetworks",
                    "locations": [
                        "East US",
                        "East US 2",
                        "West US",
                        "North Central US (Stage)"
                    ],
                    "apiVersions": [
                        "2014-06-01",
                        "2014-01-01"
                    ]
                },
                {
                    "resourceType": "reservedIps",
                    "locations": [
                        "East Asia",
                    ],
                    "apiVersions": [
                        "2014-06-01",
                        "2014-01-01"
                    ]
                },
                {
                    "resourceType": "quotas",
                    "locations": [],
                    "apiVersions": [
                        "2014-06-01",
                        "2014-01-01"
                    ]
                },
                {
                    "resourceType": "gatewaySupportedDevices",
                    "locations": [],
                    "apiVersions": [
                        "2014-06-01",
                        "2014-01-01"
                    ]
                }
            ],
            "registrationState": "Registered"
        },

```

Within the ‘**resourceTypes’** array, we can see that ‘**virtualNetworks’** is available.

### Updating – first review an existing VNET

Resource Manager is in early preview; thus, documentation is very limited. However, this is REST – so, the conventions of REST (for the HTTP verbs) and the shape of the JSON for updating can be somewhat determined through reviewing existing resources.

```
{
    "value": [
        {
            "properties": {
                "provisioningState": "Succeeded",
                "status": "Created",
                "siteId": "<siteId>",
                "inUse": false,
                "addressSpace": {
                    "addressPrefixes": [
                        "10.1.0.0/16"
                    ]
                },
                "subnets": [
                    {
                        "name": "Subnet-1",
                        "addressPrefix": "10.1.0.0/24"
                    }
                ]
            },
            "id": "/subscriptions/<subscriptionId>/resourceGroups/demo2/providers/Microsoft.ClassicNetwork/virtualNetworks/myVnet",
            "name": "myVnet",
            "type": "Microsoft.ClassicNetwork/virtualNetworks",
            "location": "eastus2"
        }
    ]
}
```

From the above, you can see the shape of the VNET resource, and also take note of the ‘**id’** property as it illustrates the existence of the VNET within the resource group – here ‘**demo2’**.  Also note that the URI has the Resource name on the URL itself – this will be important when we PUT a new VNET.

## Create a Resource Group

Let’s first create a new Resource Group using a PUT

```
PUT
https://management.azure.com/subscriptions/<subscriptionId>/resourceGroups/demo2?api-version=2015-01-01

Content-Type: application/json  

Authorization:Bearer <token>

{  

"name": "demo2",  

"location": "eastus2",  

}

```

This should give you a HTTP 201 – Created response.

[![newrg](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/5100.newrg_thumb_4475F399.jpg "newrg")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/6237.newrg_098EC0D0.jpg)

## Creating a VNET

If you saw above, the shape of the VNET resource has a set of properties.  The REST call is shaped as follows:

```
https://management.azure.com/subscriptions/<subscriptionId>/resourceGroups/demo2/providers/Microsoft.ClassicNetwork/virtualNetworks/myVnet?api-version=2014-06-01

Authorization: Bearer <token>  

Content-Type: application/json  

{  

"name": "myVnet",  

"type": "Microsoft.ClassicNetwork/virtualNetworks",  

"location": "eastus2",  

"properties": {  

"addressSpace": {  

"addressPrefixes": [  

"10.1.0.0/16"  

]  

},  

"subnets": [  

{  

"name": "Subnet-1",  

"addressPrefix": "10.1.0.0/24"  

}  

]  

}  

}

```

For this VNET – called ‘**myVnet’** under the ‘**demo2’** resource group, I’ll be using the 10.1.0.0/16 address space (CIDR format) along with defining a single subnet – called ‘**Subnet-1’** that is a segment 10.1.0.0/24.

Again, once this runs, you receive a HTTP 201 – Created if all is OK.

[![SNAGHTMLd27cd3](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/1830.SNAGHTMLd27cd3_thumb_214888E7.png "SNAGHTMLd27cd3")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/8156.SNAGHTMLd27cd3_74339C18.png)

Now, you an switch back to the Portal to take a look at your VNET and review the settings.

[![image](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/1185.image_thumb_3A46E9DD.png "image")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/6038.image_4A5327E3.png)

**NOTE**: I want to stress again that not all aspects of each service within Azure is available today through Resource Manager. It is still in preview and as capabilities are added they will appear under the various /providers that are associated with your subscriptions.

## Registered Resource Providers

One last note, review the /providers result and identify IF your subscription is even “**Registered**” for that resource provider. For my subscription as an example, the status is as follows:

```
https://management.azure.com/subscriptions/<subscriptionId>/providers?api-version=2015-01-01

providers/microsoft.batch  

providers/microsoft.cache  

providers/Microsoft.DataFactory  

providers/Microsoft.DocumentDb  

providers/Microsoft.Insights  

providers/Microsoft.KeyVault  

providers/Microsoft.OperationalInsights  

providers/Microsoft.Search  

providers/Microsoft.StreamAnalytics  

providers/successbricks.cleardb  

providers/Microsoft.ADHybridHealthService  

providers/Microsoft.Authorization  

/providers/Microsoft.Features  

providers/Microsoft.Resources  

providers/Microsoft.Scheduler  

providers/Microsoft.Sql  

providers/microsoft.visualstudio  

providers/Microsoft.Web",

Classic:  

providers/Microsoft.ClassicCompute  

providers/Microsoft.ClassicNetwork  

providers/Microsoft.ClassicStorage

Not registered:  

providers/Microsoft.ApiManagement  

providers/Microsoft.BizTalkServices  

providers/Microsoft.IntelligentSystems  

providers/microsoft.support  

providers/NewRelic.APM

```

## Resource Provider Registration

For registering a subscription with a Resource provider, check the Azure Resource Manager REST API Reference: [https://msdn.microsoft.com/en-us/library/azure/dn790548.aspx](https://msdn.microsoft.com/en-us/library/azure/dn790548.aspx "https://msdn.microsoft.com/en-us/library/azure/dn790548.aspx")
