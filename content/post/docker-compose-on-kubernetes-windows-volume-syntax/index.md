---
title: "Docker Compose on Kubernetes - Windows Volume Syntax"
date: 2018-12-16T16:51:28+0000
lastmod: 2018-12-16T16:51:28+0000
slug: "docker-compose-on-kubernetes-windows-volume-syntax"
feature_image: "https://www.cicoria.com/content/images/2018/12/image-9.png"
aliases:
  - /docker-compose-on-kubernetes-windows-volume-syntax/
---

I've been looking at Docker Compose on Kubernetes, thanks to a pointer from my teammate [Clemens Wolff](https://www.linkedin.com/in/clemens-wolff/), and had a hard time with mapping the volumes from the host.

My first compose file looked like this:

```
# Use root/example as user/password credentials
version: '3.6'

services:
  mongo:
    image: mongo
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: example
    volumes: 
      - c:/g/learn/mongo/data:/data
    ports:
      - 27017:27017

  mongo-express:
    image: mongo-express
    ports:
      - 8080:8081
    environment:
      ME_CONFIG_MONGODB_ADMINUSERNAME: root
      ME_CONFIG_MONGODB_ADMINPASSWORD: example

```

But you'll see errors telling you that it's not an absolute path - WTF?

```
Stack.compose.docker.com "hellokube" is invalid: hellokube: Invalid value: "null": conversion to kube entities failed: 
only absolute paths can be specified in mount source      

```

Turns out you need to assume a linux mindset and must make the mapping

```
    volumes: 
      - c:/g/learn/mongo/data:/data

```

The full compose is here:

```
# Use root/example as user/password credentials
version: '3.6'

services:
  mongo:
    image: mongo
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: example
    volumes: 
      - /c/g/learn/mongo/data:/data
    ports:
      - 27017:27017

  mongo-express:
    image: mongo-express
    ports:
      - 8080:8081
    environment:
      ME_CONFIG_MONGODB_ADMINUSERNAME: root
      ME_CONFIG_MONGODB_ADMINPASSWORD: example

```
