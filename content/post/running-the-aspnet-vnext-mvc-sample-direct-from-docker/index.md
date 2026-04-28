---
title: "Running the AspNet vNext MVC sample direct from Docker"
date: 2014-11-24T03:51:24+0000
lastmod: 2014-11-24T03:51:24+0000
slug: "running-the-aspnet-vnext-mvc-sample-direct-from-docker"
aliases:
  - /running-the-aspnet-vnext-mvc-sample-direct-from-docker/
---

In the post

[Using the Docker client from Windows and getting AspNet vNext running in a Docker Container](http://blogs.msdn.com/b/scicoria/archive/2014/11/23/using-the-docker-client-from-windows-and-getting-aspnet-vnext-running-in-a-docker-container.aspx) you had to step through downloading GO, building the docker.exe, etc.

I’ve updated the GitHub repo adding the hacked version of the Docker.exe along with their LICENSE.

And the whole thing has been published to the Docker hub registry.

So, all you need to do is run the following (assuming you have a Docker host running):

```
docker run -d -t -p 8080:5004 cicorias/dockermvcsample2
```

This will get you a running AspNet vNext on Linux and a Sample MVC app.

Note that temporary workaround in the approach is TAR all the files 1st – and use that in the Dockerfile.

[https://github.com/cicorias/dockerMvcSample](https://github.com/cicorias/dockerMvcSample "https://github.com/cicorias/dockerMvcSample")

[https://registry.hub.docker.com/u/cicorias/dockermvcsample2/](https://registry.hub.docker.com/u/cicorias/dockermvcsample2/ "https://registry.hub.docker.com/u/cicorias/dockermvcsample2/")
