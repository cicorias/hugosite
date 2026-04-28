---
title: "Error: Manually created ServicePrincipalToken does not contain secret material to retrieve a new access token"
date: 2019-12-07T12:05:25+0000
lastmod: 2019-12-07T12:05:25+0000
slug: "error-manually-created-serviceprincipaltoken-does-not-contain-secret-material-to-retrieve-a-new-access-token"
feature_image: "/images/2019/12/Annotation-2019-12-07-120339.jpg"
aliases:
  - /error-manually-created-serviceprincipaltoken-does-not-contain-secret-material-to-retrieve-a-new-access-token/
---

When a long-running Terraform on Azure deployment is happening (or an `apply`) the token used by Terraform is NOT being refreshed during the operation.

### Error message

```
Error: Error waiting for creation of HDInsight Hadoop Cluster "mycluster" (Resource Group "my-cluster"): azure.BearerAuthorizer#WithAuthorization: Failed to refresh the Token for request to https://management.azure.com/subscriptions/<redacted>/resourceGroups/scicoria-hdp-cluster/providers/Microsoft.HDInsight/clusters/mycluster/azureasyncoperations/create?api-version=2018-06-01-preview: StatusCode=0 -- Original Error: Manually created ServicePrincipalToken does not contain secret material to retrieve a new access token

```

There is an outstanding or actually closed [issue on GitHub](https://github.com/hashicorp/go-azure-helpers/issues/22) that IMHO was prematurely closed. There is hope, the `1.37` version of the Azure Provider may have fixed this - as shown in [this issue](https://github.com/terraform-providers/terraform-provider-azurerm/issues/2602#issuecomment-558524825)

To specify a specific version of the provider you can use the following in your `.tf` files

```
provider "azurerm" {
  version         = "=1.37.0"
  subscription_id = var.subscription_id
}

```

But to get around this limit and get a "full-hour" of deployment time, you can "kill" the tokens with the following:

> Note: this is run from **PowerShell core** [taken from this gh issue](https://github.com/hashicorp/go-azure-helpers/pull/39#issuecomment-543253781)

```
$tokens = Get-Content $Home\.azure\accessTokens.json | ConvertFrom-Json
foreach ($token in $tokens) { $token.expiresOn = "1970-01-01 00:00:00.000000" }
$tokens | ConvertTo-json | Set-Content $Home\.azure\accessTokens.json

```
