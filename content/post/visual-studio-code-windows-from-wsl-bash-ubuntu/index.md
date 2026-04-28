---
title: "Visual Studio Code Windows from WSL Bash Ubuntu"
date: 2018-04-18T15:26:41+0000
lastmod: 2018-04-18T15:26:41+0000
slug: "visual-studio-code-windows-from-wsl-bash-ubuntu"
feature_image: "/images/2018/04/opengraph-home.png"
aliases:
  - /visual-studio-code-windows-from-wsl-bash-ubuntu/
---

If you're launching VS Code from the WSL prompt there are 2 annoyances. The first is the logging messages that appear. The second is it's blocked and doesn't return. While there are some issues and requests for PRs for me this is working for now.

```
alias vsc='nohup code . >/dev/null 2>/dev/null &'

```

This just creates a job that can die, etc. as once it's launched Windows takes over. But, I get my prompt back with no silly log messages.
