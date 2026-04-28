---
title: "Using regular expressions in Azure Application Gateway Rewrite Rules - extract Certificate Common Name"
date: 2023-04-30T17:05:05+0000
lastmod: 2023-04-30T18:17:40+0000
slug: "using-regular-expressions-in-azure-application-gateway-rewrite-rules-extract-certificate-common-name"
feature_image: "/images/2023/04/blog-hero-homepage-road-traffic-prediction_1000x800.webp"
aliases:
  - /using-regular-expressions-in-azure-application-gateway-rewrite-rules-extract-certificate-common-name/
---

Microsoft Azure's [Application Gateway](https://learn.microsoft.com/en-us/azure/application-gateway/) is a platform service that can offload capabilities, so you don't have to code them for yourself.

With proxy software, one capability is the ability to rewrite aspects of the HTTP request – Server, Request, and Response variables.

Another feature is Application Gateway is support for certificate authentication or mTLS ([mutual TLS](https://www.cloudflare.com/learning/access-management/what-is-mutual-tls/)).  In this model, Application Gateway becomes the authentication boundary, again offloading a capability that you do not have to code for. But to identify aspects of the client it's necessary to set up rewrite rules to supplement the forwarded request to your application over HTTP.

The set of mTLS headers that are available from Application Gateway are listed here: [Rewrite HTTP headers and URL with Azure Application Gateway | Microsoft Learn](https://learn.microsoft.com/en-us/azure/application-gateway/rewrite-http-headers-url#mutual-authentication-server-variables)

## Example Certificate Header

Enabling the forwarding of the certificate information is as easy as setting up a simple rule.

### Via the portal

![](/images/2023/04/image-2.png)

### Via Terraform

Here's a full example of how in Terraform to setup mTLS rewrite rules using the [Azure RM Application Gateway Terraform Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/application_gateway):

```hcl
resource "azurerm_application_gateway" "app_gateway" 
... #

  rewrite_rule_set {
    name = local.rewrite_rule_set_name
    rewrite_rule {
      name          = "client_certificate_mtls"
      rule_sequence = 100
      request_header_configuration {
        header_name  = "x-client-certificate"
        header_value = "{var_client_certificate}"
      }
      request_header_configuration {
        header_name  = "x-client-certificate-end-date"
        header_value = "{var_client_certificate_end_date}"
      }
      request_header_configuration {
        header_name  = "x-client-certificate-fingerprint"
        header_value = "{var_client_certificate_fingerprint}"
      }
      request_header_configuration {
        header_name  = "x-client-certificate-issuer"
        header_value = "{var_client_certificate_issuer}"
      }
      request_header_configuration {
        header_name  = "x-client-certificate-serial"
        header_value = "{var_client_certificate_serial}"
      }
      request_header_configuration {
        header_name  = "x-client-certificate-start-date"
        header_value = "{var_client_certificate_start_date}"
      }
      request_header_configuration {
        header_name  = "x-client-certificate-subject"
        header_value = "{var_client_certificate_subject}"
      }
      request_header_configuration {
        header_name  = "x-client-certificate-verification"
        header_value = "{var_client_certificate_verification}"
      }
    }
  }
```

>NOTE: sample terraform is location [here](https://github.com/cicorias/azure-terraform-appgateway-traffic-manager/tree/main/generated).

After deploying, an mTLS request looks like the following – which uses a sample Go based diagnostic server located here.

We can see the amended headers below – and notice the subject name of the certificate as shown is `CN=FOO_987654321087654321,OU=IoT,O=Contoso,L=Take,ST=NY,C=US`.

```bash
Request Headers
	User-Agent: curl/7.87.0
	X-Forwarded-For: 22.21.20.111:55272
	X-Client-Certificate: -----BEGIN%20CERTIFICATE-----%0AMIICWTCCAgCgAwIBAgIBAjAKBggqhkjOPQQDAjA0MTIwMAYDVQQDDClBenVyZSBJ%0Ab1QgSHViIEludGVybWVkaWF0ZSBDZXJ0IFRlc3QgT25seTAeFw0yMzA0MzAxNTMy%0AMDBaFi0wXBxuc04%3D%0A-----END%20CERTIFICATE-----%0A
	X-Client-Certificate-Issuer: CN=Azure IoT Hub Intermediate Cert Test Only
	X-Client-Certificate-Start-Date: Apr 30 15:32:00 2023 GMT
	X-Client-Cn: FOO_987654321087654321
	X-Original-Host: scicoriaag1.eastus.cloudapp.azure.com
	Accept: */*
	X-Forwarded-Proto: https
	X-Client-Certificate-Serial: 02
	X-Client-Certificate-Subject: CN=FOO_987654321087654321,OU=IoT,O=Contoso,L=Take,ST=NY,C=US
	Connection: keep-alive
	X-Forwarded-Port: 443
	X-Original-Url: /
	X-Client-Certificate-End-Date: May 30 15:32:00 2023 GMT
	X-Client-Certificate-Verification: SUCCESS
	X-Appgw-Trace-Id: ca99b77c0afee96d6a12bff457f7be09
	X-Client-Certificate-Fingerprint: 2c46ace8e01e3284e5fdd30787cc4303952bfb09
	Request Details
	Method:   GET
	Host:     scicoriaag1.eastus.cloudapp.azure.com
	URL:      /
	URI:      /
	Proto:    HTTP/1.1
	Remote:   10.21.0.6:26248
	Username:
	Length:   0
Env Details
	HOSTNAME: myLinuxVM3
```

# Using Regular Expressions

Now, say the back-end application just needs the common name (CN=) from the certificate subject?

For example, from above, the full subject is `CN=FOO_987654321087654321,OU=IoT,O=Contoso,L=Take,ST=NY,C=US` – but our back-end application just needs the value of the `CN=` part of the certificate.

For that, Application Gateway supports the use of regular expressions along with providing the matched groups to the action part of the rules.

## Using the Portal

For this, we need to provide a condition, which triggers the regular expression and feeds the match groups to the action.

![](/images/2023/04/image-3.png)

## Using Terraform

In Terraform, we supply an additional `rewrite_rule` to the `rewrite_rule_set` block in the `resource azurerm_application_gateway` definition as shown below:

![](/images/2023/04/image-4.png)

Here is the Terraform code – note the regular expression is `"CN=(.*?)[,|$]"` for the condition, and for the match group the header value is set to the pattern `{var_serverVariable_#}`  – so for this case it becomes `{var_client_certificate_subject_1}`

```hcl
resource "azurerm_application_gateway" "app_gateway" {
  location            = azurerm_resource_group.this_resource_group.location
  name                = local.app_gateway_name
  resource_group_name = azurerm_resource_group.this_resource_group.name

  backend_address_pool {
    name = local.backend_address_pool_name
  }

  backend_http_settings {
    affinity_cookie_name  = "ApplicationGatewayAffinity"
    cookie_based_affinity = "Disabled"
    name                  = local.backend_http_settings_name
    port                  = 8080
    protocol              = "Http"
    request_timeout       = 60
  }

  frontend_ip_configuration {
    name = local.frontend_ip_configuration_name
    public_ip_address_id = azurerm_public_ip.app_gateway_public_ip.id
  }

  frontend_port {
    name = "port_80"
    port = 80
  }

  frontend_port {
    name = local.frontend_port_name
    port = 443
  }

  gateway_ip_configuration {
    name      = local.gateway_ip_configuration_name
    subnet_id = azurerm_subnet.subnet_app_gateway_2.id
  }

  http_listener {
    frontend_ip_configuration_name = local.frontend_ip_configuration_name
    frontend_port_name             = local.frontend_port_name
    name                           = local.http_listener_name
    protocol                       = "Https"
    ssl_certificate_name           = local.frontend_ssl_cert_name
    ssl_profile_name               = local.ssl_profile_name
  }
  identity {
    identity_ids = [azurerm_user_assigned_identity.user_identity.id]
    type         = "UserAssigned"
  }

  request_routing_rule {
    backend_address_pool_name  = local.backend_address_pool_name
    backend_http_settings_name = local.backend_http_settings_name
    http_listener_name         = local.http_listener_name
    name                       = local.request_routing_rule_name
    priority                   = 8
    rewrite_rule_set_name      = local.rewrite_rule_set_name
    rule_type                  = "Basic"
  }

  // potential list of request headers to pass to backend pool
  // https://learn.microsoft.com/en-us/azure/application-gateway/rewrite-http-headers-url#server-variables
  // mTSL https://learn.microsoft.com/en-us/azure/application-gateway/rewrite-http-headers-url#mutual-authentication-server-variables
  rewrite_rule_set {
    name = local.rewrite_rule_set_name
    rewrite_rule {
      name          = "client_certificate"
      rule_sequence = 102
      condition {
        ignore_case = true
        negate      = false
        variable    = "var_client_certificate_subject"
        pattern     = "CN=(.*?)[,|$]"
      }
      request_header_configuration {
        header_name  = "x-client-cn"
        header_value = "{var_client_certificate_subject_1}"
      }
    }

    rewrite_rule {
      name          = "client_certificate_mtls"
      rule_sequence = 100
      request_header_configuration {
        header_name  = "x-client-certificate"
        header_value = "{var_client_certificate}"
      }
      request_header_configuration {
        header_name  = "x-client-certificate-end-date"
        header_value = "{var_client_certificate_end_date}"
      }
      request_header_configuration {
        header_name  = "x-client-certificate-fingerprint"
        header_value = "{var_client_certificate_fingerprint}"
      }
      request_header_configuration {
        header_name  = "x-client-certificate-issuer"
        header_value = "{var_client_certificate_issuer}"
      }
      request_header_configuration {
        header_name  = "x-client-certificate-serial"
        header_value = "{var_client_certificate_serial}"
      }
      request_header_configuration {
        header_name  = "x-client-certificate-start-date"
        header_value = "{var_client_certificate_start_date}"
      }
      request_header_configuration {
        header_name  = "x-client-certificate-subject"
        header_value = "{var_client_certificate_subject}"
      }
      request_header_configuration {
        header_name  = "x-client-certificate-verification"
        header_value = "{var_client_certificate_verification}"
      }
    }
  }
  sku {
    capacity = 2
    name     = "WAF_v2"
    tier     = "WAF_v2"
  }

  waf_configuration {
    enabled          = false
    firewall_mode    = "Detection"
    rule_set_type    = "OWASP"
    rule_set_version = "3.1"
    # file_upload_limit_mb = 100
    # max_request_body_size_kb = 128
    # request_body_check = true
  }

```
