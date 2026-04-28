---
title: "Checking if a WebSite Name is Available via Azure ARM (REST)"
date: 2016-06-17T16:22:01+0000
lastmod: 2016-06-17T16:22:45+0000
slug: "checking-if-a-website-name-is-available-via-azure-arm-rest"
feature_image: "/images/2016/06/azure.png"
aliases:
  - /checking-if-a-website-name-is-available-via-azure-arm-rest/
---

**Note:** *Once I get my old blog history back - which has a bunch of Azure REST stuff, you can go to <https://blogs.msdn.microsoft.com/scicoria> for now...*

## Get what Features are available for a Resource Provider.

If you're not sure what potential REST calls you can make, you can query (GET) via a simple call to the Provider - for example, I'm going to issue a call to the `Microsoft.Web` resource provider.

Using a Bearer token obtained via AAD or just look at your browser history to get an OAuth token in the traffic as a quick and temporary means.

```
Authorization: Bearer xxxx
Accept: application/json
GET https://management.azure.com/subscriptions/<yoursubid>/providers/Microsoft.Web?api-version=2016-06-01

```

This gives me a big json payload back. But in that payload is the following:

```
{
      "resourceType": "ishostnameavailable",
      "locations": [
        "South Central US",
        "North Europe",
        "West Europe",
        "Southeast Asia",
        "West US",
        "East US",
        "Japan West",
        "Japan East",
        "East Asia",
        "East US 2",
        "North Central US",
        "Central US",
        "Brazil South",
        "Canada Central",
        "Canada East"
      ],

```

The `ishostnameavailable` is there. Given that, now I can issue a simple request - via an HTTP GET to a resource to see if it's available or noe.

```
Authorization: Bearer xxxx
Accept: application/json
GET https://management.azure.com//subscriptions/<yoursubid>/providers/microsoft.web/ishostnameavailable/cicoriablog?api-version=2015-08-01
{
  "id": null,
  "name": "cicoriablog",
  "type": "Microsoft.Web/global",
  "location": null,
  "tags": null,
  "properties": false
}

```

In the above, `false` means is NOT available.. Not sure if that's obvious.

What else is there?  
Turns out there's a hole bunch of potential API calls - have fun poking around...

```
      "resourceType": "sites/extensions",
      "resourceType": "sites/slots/extensions",
      "resourceType": "sites/instances",
      "resourceType": "sites/slots/instances",
      "resourceType": "sites/instances/extensions",
      "resourceType": "sites/slots/instances/extensions",
      "resourceType": "publishingUsers",
      "resourceType": "ishostnameavailable",
      "resourceType": "isusernameavailable",
      "resourceType": "sourceControls",
      "resourceType": "availableStacks",
      "resourceType": "listSitesAssignedToHostName",
      "resourceType": "sites/hostNameBindings",
      "resourceType": "sites/domainOwnershipIdentifiers",
      "resourceType": "sites/slots/hostNameBindings",
      "resourceType": "operations",
      "resourceType": "certificates",
      "resourceType": "serverFarms",
      "resourceType": "serverFarms/workers",
      "resourceType": "sites",
      "resourceType": "sites/slots",
      "resourceType": "runtimes",
      "resourceType": "sites/metrics",
      "resourceType": "sites/metricDefinitions",
      "resourceType": "sites/slots/metrics",
      "resourceType": "sites/slots/metricDefinitions",
      "resourceType": "serverFarms/metrics",
      "resourceType": "serverFarms/metricDefinitions",
      "resourceType": "sites/recommendations",
      "resourceType": "recommendations",
      "resourceType": "georegions",
      "resourceType": "sites/premieraddons",
      "resourceType": "hostingEnvironments",
      "resourceType": "hostingEnvironments/multiRolePools",
      "resourceType": "hostingEnvironments/workerPools",
      "resourceType": "hostingEnvironments/metrics",
      "resourceType": "hostingEnvironments/metricDefinitions",
      "resourceType": "hostingEnvironments/multiRolePools/metrics",
      "resourceType": "hostingEnvironments/multiRolePools/metricDefinitions",
      "resourceType": "hostingEnvironments/workerPools/metrics",
      "resourceType": "hostingEnvironments/workerPools/metricDefinitions",
      "resourceType": "hostingEnvironments/multiRolePools/instances",
      "resourceType": "hostingEnvironments/multiRolePools/instances/metrics",
      "resourceType": "hostingEnvironments/multiRolePools/instances/metricDefinitions",
      "resourceType": "hostingEnvironments/workerPools/instances",
      "resourceType": "hostingEnvironments/workerPools/instances/metrics",
      "resourceType": "hostingEnvironments/workerPools/instances/metricDefinitions",
      "resourceType": "managedHostingEnvironments",
      "resourceType": "deploymentLocations",
      "resourceType": "functions",
      "resourceType": "ishostingenvironmentnameavailable",
      "resourceType": "classicMobileServices",
      "resourceType": "connections",
      "resourceType": "locations",
      "resourceType": "locations/managedApis",
      "resourceType": "locations/apiOperations",

```
