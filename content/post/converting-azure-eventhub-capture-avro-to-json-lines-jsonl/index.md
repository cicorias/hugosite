---
title: "Converting Azure EventHub Capture AVRO to JSON Lines (JSONL)"
date: 2022-03-24T11:06:40+0000
lastmod: 2022-03-24T11:06:40+0000
slug: "converting-azure-eventhub-capture-avro-to-json-lines-jsonl"
summary: "quickly convert lots of avro files to json using eventhub capture files"
tags: ["azure", "cloud", "utilities"]
feature_image: "/images/2022/03/Apache_Avro_Logo.svg"
aliases:
  - /converting-azure-eventhub-capture-avro-to-json-lines-jsonl/
---

One of the notable features of EventHub is [EventHub Capture](https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-capture-overview). This automatically captures a set of messages (zero or more) into an [Apache Avro File](https://en.wikipedia.org/wiki/Apache_Avro) in a Storage Account Container of your choosing.

But using the AVRO files, even human reading, needs a little bit of help. This Python script helps convert each AVRO file that is > 508 bytes to a [JSON Lines](https://jsonlines.org/) file alongside the AVRO file. Here's an alternative way to download direct from Storage as well - <https://askpythonquestions.com/2021/04/07/how-to-convert-from-an-avro-file-to-a-json-file-which-was-originally-sent-as-raw-json-via-postman-through-azure-event-hub/>

What follows is the code, simple README.md along with the python requirements.txt.
