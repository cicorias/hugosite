---
title: "Azure Resource Manager–Creating an IaaS VM within a VNET"
date: 2015-02-12T07:57:54+0000
lastmod: 2015-02-12T07:57:54+0000
slug: "azure-resource-managercreating-an-iaas-vm-within-a-vnet"
aliases:
  - /azure-resource-managercreating-an-iaas-vm-within-a-vnet/
---

**NOTE**: [Azure Resource](https://msdn.microsoft.com/en-us/library/azure/dn790568.aspx) manager is in Preview. Thus, anything posted here may change. However, the approach for identifying what resources are available for update and registered for Subscriptions should be the same.

**NOTE: Any reference to the "Classic" Resource providers - such as ClassicNetwork, ClassicCompute - should NOT be used and are NOT supported.**

#### Here are the prior posts:

- [Azure Resource Manager – Creating Storage Accounts](http://blogs.msdn.com/b/scicoria/archive/2015/02/09/azure-resource-manager-creating-storage-accounts.aspx)
- [Azure Resource Manager– Creating a Resource Group and a VNET](http://blogs.msdn.com/b/scicoria/archive/2015/02/09/azure-resource-manager-creating-a-resource-group-and-a-vnet.aspx)
- [Azure Resource Manager – Adding and Assigning Certificates to a Website](http://blogs.msdn.com/b/scicoria/archive/2015/01/31/azure-resource-manager-adding-and-assigning-certificates-to-a-website.aspx)

For this walkthrough I’m going to build up a Linux VM instance off of a VHD that I have within a storage account. I use the ARM REST API calls direct, bypassing the Templates that are coming to ARM.

## Azure Resource Manager Templates

The REST API calls that I’m illustrating below are **NOT** using *Azure Resource Manager* (**ARM**) **Templates**. You can review some of the articles below for more information on **ARM Templates**.

- <http://azure.microsoft.com/blog/2015/01/06/how-to-provision-and-deploy-multiple-websites-from-your-cloud-deployment-project/>
- <https://msdn.microsoft.com/en-us/library/azure/dn835138.aspx>
- <http://blogs.technet.com/b/devops/archive/2014/09/25/azure-resource-manager-for-devops-and-mere-mortals.aspx>

Currently, ARM Templates are in preview and as of this writing, only 3 templates are available. Those are listed in the tooling. in the links above.

### ARM Templates Basics

ARM Templates provided a template language that establishes the dependencies amongst the composition of supporting resources. In addition, the backend to ARM Templates provides the management and control over provisioning all these dependency upon submission of the ARM Template provision request. Ultimately, it is built upon ARM – which for this post is accessible via the ARM REST API calls.

## Creating a VM using ARM REST API – not using Templates

This blog post is NOT about ARM Templates. I cover the underlying ARM REST API directly and create composition through a series of client side REST API calls (if that makes any sense).

### Preparation steps:

- Existence of a storage account within a subscription that the user (who’s access token we are using – see prior posts) has access to. In other words – owner.
- A VHD that is ready for deployment – prior to the REST calls below, I used the Copy Blob REST API call <https://msdn.microsoft.com/en-us/library/azure/dd894037.aspx> - you can also use the PowerShell ‘[Start-AzureStorageBlobCopy’](https://msdn.microsoft.com/en-us/library/azure/dn495267.aspx)  – this will make a quick copy of the VHD.

```
$blob1 = Start-AzureStorageBlobCopy -srcUri $srcUri `
	-SrcContext $srcContext `
	-DestContainer $containerName `
	-DestBlob "testcopy1.vhd" `
	-DestContext $destContext 

```

## Resource Manager Composition

If you examine an existing VM via the REST API you will see within the JSON response several sections contained within the properties JSON object.

Any of these, for example ‘**domainName’**, ‘*networkProfile*/**virtualNetworks’**, ‘*storageProfile/operatingSystemDisk*/**storageAccount’** are additional resources that you must compose or create prior to making the REST API call to create (PUT) the VM that you want to provision. If you refer back to the prior posts that lists the /providers for a subscription, you will find providers as follows:

- Networks - **Microsoft.ClassicNetwork** – with resource types of ‘**virtualNetworks’**, ‘**reservedIps’**, ‘quotas’, and ‘**gatewaySupportedDevices’**
- Domain Name - **Microsoft.ClassicCompute** – with resource providers of ‘**domainNames’**, ‘**virtualMachines’**, ‘**capabilities**, ‘**quotas’**, etc.

You will see ‘**storageAccount’** listed in the GET response for each disk – OS and data disks – that are used by the existing VM. Note that there is an ‘id’ property. That’s the ‘id’ or reference that will be used in the final PUT request at the end of the post for each of the associated resources.

## Prior Posts

In prior posts, I cover the creation of a Resource Group and a Storage Account.  Here is a screen shot of the Resource Group creating using Postman (I won’t repeat the Storage Account creation).

[![SNAGHTML1671163](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/0066.SNAGHTML1671163_thumb_108AF5A2.png "SNAGHTML1671163")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/8468.SNAGHTML1671163_55A3C2D8.png)

## Create Domain Name

The domain name represents the ‘**cloud service’** – which essentially represents the wrapper and associated public IP address that the VM when created be behind – think firewall. In the new portal (<https://portal.azure.com>) these show as **Domains** (thus that is what ARM uses). In the current production portal (<https://manage.windowsazure.com>) they appear as **Cloud Services** – a term that anybody doing Worker and Web Roles in PaaS are quite familiar with.

The PUT request contains a JSON body that is quite simple.

```
PUT https://management.azure.com/subscriptions/<subscriptionId>/resourceGroups/demo2/providers/Microsoft.ClassicCompute/domainNames/scicoriacentosnew?api-version=2014-06-01

Content-Type: application/json  

Authorization: Bearer: <token>

{  

"properties": {  

"label": "scicoriacentosnew",  

"hostName": "scicoriacentosnew.cloudapp.net"  

},  

"name": "scicoriacentosnew",  

"type": "Microsoft.ClassicCompute/domainNames",  

"location": "eastus2"  

}

```

### Create Domain Response

For this call, the HTTP response comes back as ‘**201 – created’** – you’ll see in the other requests, as they are longer running, you will get a ‘**202 – Accepted’** – and with that response headers that you can obtain the operation request ID and ask Azure for the status of the request. That is key to identifying any issues beyond the simple serialization issues for bad JSON PUT payloads.

## Create Virtual Network

For a VNET (virtual network) I’m going to create with my ‘**demo2’** resource group a VNET with –well, the JSON below should be fairly explanatory (that’s what’s nice about JSON and REST of these things).

```
PUT https://management.azure.com/subscriptions/<subscriptionId>/resourceGroups/demo2/providers/Microsoft.ClassicNetwork/virtualNetworks/scicoriacentosnew?api-version=2014-06-01

Content-Type: application/json  

Authorization: Bearer <token>

{  

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

},  

{  

"name": "Subnet-2",  

"addressPrefix": "10.1.1.0/24"  

}  

]  

},  

"id": "/subscriptions/<subscriptionId>/resourceGroups/demo2/providers/Microsoft.ClassicNetwork/virtualNetworks/scicoriacentosnew",  

"name": "scicoriacentosnew",  

"type": "Microsoft.ClassicNetwork/virtualNetworks",  

"location": "eastus2"  

}

```

#### Explanation

For those that aren’t familiar, the VNET will be created covering a CIDR range of addresses 10.1.\*.\*/16 – and, in addition, within that top-level range, I’ve created a 2 subnets covering 10.1.0.\*/24 & 10.1.1.\*/24.

Additional subnets can be specified within the JSON array [] if needed. Validation will occur at submission and provisioning time – so, you need to check for a ‘202 – Accepted’ response, and with that operations ID, validate status.. I could’ve also specified additional ranges for the address prefixes as well – just as you can do in the Azure Management portal.

[![SNAGHTML169aba5](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/7120.SNAGHTML169aba5_thumb_6640DF28.png "SNAGHTML169aba5")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/0358.SNAGHTML169aba5_125DDC1A.png)

## Create Virtual Machine

Now that we have the following, we’re ready to issue an **ARM REST API PUT** request to create the virtual machine.:

1. Storage Account with a VHD ready to use
2. Resource Group
3. Domain Name
4. Virtual Network

This one is rather lengthy. You should note the ‘**nested’** referred to resource that were created in the prior steps. Again, once submitted and no deserialization issues, URI issues, etc., you should get back a ‘**202 – Accepted’** – from that response you have to check the Operation Status using the provided status ID:

```
//PUT https://management.azure.com/subscriptions/<subscriptionId>/resourceGroups/demo2/providers/Microsoft.ClassicCompute/virtualMachines/scicoriacentosnew?api-version=2014-06-01
{
    "properties": {
        "hardwareProfile": {
            "platformGuestAgent": true,
            "size": "Basic_A2",
            "deploymentName": "scicoriacentosnew",
            "deploymentLabel": "scicoriacentosnew",
        },
        "domainName": {
            "id": "/subscriptions/<subscriptionId>resourceGroups/demo2/providers/Microsoft.ClassicCompute/domainNames/scicoriacentosnew",
            "name": "scicoriacentosnew",
            "type": "Microsoft.ClassicCompute/domainNames"
        },
        "storageProfile": {
            "operatingSystemDisk": {
                "diskName": "scicoriacentosnew-os-20150212",
                "caching": "ReadWrite",
                "operatingSystem": "Linux",
                "ioType": "Standard",
                //"sourceImageName": "5112500ae3b842c8b9c604889f8753c3__OpenLogic-CentOS-65-20140926",
                "vhdUri": "https://scicoriademo.blob.core.windows.net/vhds/testcopy1.vhd",
                "storageAccount": {
                    "id": "/subscriptions/<subscriptionId>resourceGroups/demo/providers/Microsoft.ClassicStorage/storageAccounts/scicoriademo",
                    "name": "scicoriademo",
                    "type": "Microsoft.ClassicStorage/storageAccounts"
                }
            }
        },
        "networkProfile": {
            "inputEndpoints": [
                {
                    "endpointName": "SSH",
                    "privatePort": 22,
                    "publicPort": 22,
                    "protocol": "tcp",
                    "enableDirectServerReturn": false
                }
            ],
            "virtualNetwork": {
                "subnetNames": [
                    "Subnet-1"
                ],
                "id": "/subscriptions/<subscriptionId>resourceGroups/demo/providers/Microsoft.ClassicNetwork/virtualNetworks/scicoriacentos",
                "name": "scicoriacentos",
                "type": "Microsoft.ClassicNetwork/virtualNetworks"
            }
        }
    },
    "location": "eastus2",
    "name": "scicoriacentosnew"
}

```

### Response

If all is OK from a formatting and basic validation, you should see an ‘202 – Accepted’ – from that obtain the operation ID – and use the API call to check that operation’s status.

[![SNAGHTML16bd423](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/8662.SNAGHTML16bd423_thumb_260D565F.png "SNAGHTML16bd423")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/1616.SNAGHTML16bd423_48625B27.png)

## Checking Operation Status

Take a look at the documentation for the structure of that call.

<https://msdn.microsoft.com/en-us/library/azure/ee460783.aspx>

#### A Succeeded Operation

[![SNAGHTML1690757](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/5556.SNAGHTML1690757_thumb_555ECBE9.png "SNAGHTML1690757")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/4466.SNAGHTML1690757_0C392030.png)

#### An InProgress Operation

[![SNAGHTML1681c7a](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/2781.SNAGHTML1681c7a_thumb_1282876F.png "SNAGHTML1681c7a")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/6888.SNAGHTML1681c7a_0992F530.png)

### An Error Operation Status

[![SNAGHTML16a181b](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/3113.SNAGHTML16a181b_thumb_28D82CB4.png "SNAGHTML16a181b")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/3276.SNAGHTML16a181b_2DBAE070.png)
