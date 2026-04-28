---
title: "Using BlobOutput and EventHubTrigger bindings with System Properties in Java Azure Functions"
date: 2022-08-25T16:51:21+0000
lastmod: 2022-08-25T16:52:14+0000
slug: "using-bloboutput-and-eventhubtrigger-bindings-with-system-properties"
tags: ["azure", "cloud", "java", "functions", "eventhub"]
feature_image: "https://www.cicoria.com/content/images/2022/08/func-eh.png"
aliases:
  - /using-bloboutput-and-eventhubtrigger-bindings-with-system-properties/
---

One of the nice developer features of Azure Functions is the Bindings that provide pre-baked code and logic to help manage events inbound or sending things outbound

However, much of the documentation is centered around C# and I found it difficult to find any clear Java examples that use EventHub and Blob output.

So, after bunch of debugging and spelunking, I created a simple Azure Function in Java the illustrates pulling in System and Custom properties from the Event Hub message.

Adding to this is writing the output to Blob Storage using a best practice of slash separation such as `YY/MM/DD/hh/mm/partition/item.json`. The reason for this is the Storage API search provides a "prefix" option to narrow down the search, and tools such as Azure Stream Analytics strongly suggest this approach, so it doesn't have to enumerate ALL files to find the files within their window of search.

Here is the entire listing of the Function in Java:

```java
package com.shawn;

import java.util.Map;
import java.time.ZonedDateTime;

import com.microsoft.azure.functions.annotation.*;
import com.microsoft.azure.functions.*;

/**
 * Azure Functions with Event Hub trigger.
 * and Blob Output using date in path along with sequenct and partition ID
 */
public class EventHubReceiver {

    @FunctionName("EventHubReceiver")
    @StorageAccount("bloboutput") // unfortunately this won't work with Azurite emulator - unknown issue
                                  // see https://github.com/microsoft/AzureStorageExplorer/issues/6008
    public void run(
            @EventHubTrigger(name = "message",
                eventHubName = "%eventhub%",
                consumerGroup = "%consumergroup%",
                connection = "eventhubconnection",
                cardinality = Cardinality.ONE)
            String message,
            
            final ExecutionContext context,
            
            @BindingName("Properties") Map<String, Object> properties,
            @BindingName("SystemProperties") Map<String, Object> systemProperties,
            @BindingName("PartitionContext") Map<String, Object> partitionContext,
            @BindingName("EnqueuedTimeUtc") Object enqueuedTimeUtc,

            @BlobOutput(
                name = "outputItem",
                path = "iotevents/{datetime:yy}/{datetime:MM}/{datetime:dd}/{datetime:HH}/" +
                       "{datetime:mm}/{PartitionContext.PartitionId}/{SystemProperties.SequenceNumber}.json")
            OutputBinding<String> outputItem) {

        var et = ZonedDateTime.parse(enqueuedTimeUtc + "Z"); // needed as the UTC time presented does not have a TZ
                                                             // indicator
        context.getLogger().info("Event hub message received: " + message + ", properties: " + properties);
        context.getLogger().info("Properties: " + properties);
        context.getLogger().info("System Properties: " + systemProperties);
        context.getLogger().info("partitionContext: " + partitionContext);
        context.getLogger().info("EnqueuedTimeUtc: " + et);

        outputItem.setValue(message);
    }
}
```

And the full Project is up here on GitHub [cicorias/azfunct-java-eventhubs (github.com)](https://github.com/cicorias/azfunct-java-eventhubs)

## Items of Note

One interesting item is the Enqueue Date Time while in UTC doesn't have a Time zone suffix of `Z`  (for UTC or zulu time) – so, for that you can't just using `@Bindingname` to a Date Time data type – as it fails the Google gson deserialization indicating it's missing a `TZ` indicator.

The documentation is quite Queue centric – never really showing methods for binding to EventHub meta-data – see here: [Azure Functions bindings expressions and patterns | Microsoft Docs](https://docs.microsoft.com/en-us/azure/azure-functions/functions-bindings-expressions-patterns#trigger-metadata)

Also note the use of percentage signs that allow externalizing values in App Settings. A sample `local.settings.json` file is provided so update that to your environment needs.

You'll also note that I used Azure Storage Emulator Azurite – unfortunately, there's some off known issue with missing MD5 hash values that is a regression – the issue is noted in the source code and hopefully that's fixed soon.

## Event Hub Sender

I also added in a folder under `./tools` a TypeScript node app that sends a couple of messages to the EventHub of your choice – this is helpful for testing.
