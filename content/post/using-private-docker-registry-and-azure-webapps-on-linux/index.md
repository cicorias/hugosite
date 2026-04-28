---
title: "Using Private Docker Registry and Azure WebApps on Linux with ARM Templates"
date: 2017-05-18T15:02:23+0000
lastmod: 2017-05-18T15:02:23+0000
slug: "using-private-docker-registry-and-azure-webapps-on-linux"
feature_image: "https://www.cicoria.com/content/images/2017/05/image_4.png"
aliases:
  - /using-private-docker-registry-and-azure-webapps-on-linux/
---

Took a bit of decoding, but an approach to deploy via Azure ARM templates to Azure WebApps on Linux (Preview now), the special properties needed are as follows:

```
{
  "name": "appsettings",
  "type": "config",
  "apiVersion": "2016-03-01",
  "dependsOn": [
    "[resourceId('Microsoft.Web/sites', parameters('appName'))]"
  ],
  "tags": {
    "displayName": "appSettings"
  },
  "properties": {
    "DOCKER_CUSTOM_IMAGE_NAME": "mszzz.azurecr.io/escrow-webapp:latest",
    "DOCKER_CUSTOM_IMAGE_RUN_COMMAND": "nginx",
    "DOCKER_REGISTRY_SERVER_PASSWORD": "o8P=!!!!!!!!!!!!",
    "DOCKER_REGISTRY_SERVER_URL": "https://mszzz.azurecr.io/",
    "DOCKER_REGISTRY_SERVER_USERNAME": "mszzz"
  }
}

```

Clearly, the `PASSWORD` and the server URL, image name, must match your environment, but this is the gist of it :)
