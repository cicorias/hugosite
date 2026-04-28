---
title: "Simple Azure Blob Storage Performance (upload) testing"
date: 2015-09-17T09:48:49+0000
lastmod: 2015-09-17T09:48:49+0000
slug: "simple-azure-blob-storage-performance-upload-testing"
aliases:
  - /simple-azure-blob-storage-performance-upload-testing/
---

# Azure Blob Storage Perf Testing Tool

This is a simple testing tool using Mocha that provides upload speed testing when modifying the [parallelOperationThreadCount](https://github.com/Azure/azure-storage-node/blob/631beb481733ecb8ef0656aff7853c98342f5703/ChangeLog.txt)   
setting that is available in the [Azure Storage Nodejs tools](https://github.com/Azure/azure-storage-node).

## Setup

### Install Nodejs and npm for your environment

Review what [Nodejs.org](http://nodejs.org) says for your environment in order to get Nodejs and npm running.

### Clone the repo

```
git clone https://github.com/cicorias/blobTool
chdir blobTool
npm install
```

Run the mocha test

```
npm test
```

### Review the `package.json`

This file will show what the script calls - this uses babel-core to polyfill ES6 support
  
and runnable on node >=10.x

```json
{
  "name": "blobtool",
  "version": "1.0.0",
  "description": "Simple Blob upload check",
  "main": "app.js",
  "scripts": {
    "start": "node ./app.js",
    "test": "node ./node_modules/mocha/bin/mocha --compilers js:babel/register"
  },
  "author": "shawn cicoria",
  "license": "ISC",
  "dependencies": {
    "azure-storage": "^0.5.0",
    "nconf": "^0.7.2",
    "node-uuid": "^1.4.3"
  },
  "devDependencies": {
    "babel": "^5.8.23",
    "babel-core": "^5.8.24",
    "mocha": "^2.3.2",
    "performance-now": "^0.2.0",
    "qunit": "^0.7.6"
  }
}
```

## Configuration

The `config.1.json` file needs to be updated to include your test container name, storage account name, and the storage key.

```json
{
    "CONTAINER_NAME" : "<containername>",
    "STORAGE_NAME": "<storageaccount>",
    "STORAGE_KEY": "<key>"
}
```

## Example test results

Below are some console output captures of results.
  
Note that for the most part anything above 2 parallel operations is really not helping. Perhaps 3. Note that the

service limit on Standard Storage is 60 MBS see [this](https://azure.microsoft.com/en-us/documentation/articles/azure-subscription-service-limits/#storage-limits) for more information.

The tests were run from East -> East 2 to hopefully accomplish eliminating things like my ISP’s stuff, keep it on the Azure backbone, but also from something other than the direct Region / Datacenter.

### From local Mac

![local mac](https://raw.githubusercontent.com/cicorias/blobTool/master/assets/local.png)

### From an A2 machine

![A2 in East to East2](https://raw.githubusercontent.com/cicorias/blobTool/master/assets/a2.png)

### From an A8 machine

![A8 in East to East2](https://raw.githubusercontent.com/cicorias/blobTool/master/assets/a8.png)
