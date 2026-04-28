---
title: "ssh annoyance -- strict mode and known_hosts cleanup"
date: 2019-12-07T15:16:36+0000
lastmod: 2019-12-07T15:16:36+0000
slug: "ssh-annoyance-strict-mode-and-known_hosts-cleanup"
feature_image: "/images/2019/12/Annotation-2019-12-07-151541.jpg"
aliases:
  - /ssh-annoyance-strict-mode-and-known_hosts-cleanup/
---

Often when using DNS names behind dynamic IP addresses the IP address might change. But the default for ssh is to ensure that the IP address still matches -- well, kinda annoying but "proper".

You can clean a host using `ssh-keygen` as below:

```
ssh-keygen -f "/home/cicorias/.ssh/known_hosts" -R "scicoriahdicluster-ssh.azurehdinsight.net"

```

Windows or PowerShell -

```
ssh-keygen -f "/Users/cicor/.ssh/known_hosts" -R "scicoriahdicluster-ssh.azurehdinsight.net"

```

Or, just use the `ssh -o`  flag:

```
ssh -o StrictHostKeyChecking=no user@myhostname.com

```
