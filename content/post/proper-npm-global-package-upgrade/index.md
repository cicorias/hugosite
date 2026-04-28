---
title: "Proper npm Global Package Upgrade"
date: 2016-12-30T16:03:31+0000
lastmod: 2016-12-30T16:03:31+0000
slug: "proper-npm-global-package-upgrade"
feature_image: "https://www.cicoria.com/content/images/2016/12/tokyo-wombat-1200x.jpg"
aliases:
  - /proper-npm-global-package-upgrade/
---

Per the npm [documentation](https://docs.npmjs.com/getting-started/updating-global-packages), this is the script to use:

Here's the [gist](https://gist.github.com/othiym23/4ac31155da23962afd0e)

```javascript
#!/bin/sh

set -e
set -x

for package in $(npm -g outdated --parseable --depth=0 | cut -d: -f2)
do
    npm -g install "$package"
done

```
