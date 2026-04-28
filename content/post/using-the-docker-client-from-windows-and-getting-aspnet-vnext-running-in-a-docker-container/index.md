---
title: "Using the Docker client from Windows and getting AspNet vNext running in a Docker Container"
date: 2014-11-23T09:46:32+0000
lastmod: 2014-11-23T09:46:32+0000
slug: "using-the-docker-client-from-windows-and-getting-aspnet-vnext-running-in-a-docker-container"
aliases:
  - /using-the-docker-client-from-windows-and-getting-aspnet-vnext-running-in-a-docker-container/
---

**Update: 2015-01-15** – Note that Ahmet has posted an official Docker walkthrough for ASP.NET 5 <http://blogs.msdn.com/b/webdev/archive/2015/01/14/running-asp-net-5-applications-in-linux-containers-with-docker.aspx>

**Update: 2014-11-24** – Added links to HOWTO build Docker on Windows from Ahmet.

As Docker progress as a native application on Windows, and Asp.NET progresses direct from Microsoft for running on Linux, I wanted to see how far I could get using what’s out there today. While there are some challenges, there are a couple of simple steps that you can use to get around some initial blockers.

There are known issues in the Docker Windows implementation [[Github pull request 9113](https://github.com/docker/docker/pull/9113)] – specifically, the use of Path separators – in that in Linux we have ‘/’ and in Windows it’s ‘\’. While GO has a constant for this, the Docker client and server are not handling this platform translation just yet. **The trick for this is just TAR up your directory first, then use the ADD Dockerfile command which can handle TAR files natively.**

The other key change is downgrading the VERSION number so the client matches the Boot2Docker versions.  While I didn’t see any API changes that would impact this other than the version number.

Here’s an image of it running on a Docker host container (running on Hyper-V Windows 8.1).  Getting here was a bit challenging, but worth it ![Smile](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/1104.wlEmoticon-smile_363DE18E.png)

github repo here: [https://github.com/cicorias/dockerMvcSample](https://github.com/cicorias/dockerMvcSample "https://github.com/cicorias/dockerMvcSample")

[![image](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/7220.image_thumb_1A9BE649.png "image")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/4667.image_63BF0151.png)

**Here are the general steps that I followed:**

### Follow boot2docker on Hyper-V setup steps

In the post [here](http://blogs.msdn.com/b/scicoria/archive/2014/10/09/getting-docker-running-on-hyper-v-8-1-2012-r2.aspx) you can use that to get Docker via Boot2Docker running in HyperV. Again, all you need is a Docker host, but if you want to be all HyperV this is a way to do it.

### Modify Docker client version ‘server 1.15’ (HACK)

Ahmet goes through the HOWTO on building the Docker client – here: <https://ahmetalpbalkan.com/blog/compiling-docker-cli-on-windows/>.

GO is from here: <https://golang.org/>   
   
Follow the steps to install GO, then clone the Docker git repo – and make a small change to the version number so you’ll be able to attach with the Native client (which is being built against the dev branch from Docker’s Github repo. The Boot2Docker server is still at the prior version.  See the comments in the pull request above where some folks have indicates similar approach.

```
C:\gopath\src\github.com\docker\docker\api\common.go
const (
	APIVERSION        version.Version = "1.15"
  
```

### Build Docker client with GO

Once you have the docker.exe built, you can put it away safely and kill the repo if you want.

### Turn off TLS if you like a simple command line

I turn off TLS for development.  see <https://github.com/boot2docker/boot2docker/blob/master/README.md>

“disable it by adding DOCKER\_TLS=no to your/var/lib/boot2docker/profile file on the persistent partition inside the Boot2Docker virtual machine (use boot2docker ssh sudo vi /var/lib/boot2docker/profile).”

if you don’t turn it off, you can use TLS and just copy over to your Windows machien the following files then reference them from the ‘docker’ command line or set the environment variables.

### If using TLS ‘steal’ the following files from your boot2docker host

The following files sit on the Docker host in **/var/lib/boot2docker**

- cert.pem
- key.pem
- ca.pem

[![image](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/7268.image_thumb_49ED5BD3.png "image")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/3146.image_43A68545.png)

If you need to SSH into the Docker image:

> **ssh** [**docker@192.168.1.165**](mailto:docker@192.168.1.165)
>
> **Password: tcuser**

### Run docker client to verify access to your Docker host

Using the Docker client that you built from the GO source (and the hacked version #)

If you set an environment variable, you can avoid passing command line parms each time.

Note that the non-secure port is 2375 by default, and the secure port is 2376.

```
E:\gitrepos\dockerAspNet>set dock
DOCKER_HOST=tcp://192.168.1.165:2375
```

If you’re running via TLS, you can use the Certificate files that are located on the Server and mentioned above:

```
docker --tls --tlscert="e:\\temp\\docker\\cert.pem" --tlskey="e:\\temp\\docker\\key.pem" --tlscacert="e:\\temp\\docker\\ca.pem" ps
  
```

## Getting ASP.NET vNext running

Now for the fun part.

#### First, grab (clone) the github repo at:

git clone [https://github.com/aspnet/Home.git](https://github.com/aspnet/Home.git "https://github.com/aspnet/Home.git")

#### Tar files into 1 archive

Then in the ./samples/HelloMvc directory using a tool (such as 7-zip) to ‘tar’ up all the files so you have a ‘HelloMvc.tar’ file. This step is needed until the Docker client/daemon properly addresses File Separator differences between Windows and Linux.

### Create a ‘Dockerfile’ with the following:

```
FROM microsoft/aspnet
# copy the contents of the local directory to /app/ on the image
ADD HelloMvc.tar /app/

RUN ls -l

# set the working directory for subsequent commands

WORKDIR app  

RUN ls -l

# fetch the NuGet dependencies for our application

RUN kpm restore

# set the working directory for subsequent commands

# expose TCP port 5004 from container

EXPOSE 5004

# Configure the image as an executable

# When the image starts it will execute the “k web” command

# effectively starting our web application

# (listening on port 5004 by default)

ENTRYPOINT ["k", "kestrel"]

```

Once this is done the directory should look like this:

[![image](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/1348.image_thumb_0E3053D1.png "image")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/5621.image_00CA40CB.png)

## Build the Docker package

Now, from the root of the repo (./dockerAspNet/samples in my example) execute the following:

```
docker build -t myapp samples/HelloMvc
```

At this point, you should see Asp.NET and all the supporting dependencies fly by in the build interactive console. It will take a bit a time the first time as it will install the ‘**microsoft/aspnet’ docker** package too. Once that is done, future updates will be faster just for you’re package.

After a bit, you should see something like the following.

[![SNAGHTML2041d3e](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/2474.SNAGHTML2041d3e_thumb_31EC0C1C.png "SNAGHTML2041d3e")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/8625.SNAGHTML2041d3e_2249705A.png)

## Startup the Container

Now we’re ready to start our MVC app on ASP.NET in our Docker Container on Linux!!!!

```
docker run -d -t -p 8080:5004 myapp
  
```

[![image](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/2816.image_thumb_4AEA6D12.png "image")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/4454.image_2FB21411.png)

### Navigate to your IP address of your Linux instance:

As Martha Stewart would say – “It’s a good thing…”

[![image](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/7462.image_thumb_536DCC5C.png "image")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/5468.image_3F54AFD3.png)
