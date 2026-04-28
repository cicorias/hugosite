---
title: "Azure Resource Manager – Creating Storage Accounts"
date: 2015-02-09T09:09:43+0000
lastmod: 2015-02-09T09:09:43+0000
slug: "azure-resource-manager-creating-storage-accounts"
aliases:
  - /azure-resource-manager-creating-storage-accounts/
---

**NOTE**: [Azure Resource](https://msdn.microsoft.com/en-us/library/azure/dn790568.aspx) manager is in Preview. Thus, anything posted here may change. However, the approach for identifying what resources are available updatable, and registered for Subscriptions should be the same.

In a prior [post](http://cicoria.com/cs1/blogs/cedarlogic/archive/2015/01/31/azure-resource-manager-adding-and-assigning-certificates-to-a-website.aspx) I walked through adding an SSL certificate then associating that certificate with an Azure Websites. While some sample C# code was provided, for this post it will entirely via using a REST tool – [Fiddler](http://www.telerik.com/download/fiddler) or [PostMan](https://chrome.google.com/webstore/detail/postman-rest-client/fdmmgilgnpjigdojojpjoooidkmcomcm?hl=en) suffices for this.

The last [post](http://blogs.msdn.com/b/scicoria/) I walked through adding a VNET. To cleanup, remember that with REST an HTTP DELETE is all you need to cleanup…

## Getting Available Resource Providers

Again, from the prior posts, if you want to see the list of resource providers for a subscription, issue an authenticated call to the /providers resource:

[https://msdn.microsoft.com/en-us/library/azure/dn790572.aspx](https://msdn.microsoft.com/en-us/library/azure/dn790572.aspx "https://msdn.microsoft.com/en-us/library/azure/dn790572.aspx")

I’ve glossed over authentication quite a bit in the prior posts, take a look here: [https://msdn.microsoft.com/en-us/library/azure/dn790557.aspx](https://msdn.microsoft.com/en-us/library/azure/dn790557.aspx "https://msdn.microsoft.com/en-us/library/azure/dn790557.aspx") which uses the ADAL library for Managed code.  Again, you can do the calls via REST as well – I’ll try to cover that in a future post.

## Creating a Storage Account

Again, the best way to ‘learn’ the representation of these resources is to review an existing one.

Here, issuing a GET request to the following gives me the resource properties.

```
GET https://management.azure.com/subscriptions/<subscriptionId>/resourceGroups/somegroup/providers/Microsoft.ClassicStorage/storageAccounts/<resourceName>?api-version=2014-06-01

{  

"properties": {  

"provisioningState": "Succeeded",  

"status": "Created",  

"endpoints": [  

"https://<accountName>.blob.core.windows.net/",  

"https://<accountName>.queue.core.windows.net/",  

"https://<accountName>.table.core.windows.net/",  

"https://<accountName>.file.core.windows.net/"  

],  

"accountType": "Standard-LRS",  

"geoPrimaryRegion": "East US",  

"statusOfPrimaryRegion": "Available",  

"geoSecondaryRegion": "",  

"statusOfSecondaryRegion": "",  

"creationTime": "2014-12-19T19:18:59Z"  

},  

"id": "/subscriptions/<subscriptionId>/resourceGroups/somegroup/providers/Microsoft.ClassicStorage/storageAccounts/<accountName>",  

"name": "<accountName>",  

"type": "Microsoft.ClassicStorage/storageAccounts",  

"location": "eastus2"  

}

```

## Creating a Locally Redundant Storage Account (LRS)

Ok, we trim back the JSON properties to what we just need to create. Note that when you’re in the portal, there’s really not too many options to set other than the Name and the Pricing level. Same for the JSON properties here.

```
PUT https://management.azure.com/subscriptions/<subscriptionId>/resourceGroups/demo2/providers/Microsoft.ClassicStorage/storageAccounts/<resourceName>?api-version=2014-06-01

Authorization: Bearer <token>  

Content-Type: application/json

{  

"properties": {  

"accountType": "Standard-LRS",  

},  

"name": "<reourceName>",  

"type": "Microsoft.ClassicStorage/storageAccounts",  

"location": "eastus2"  

}

```

Here’s the screenshot from Postman – note the 202 – Accepted

[![SNAGHTMLf393b6](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/8308.SNAGHTMLf393b6_thumb_664C7946.png "SNAGHTMLf393b6")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/2185.SNAGHTMLf393b6_2F6F944F.png)
