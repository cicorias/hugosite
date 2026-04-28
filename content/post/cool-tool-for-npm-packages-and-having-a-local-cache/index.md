---
title: "Cool tool for npm packages and having a local cache"
date: 2017-07-28T11:49:55+0000
lastmod: 2017-07-28T11:51:15+0000
slug: "cool-tool-for-npm-packages-and-having-a-local-cache"
feature_image: "/images/2017/07/two.png"
aliases:
  - /cool-tool-for-npm-packages-and-having-a-local-cache/
---

[Verdaccio](https://github.com/verdaccio/verdaccio), a fork of [Sinopia](https://github.com/rlidwka/sinopia), to the rescue...

use with each command or set forever...

```
npm install --registry http://localhost:4978

```

Good also to know that sometimes the HTTPS connections are that much slower (airplane Wifi); for that use the non-TLS endpoint:

```
npm install --registry http://registry.npmjs.org/ FOOBAR

```
