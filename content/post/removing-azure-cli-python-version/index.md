---
title: "Removing Azure CLI (Python version)"
date: 2017-05-12T09:22:17+0000
lastmod: 2017-05-12T09:22:17+0000
slug: "removing-azure-cli-python-version"
feature_image: "https://www.cicoria.com/content/images/2017/05/python.jpg"
aliases:
  - /removing-azure-cli-python-version/
---

As with many developers churn happens. So, with the Azure CLI I had installed it previously using `pip`. However, that's no longer the recommend practice.

So, the Azure CLI installs many packages. I needed a 1 liner to uninstall the packages. This is what I used.

```
pip list --format=legacy |grep azure | cut -d ' ' -f 1 | xargs -L1 pip uninstall -y

```

Further cleanup, as Python has been messy on macOS of late is to fix the pip directories.

```
sudo chown -R $USER $HOME/Library/Logs/
sudo chown -R $USER $HOME/Library/Caches/

```
