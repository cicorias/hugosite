---
title: "Reminder: quick cleanup of Docker images..."
date: 2016-08-19T13:10:50+0000
lastmod: 2016-08-19T13:10:50+0000
slug: "reminder-quick-cleanup-of-docker-images"
feature_image: "https://www.cicoria.com/content/images/2016/08/homepage-docker-logo.png"
aliases:
  - /reminder-quick-cleanup-of-docker-images/
---

```
docker rm --force $(docker ps -q -s)
docker rmi --force $(docker images -q)

```
