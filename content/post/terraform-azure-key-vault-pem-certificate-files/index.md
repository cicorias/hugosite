---
title: "terraform azure key vault PEM certificate files"
date: 2023-01-28T22:54:29+0000
lastmod: 2023-01-28T22:55:25+0000
slug: "terraform-azure-key-vault-pem-certificate-files"
draft: true
aliases:
  - /terraform-azure-key-vault-pem-certificate-files/
---

```
###
# Root Certificate
# 
# Self-signed certificate that is used to sign client certificates along. Root certificate
# is later sent to the MQTT broker head in Event Grid for client verification.
###

resource "tls_private_key" "root_ca_key" {
  algorithm = var.certifcate_type
  rsa_bits  = var.certifcate_size
}

resource "tls_self_signed_cert" "root_ca_cert" {
  private_key_pem = tls_private_key.root_ca_key.private_key_pem
  allowed_uses = [
    "crl_signing", "client_auth", "cert_signing", "digital_signature", "content_commitment",
    "key_encipherment", "key_agreement", "email_protection"
  ]

  subject {
    common_name = var.root_ca_cert_common_name
  }

  # Configurable validity window. Renewing certs requires a different process to produce new certs
  # and distributed them among client devices.
  validity_period_hours = var.certifcate_validity_period_hours # 336.5 days?
  # CA certificate required for both signing certs and also, required for MQTT CA Certificates.
  is_ca_certificate    = true
  set_authority_key_id = true
  set_subject_key_id   = true
}

data "tls_certificate" "root_ca_cert_pem" {
  content = tls_self_signed_cert.root_ca_cert.cert_pem
}

# Output certificates to directory for later use for sample clients.
resource "local_sensitive_file" "root_ca_key_pem" {
  filename = "${local.cert_file_path}/${var.pem_name}-root.pem"
  content  = tls_private_key.root_ca_key.private_key_pem
}

# Output certificates to directory for later use for sample clients.
resource "local_sensitive_file" "root_ca_cert_pem" {
  filename = "${local.cert_file_path}/${var.pem_name}-signing.pem"
  content  = tls_self_signed_cert.root_ca_cert.cert_pem
}

###
# Client Certificates
# 
# Certificates signed by the root CA above, distributed to sample client applications.
###

resource "tls_private_key" "sample_client_keys" {
  for_each  = var.client_names
  algorithm = var.certifcate_type
  rsa_bits  = var.certifcate_size
}

resource "tls_cert_request" "sample_client_certs" {
  for_each        = var.client_names
  private_key_pem = tls_private_key.sample_client_keys[each.key].private_key_pem
  subject {
    # CN used for validating client certificate with the registered client.
    common_name = each.value
  }
}

resource "tls_locally_signed_cert" "sample_client_certs" {
  for_each = var.client_names
  allowed_uses = [
    "crl_signing", "client_auth", "digital_signature", "content_commitment",
    "key_encipherment", "key_agreement", "email_protection"
  ]
  ca_cert_pem        = tls_self_signed_cert.root_ca_cert.cert_pem
  ca_private_key_pem = tls_private_key.root_ca_key.private_key_pem
  cert_request_pem   = tls_cert_request.sample_client_certs[each.key].cert_request_pem

  # Configurable validity window. Renewing certs requires a different process to produce new certs
  # and distributed them among client devices.
  validity_period_hours = var.certifcate_validity_period_hours
  is_ca_certificate     = false
}

# Output certificates to directory for later use for sample clients.
resource "local_sensitive_file" "sample_client_key_pems" {
  for_each = var.client_names
  filename = "${local.cert_file_path}/${each.key}-private-key.pem"
  content  = tls_private_key.sample_client_keys[each.key].private_key_pem
}

# Output certificates to directory for later use for sample clients.
resource "local_sensitive_file" "sample_client_cert_pems" {
  for_each = var.client_names
  filename = "${local.cert_file_path}/${each.key}-cert.pem"
  content  = tls_locally_signed_cert.sample_client_certs[each.key].cert_pem
}

resource "local_sensitive_file" "full_cert" {
  for_each = var.client_names
  filename = "${local.cert_file_path}/${each.key}-full.pem"
  # content  = replace("${tls_private_key.sample_client_keys[each.key].private_key_pem}${tls_locally_signed_cert.sample_client_certs[each.key].cert_pem}","RSA ", "")
  content  = "${tls_private_key.sample_client_keys[each.key].private_key_pem}${tls_locally_signed_cert.sample_client_certs[each.key].cert_pem}"
  # join("", "${tls_locally_signed_cert.sample_client_certs[each.key].cert_pem}", "${tls_private_key.sample_client_keys[each.key].private_key_pem}")
}

# TODO: remove WIP
resource "local_sensitive_file" "pkcs8_contents" {
  for_each = var.client_names
  filename = "${local.cert_file_path}/${each.key}-pkcs8.pem"
  content  = tls_private_key.sample_client_keys[each.key].private_key_pem_pkcs8
}

resource "azurerm_key_vault_certificate" "client_cert" {
  for_each = var.client_names
  name = "${var.keyvault_cert_prefix}-${each.key}"
  key_vault_id = var.key_vault_id

  certificate {
    # contents = "${local.cert_file_path}/${each.key}-full.pem"
    # contents = base64encode(replace("${tls_private_key.sample_client_keys[each.key].private_key_pem}${tls_locally_signed_cert.sample_client_certs[each.key].cert_pem}", "RSA ", ""))
    # contents = base64encode("${tls_private_key.sample_client_keys[each.key].private_key_pem}${tls_locally_signed_cert.sample_client_certs[each.key].cert_pem}")
    # contents = "${tls_self_signed_cert.root_ca_cert.cert_pem}${tls_private_key.sample_client_keys[each.key].private_key_pem}${tls_locally_signed_cert.sample_client_certs[each.key].cert_pem}"
    # contents = replace("${tls_self_signed_cert.root_ca_cert.cert_pem}${tls_private_key.sample_client_keys[each.key].private_key_pem}${tls_locally_signed_cert.sample_client_certs[each.key].cert_pem}", "RSA ", "")
   
    # contents = "${tls_private_key.sample_client_keys[each.key].private_key_pem_pkcs8}"
    contents = "${tls_private_key.sample_client_keys[each.key].private_key_pem_pkcs8}${tls_locally_signed_cert.sample_client_certs[each.key].cert_pem}"
 
 
    # contents = base64encode("${tls_private_key.sample_client_keys[each.key].private_key_pem_pkcs8}")
    # contents = tls_private_key.test1.private_key_pem_pkcs8
    #contents = file("./secrets/test.pem")
    # password = ""
  }
  certificate_policy {
    key_properties {
      exportable = "true"
      key_size   = var.certifcate_size
      key_type   = var.certifcate_type
      reuse_key  = "true"
    }
    issuer_parameters {
      name = "Unknown"
    }
    secret_properties {
      content_type = "application/x-pem-file"
    }
  }

}

# TODO: make this not use the file system
# resource "azurerm_key_vault_certificate" "keyvault_cert_key" {
#   for_each = var.client_names
#   name = "${var.keyvault_cert_prefix}-${each.key}"
#   key_vault_id = var.key_vault_id

#   certificate {
    
#     # contents = base64encode(file("${local.cert_file_path}/${each.key}-cert.pem"))
#     //contents = base64encode(file("${local.cert_file_path}/c1.pem"))
#     # contents = base64encode(join("",file("${local.cert_file_path}/${each.key}-cert.pem"), file("${local.cert_file_path}/${each.key}-private-key.pem")))
#     # contents = filebase64(join("",file(,))
#     contents = filebase64("${local.cert_file_path}/${each.key}-full.pem")
#     password = ""
#   }

# }

```
