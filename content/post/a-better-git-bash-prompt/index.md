---
title: "A better git bash prompt"
date: 2019-04-11T09:48:46+0000
lastmod: 2019-04-11T09:48:46+0000
slug: "a-better-git-bash-prompt"
feature_image: "https://www.cicoria.com/content/images/2019/04/chris-ried-512801-unsplash2.jpg"
aliases:
  - /a-better-git-bash-prompt/
---

```
git clone https://github.com/magicmonty/bash-git-prompt.git ~/.bash-git-prompt --depth=1

cat >> ~/.bashrc <<EOF
if [ -f "$HOME/.bash-git-prompt/gitprompt.sh" ]; then
    GIT_PROMPT_ONLY_IN_REPO=1
    source $HOME/.bash-git-prompt/gitprompt.sh
fi
EOF

```
