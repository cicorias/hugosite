---
title: "DotNet Core Building Docker SDK Missing."
date: 2021-07-01T18:03:42+0000
lastmod: 2021-07-09T09:44:02+0000
slug: "dotnet-core-building-docker-sdk-missing"
tags: ["azure", "cloud", "containers"]
feature_image: "/images/2021/07/1_MdsKZZDjdYBtRBcBJmj43w.jpeg"
aliases:
  - /dotnet-core-building-docker-sdk-missing/
---

If you see this

```
/src/docker-compose.dcproj : error MSB4236: The SDK 'Microsoft.Docker.Sdk' specified could not be found.

```

Or something similar, you can update the base image to the following.

## Docker Hub

Look at the Tags and what's in the Dockerfile

First update your project...

```
ci-build_1  | /usr/share/dotnet/sdk/1.1.0/Sdks/Microsoft.NET.Sdk/build/Microsoft.NET.TargetFrameworkInference.targets(112,5): error : The current .NET SDK does not support targeting .NET Core 2.0.  Either target .NET Core 1.1 or lower, or use a version of the .NET SDK that supports .NET Core 2.0. [/src/EhReceiver/EhReceiver.csproj]
ci-build_1  | /usr/share/dotnet/sdk/1.1.0/Sdks/Microsoft.NET.Sdk/build/Microsoft.NET.TargetFrameworkInference.targets(112,5): error : The current .NET SDK does not support targeting .NET Core 2.0.  Either target .NET Core 1.1 or lower, or use a version of the .NET SDK that supports .NET Core 2.0. [/src/EhSender/EhSender.csproj]

```
> \docker-compose.ci.build.yml

```
version: '3'

services:
  ci-build:
    image: microsoft/aspnetcore-build:1.0-2.0-2017-08
    volumes:
      - .:/src
    working_dir: /src
    command: /bin/bash -c "dotnet restore ./EhubTester.sln && dotnet publish ./EhubTester.sln -c Release -o ./obj/Docker/publish"

```
