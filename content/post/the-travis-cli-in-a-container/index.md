---
title: "The Travis CLI in a Container"
date: 2018-08-05T01:41:19+0000
lastmod: 2018-08-05T01:41:19+0000
slug: "the-travis-cli-in-a-container"
feature_image: "/images/2018/08/image.png"
aliases:
  - /the-travis-cli-in-a-container/
---

I must be missing it, but I could never find the Travis CLI already built and published on Docker Hub. So, I just pulled together on.

It's really simple. Really the only complexity is passing in the `VOLUME` mappings (2 of them) when you run the container.

All is articulated in the [Docker Hub container page](https://hub.docker.com/r/cicorias/travis-cli/). But, here's the basics from the Readme.

### Travis CLI

The best documentation is in the repo [travis-ci/travis.rb](https://github.com/travis-ci/travis.rb#console). Note that this is a Ruby Gem, so the base container of this Dockerfile is the official Docker Hub Ruby image.

## Running

Two volumes `/data` and `/root/.travis` are defined.

The `/data` is where the Docker HOST (your machine) shouldprobably be mapped - this would have any scripts, data, etc. that is needed.

> NOTE: this is essentially your project directory

The `/root/.travis` is where any of Travis configuration options are store or end up...

## Example

From your home path, first we'll make some local directory and run a task

```
mkdir mywork
cd mywork

```

### macOS and Linux

This will use or create the `.travis` folder in your profile path.

```
docker run -it --rm -v `pwd`:/data -v $HOME/.travis:/root/.travis cicorias/travis-cli login

```

### Windows

This example creates a separate folder for the `.travis` profile infomration

> WARNING: this directory contains secrets / tokens and should never be shared and should have proper ACLs to prevent others from reading

```
docker run -it --rm -v C:\g\containers\travis-cli\travis:/root/.travis -v C:\g\containers\travis-cli\data:/data cicorias/travis-cli login

```

#### PowerShell (Windows for now)

This does the same as above, but uses PowerShell's `${PWD}` for the absolute path of the current working directory in the shell.

> WARNING: this directory contains secrets / tokens and should never be shared and should have proper ACLs to prevent others from reading

```
docker run -it --rm -v ${PWD}\travis:/root/.travis -v ${PWD}\data:/data cicorias/travis-cli login

```

### Verify Login persists

Since the `docker run` command used the `--rm` parameter, the container is removed after stopping. This makes the container itself stateless. All state needed should be saved to `/data` which is mapped to the host if the `-v` paramemter is passed properly. Same for the `.travis` volumne

Now, run a command `whomai` to see the logged on information

```
docker run -it --rm -v ${PWD}\travis:/root/.travis -v ${PWD}\data:/data cicorias/travis-cli whoami

```

For me my output was:

```
C:\travis-cli [master ≡ +1 ~1 -0 !]> docker run -it --rm -v ${PWD}\travis:/root/.travis -v ${PWD}\data:/data cicorias/travis-cli whoami
You are cicorias (Shawn Cicoria)

```
