---
title: "Easily capture web hook messages in storage with hierarchical structure"
date: 2021-07-09T09:40:44+0000
lastmod: 2021-07-09T09:41:55+0000
slug: "easily-capture-web-hook-messages-in-storage-with-h"
tags: ["azure", "cloud", "logic apps"]
feature_image: "/images/2021/07/Screenshot-2021-07-09-051015.png"
aliases:
  - /easily-capture-web-hook-messages-in-storage-with-h/
---

Recently I was working with [Particle.io](https://particle.io) which provides several integration types. One of which is a basic [HTTP Webhook.](https://en.wikipedia.org/wiki/Webhook)

In need of a basic ability to capture each device message that is published across the webhook, we initially thought that we had to spin up a basic HTTP application, then write the binding code for persisting to an Azure Storage Account. We could've used Azure Functions and the simplicity of the Binding to Azure Storage feature.

What we ended up with is such a basic [Azure Logic App](https://docs.microsoft.com/en-us/azure/logic-apps/) that provides quite a bit of power in just two shapes on the designer.

![](/images/2021/07/Screenshot-2021-07-09-054105.png)
*Azure Logic App Designer*

The power of these two shapes is that for each HTTP Post Webhook - each file is written to storage using the macro language - as such:

```json
"name": "@{concat(formatDateTime(utcNow(), 'yyyy/MM/dd/HH/'),
    formatDateTime(utcNow(), 'yyyy-MM-dd-HH-mm-ss') ,
    '-event-',triggerBody()?['event'] , '-coreid-',
    triggerBody()?['coreid'],'.json')}"

```

This creates files using hierarchical separators as follows with a filename:

`{container}/2021/06/16/16/event-send-coreid-e00f76181888888-13-27.json`

## Why does this matter?

Azure Blob Storage provides a Container list capability. That [REST call](https://docs.microsoft.com/en-us/rest/api/storageservices/list-blobs) (and that means everything including all SDKs use this) traverses a container and cannot search or list in any specific order. What it can do is accept a prefix that narrows the set of blob objects that are returned for traversing.

An example of where this is particularly important is in Azure Stream Analytics which when bound to an input of a Storage Account or Azure Data Lake Service v2 it must traverse all files looking for files that are "recent" to be used as messages when the Service Starts up. If there are just a few hundred this has startup time impact and slows the traversal down.

When the prefix follows ISO date formats, this permits the caller to prefix the call with `2021/06/` — which then returns just files that have that prefix. Remember that the `/` is just part of the file name and doesn't truly represent a folder.

### Full Code

The following is the full declarative code when switching to the code view in Logic App Designer:

```json
{
    "definition": {
        "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
        "actions": {
            "Create_blob": {
                "inputs": {
                    "body": "@triggerBody()",
                    "host": {
                        "connection": {
                            "name": "@parameters('$connections')['azureblob']['connectionId']"
                        }
                    },
                    "method": "post",
                    "path": "/datasets/default/files",
                    "queries": {
                        "folderPath": "/output",
                        "name": "@{concat(formatDateTime(utcNow(), 'yyyy/MM/dd/HH/'), formatDateTime(utcNow(), 'yyyy-MM-dd-HH-mm-ss') ,'-event-',triggerBody()?['event'] , '-coreid-', triggerBody()?['coreid'],'.json')}",
                        "queryParametersSingleEncoded": true
                    }
                },
                "runAfter": {},
                "runtimeConfiguration": {
                    "contentTransfer": {
                        "transferMode": "Chunked"
                    }
                },
                "type": "ApiConnection"
            }
        },
        "contentVersion": "1.0.0.0",
        "outputs": {},
        "parameters": {
            "$connections": {
                "defaultValue": {},
                "type": "Object"
            }
        },
        "triggers": {
            "manual": {
                "inputs": {
                    "schema": {
                        "data": "foobar"
                    }
                },
                "kind": "Http",
                "type": "Request"
            }
        }
    },
    "parameters": {
        "$connections": {
            "value": {
                "azureblob": {
                    "connectionId": "/subscriptions/xxx/resourceGroups/xxx/providers/Microsoft.Web/connections/azureblob",
                    "connectionName": "azureblob",
                    "id": "/subscriptions/xxx/providers/Microsoft.Web/locations/eastus/managedApis/azureblob"
                }
            }
        }
    }
}

```

Some other references

![](https://docs.microsoft.com/en-us/media/logos/logo-ms-social.png)
![](https://docs.microsoft.com/en-us/media/logos/logo-ms-social.png)
![](https://docs.microsoft.com/en-us/media/logos/logo-ms-social.png)
![](https://assets.uvcdn.com/pkg/oembed/votes-091211c9006da8621310a57b963f98502e22c56c4202c61f55909e9bf3689818.png)
![](https://en.wikipedia.org/static/apple-touch/wikipedia.png)
