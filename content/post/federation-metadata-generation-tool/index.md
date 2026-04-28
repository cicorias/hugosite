---
title: "Federation Metadata Generation Tool"
date: 2010-08-18T15:13:28+0000
lastmod: 2010-08-18T15:13:28+0000
slug: "federation-metadata-generation-tool"
aliases:
  - /federation-metadata-generation-tool/
---

***Disclaimer: Use at your own risk – no warranties are granted or implied***

**UPDATE**: this has been moved to Github here: <https://github.com/cicorias/federationmetadatagenerator>

If you’ve worked with Windows Identity Foundation (WIF) without the help of ADFS 2.0, you’ll run into situations where you’ll need to potentially generate or regenerate the metadata used for federation.

Additionally, while WIF supports SAML tokens, it doesn’t have support for SAML Passive Requestor protocol (urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST)  - you get that with ADFS 2.0.

So, I needed the ability to quickly generate meta-data and regenerate as needed.  I created a very simple tool – hacked in a few hours - that uses the meta data serialization support in WIF (MetadataSerializer) to generate the meta data.

So, this tool will generate the following metadata

[Download](https://www.cicoria.com/downloads/FederationMetadataGenerator.zip)

SAML IdP and SP

- IDPSSODescriptor "urn:oasis:names:tc:SAML:2.0:protocol"
- SPSSODescriptor "urn:oasis:names:tc:SAML:2.0:protocol"

And WS-Federation

- http://docs.oasis-open.org/wsfed/federation/200706

The tool makes use of the PropertyGrid for binding to some types used to generate, and in order to read the certificate private key it needs permissions – if you run elevated, you should have access.

[![image](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/7115.image_thumb_23683378.png "image")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/2248.image_4678A4E8.png)

[![image](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/5556.image_thumb_6EE7612F.png "image")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/0272.image_6259B413.png)
