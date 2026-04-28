---
title: "Getting Docker Running on Hyper-V 8.1/ 2012 R2"
date: 2014-10-09T13:23:20+0000
lastmod: 2014-10-09T13:23:20+0000
slug: "getting-docker-running-on-hyper-v-8-1-2012-r2"
aliases:
  - /getting-docker-running-on-hyper-v-8-1-2012-r2/
---

Running [Docker](https://docker.com/) locally on a Windows machine is generally not an issue; unless you've committed to using Hyper-V. Since the [Docker](https://docker.com/) install for Windows relies on Sun's Oracle's Virtual Box, you can't have both running (Hyper-V and Virtual Box).

There are ways to disable Hyper-V for a boot session (via bcdedit for example – [here](http://blogs.msdn.com/b/virtual_pc_guy/archive/2008/04/14/creating-a-no-hypervisor-boot-entry.aspx)). However, I'd just like to run in Hyper-V.

Thankfully, [Chris Swan has a nice post](http://blog.thestateofme.com/2014/02/18/boot2docker-on-hyper-v/) on getting started, using the Boot2Docker ISO, and setting up the data disk (via a differencing disks) so you can just re-use this config in future Docker instances. You can also see some of the details on the boot2docker requirements for naming of the data disk, username and password for SSH, etc. here:

- <https://github.com/boot2docker/boot2docker>
- <http://docs.docker.com/installation/windows/>

## Basic Steps

### Download ISO – from github <https://github.com/steeve/boot2docker/releases>

### Create the VM and just use the ISO for bootup – we'll add the disk in a moment

We'll create the VM as a Generation 1 – we need the legacy adapters etc. as the version of CoreOS used won't recognize the other adapter types.

![](http://cicoria.blob.core.windows.net/blog/images/DockerHyperV-0025.png)

### Simple Settings:

**Memory Size**: 1,204 MB

**Network Connection**: Choose an interface that has Internet access and DHCP assignable addresses for ease:

![](http://cicoria.blob.core.windows.net/blog/images/DockerHyperV-0023.png)

**Next, postpone the setup of the Hard Disk as we're going to setup a differencing disk and we'd like some control over the IDE adapter / Port to use.**

![](http://cicoria.blob.core.windows.net/blog/images/DockerHyperV-0022.png)

### Once you're done with the 'New Virtual Machine' Wizard, hop into settings for the VM

Modify the DVD settings to point to the ISO image that you downloaded above:

![](http://cicoria.blob.core.windows.net/blog/images/DockerHyperV-0020.png)

## Boot the VM for the First Time

All goes right, you should see in the VM console the 'bootdocker' loader information, and eventually the linux prompt

![](http://cicoria.blob.core.windows.net/blog/images/DockerHyperV-0019.png)

![](http://cicoria.blob.core.windows.net/blog/images/DockerHyperV-0018.png)

### Start a SSH session with your VM (if desired)

To get the IP address of the VM, run ifconfig eth0 to see the default adapter. You should get an address that is hopefully on the Network interface/LAN that you chose. This has to be accessible from your host OS if you want to use SSH – in fact, it also needs access to the internet in order to get to the Docker HUB for downloading images.

![](http://cicoria.blob.core.windows.net/blog/images/DockerHyperV-0016.png)

I use "github" Windows tools (which in turn sets up the 'poshgit' tools, etc.) so I can just run a SSH session from PowerShell. <https://windows.github.com/>

### Initiate the connection normally with SSH

> ssh [docker@<IP.address](mailto:docker@%3cIP.address)>

Note that the default username / password is : docker / tcuser - see the section on SSH at <https://github.com/boot2docker/boot2docker> for more information.

![](http://cicoria.blob.core.windows.net/blog/images/DockerHyperV-0014.png)

## Setup the Virtual Disk

Shutdown the VM.

The next step is following what Chris Swan did in his post – which is to setup the VHD – run through the initialization, then make a differencing disk based off of that VHD, then swap out the configuration settings on the VM to use the Differencing disk instead of the base.

![](http://cicoria.blob.core.windows.net/blog/images/DockerHyperV-0013.png)

## Boot the VM again

Once it's started, choose SSH or the console to perform the disk preparation

### Partition the drive

The steps below are slightly different than Chris' post – but are:

1. Dump out the partition table just to be sure

   1. cat /proc/partions (if you chose IDE 0 / PORT 0 then it should be /dev/sda)
2. run fdisk

   1. sudo fdisk /dev/sda
3. Choose 'extended'
4. Select partition '1'
5. Choose the defaults for the first and last cylinder
6. Once that is done, commit with the 'w' command

![](http://cicoria.blob.core.windows.net/blog/images/DockerHyperV-0011.png)

### Setup the file system

The naming convention of the disk is also specified on the boot2docker github page – but it has to be 'boot2docker-data'

Next, format the drive with:

```
sudo mkfs.ext4 -L boot2docker-data /dev/sda

```

Note that you will be warned about formatting the entire device, and not a partition. For now, I just went with the above.

## Create the Differencing Disk

Shut down the VM again

Go back into the Virtual Machine Wizard. Select the settings for the VM, then go to the Disk settings and create a "New Virtual Disk".

Make sure when prompted, you choose the "base" image you created before, but when you're done, your "Differencing" disk should be what's listed in the Hard Disk path for the Controller/Location as below.

![](http://cicoria.blob.core.windows.net/blog/images/DockerHyperV-0004.png)

## Boot the VM – 3rd time

I think it's the 3rd time – don't remember at this point…

Now we're ready to "run" something. We'll use the same image that Chris posted about, just because it's a cool tool (Node-RED - <http://nodered.org/>)

Access the image either through the console or via SSH

Do a 'docker run' specifying to download the image if needed (-d) as it's won't be in the image local library.

```
docker run –d –p 1880:1880 cpswan/node-red

```

If all is working, then you should see the image and all it's dependencies downloading – with the container – and at the end, docker launches the process.

![](http://cicoria.blob.core.windows.net/blog/images/DockerHyperV-0006.png)

## Checkout if the Differencing disk is working

The "before" size

![](http://cicoria.blob.core.windows.net/blog/images/DockerHyperV-0005.png)

The "after" size – note the increase of the Differencing disl.

![](http://cicoria.blob.core.windows.net/blog/images/DockerHyperV-0000.png)

## Launch the Application

Note that the port mapping is using the same port 1880 (Nat'd).

You should get the 'Node-Red' home page, which is the designer surface.

I quickly imported a simple "hello world" from the flows <http://flows.nodered.org/flow/8069baf59dcb258bb2bd>

![](http://cicoria.blob.core.windows.net/blog/images/DockerHyperV-0002.png)

![](http://cicoria.blob.core.windows.net/blog/images/DockerHyperV-0001.png)
