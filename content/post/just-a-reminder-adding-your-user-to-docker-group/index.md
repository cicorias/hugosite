---
title: "Just a reminder - adding your user to Docker group..."
date: 2016-08-15T21:23:21+0000
lastmod: 2016-08-15T21:23:21+0000
slug: "just-a-reminder-adding-your-user-to-docker-group"
feature_image: "/images/2016/08/mac-success.png"
aliases:
  - /just-a-reminder-adding-your-user-to-docker-group/
---

From a shell...

```
sudo groupadd docker
sudo usermod -aG docker $USER

```

Logout and on again - run

```
docker ps

```

If no errors, you should see what is running or just the headers.
