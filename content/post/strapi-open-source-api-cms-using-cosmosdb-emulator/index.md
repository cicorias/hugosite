---
title: "Strapi Open Source API CMS using Azure CosmosDB Emulator"
date: 2018-12-15T22:47:51+0000
lastmod: 2018-12-15T22:49:10+0000
slug: "strapi-open-source-api-cms-using-cosmosdb-emulator"
feature_image: "https://www.cicoria.com/content/images/2018/12/strapi.png"
aliases:
  - /strapi-open-source-api-cms-using-cosmosdb-emulator/
---

I've recently started looking at [Strapi](https://strapi.io/). Their default samples look for MongoDB instances. But I wanted to see if it would work with the [Azure CosmosDB Emulator](https://docs.microsoft.com/en-us/azure/cosmos-db/local-emulator) - then how it works with [Azure CosmosDB](https://docs.microsoft.com/en-us/azure/cosmos-db/).

So far, it's worked flawlessly...

## Setup

Once you `git clone` the samples from the [Strapi Samples](https://github.com/strapi/strapi-examples) - you need to edit the `database.json` file for the environment you're in. For local development, that's going to be development.

In the directory of the sample app `hello-world` - edit the `config\environments\development\database.json` file.

For the settings below, run the **Azure CosmosDB emulator** then launch the ***Data Explorer*** - that will show a website with the connection string and key.  
![explorer](https://cicoria.blob.core.windows.net/blog/2018-12/dataexplorer.png)

Also, create a new Database called `strapi` with a collection - call it anything as the tool requires it. It can be deleted later as the sample apps from Strapi will create their own collections.

![dbs](https://cicoria.blob.core.windows.net/blog/2018-12/dbs.png)

- **PORT** - examine the Mongo connection string - you'll see the port near the end prefixed by a `:` -- in mine it was `localhost:10255`
- **Database** - enter *`strapi`* as that was used in the create database / collection before.
- **Username**: `localhost`
- **Password**: from the "key" - this is also in the mongo connection string but URL encoded.

```
{
  "defaultConnection": "default",
  "connections": {
    "default": {
      "connector": "strapi-mongoose",
      "settings": {
        "client": "mongo",
        "host": "127.0.0.1",
        "port": 10255,
        "database": "strapi",
        "username": "localhost",
        "password": "C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw==",
        "authenticationDatabase": "",
        "ssl": true
      },
      "options": {}
    }
  }
}

```

That's it.
