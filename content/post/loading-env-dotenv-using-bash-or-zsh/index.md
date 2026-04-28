---
title: "Loading .env (dotenv) using bash or zsh"
date: 2022-01-05T10:15:26+0000
lastmod: 2022-01-05T10:23:31+0000
slug: "loading-env-dotenv-using-bash-or-zsh"
summary: "Keep Cloud Native and follow 12 Factor Apps with dotenv even in Shell Bash Zsh scripts"
tags: ["bash", "shell", "utilities", "containers", "cloud"]
feature_image: "https://www.cicoria.com/content/images/2022/01/isqxrrjimnx7uce0vsxe.png"
aliases:
  - /loading-env-dotenv-using-bash-or-zsh/
---

The dotenv approach has been around quite some time with tremendous support in tooling, frameworks, etc. I'm not sure if this started in nodejs but it's available across many languages now. Tooling like Visual Studio Code support the .env files - see [Environment Variables](https://code.visualstudio.com/docs/python/environments#_environment-variable-definitions-file). The use of environment variables is also one of the factors in [The Twelve Factor App - Config.](https://12factor.net/config)

In one area I've seen different approaches, but similar to the following:

```bash
if [ ! -f .env ]
then
  export $(cat .env | xargs)
fi

```

However, something that I find far simpler is to use the `allexport` feature of [bash](https://www.gnu.org/software/bash/)/[zsh](https://www.zsh.org/)

```bash
set -o allexport; source .env; set +o allexport
```

Can also be shortened to: ([see All Export Built in](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html)):

```bash
set -a; source .env; set +a
```
