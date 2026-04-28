---
title: "Using Azure CLI with two different credentials"
date: 2019-04-17T11:33:06+0000
lastmod: 2019-04-17T11:33:06+0000
slug: "using-azure-cli-with-two-different-credentials"
feature_image: "https://www.cicoria.com/content/images/2019/04/MicrosoftAzure.png"
aliases:
  - /using-azure-cli-with-two-different-credentials/
---

Sometimes you need to logon to more than one Azure Active Directory (don't ask why). Normally the azure cli tool keeps a file in `./azure` about your subscriptions, etc.

you could just logout/login - but that is a royal pain in the ass.

So for example say you need to logon to a Azure Gov cloud with different credentials. For that you can set or unset the `AZURE_CONFIG_DIR` which will point to your respective `~./azure` of your choice...

```
# government az cli credentials cached in a .azure_gov folder
export AZURE_CONFIG_DIR=.azure_gov

az cloud set --name AzureUSGovernment
az login
az account set -s 9999-9999-9999-9---9-9-9-9-

```
