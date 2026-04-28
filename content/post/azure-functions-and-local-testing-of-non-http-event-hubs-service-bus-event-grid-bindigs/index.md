---
title: "Azure Functions and local testing of non-HTTP - Event Hubs, Service Bus, Event Grid bindigs"
date: 2022-10-07T14:22:30+0000
lastmod: 2022-10-07T14:23:36+0000
slug: "azure-functions-and-local-testing-of-non-http-event-hubs-service-bus-event-grid-bindigs"
draft: true
aliases:
  - /azure-functions-and-local-testing-of-non-http-event-hubs-service-bus-event-grid-bindigs/
---

The magical endpoint and format.

![](https://learn.microsoft.com/en-us/media/logos/logo-ms-social.png)
```
Run your Event Grid function locally. The Content-Type and aeg-event-type headers are required to be manually set, while and all other values can be left as default.

Use a tool such as Postman or curl to create an HTTP POST request:

Set a Content-Type: application/json header.

Set an aeg-event-type: Notification header.

Paste the RequestBin data into the request body.

Post to the URL of your Event Grid trigger function.
```

<http://localhost:7071/runtime/webhooks/eventgrid?functionName={FUNCTION_NAME}>
