---
title: "Jupyter Notebook auto launch browser from WSL"
date: 2020-01-24T07:44:04+0000
lastmod: 2020-01-24T07:44:04+0000
slug: "jupyter-notebook-launch-browser-from-wsl"
feature_image: "https://www.cicoria.com/content/images/2020/01/image.png"
aliases:
  - /jupyter-notebook-launch-browser-from-wsl/
---

If you're running Windows 10 with WSL, built out a Python virtual environment, then running the command to launch the Notebook server - you're probably seeing this.

```
No web browser found: could not locate runnable browser

```

## Wsl Utilities

Thankfully, there's a tool that can help bridge opening the Browser onWindows from the WSL shell - you can install WslUtilities from [here](https://github.com/wslutilities/wslu)

You have to install it and ensure to register it in WSL as the browser:

```
wslview --register

```

Now, once you do this, you now have a different issue and that's related to how Jupyter decides to create the URL and pass it to the browser command.

Running the `jupyter notebook` command again.

> Note: I'm using [Poetry](https://python-poetry.org/) and [Pipenv](https://pipenv.kennethreitz.org/en/latest/) but you should get the gist.

```
07:07 $ poetry run jupyter notebook
[I 07:07:55.332 NotebookApp] Serving notebooks from local directory: /c/g/njit/njit-ml-scratch
[I 07:07:55.333 NotebookApp] The Jupyter Notebook is running at:
[I 07:07:55.333 NotebookApp] http://localhost:8888/?token=5fc7425e915e9f3083e2f658443a2b837465e5d054441fc8
[I 07:07:55.333 NotebookApp]  or http://127.0.0.1:8888/?token=5fc7425e915e9f3083e2f658443a2b837465e5d054441fc8
[I 07:07:55.333 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[C 07:07:55.545 NotebookApp]

    To access the notebook, open this file in a browser:
        file:///home/cicorias/.local/share/jupyter/runtime/nbserver-12677-open.html
    Or copy and paste one of these URLs:
        http://localhost:8888/?token=5fc7425e915e9f3083e2f658443a2b837465e5d054441fc8
     or http://127.0.0.1:8888/?token=5fc7425e915e9f3083e2f658443a2b837465e5d054441fc8
tcgetpgrp failed: Not a tty
Start : This command cannot be run due to the error: The system cannot find the file specified.
At line:1 char:1
+ Start "file:///home/cicorias/.local/share/jupyter/runtime/nbserver-12 ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidOperation: (:) [Start-Process], InvalidOperationException
    + FullyQualifiedErrorId : InvalidOperationException,Microsoft.PowerShell.Commands.StartProcessCommand

```

First thing is, that's actually PowerShell attempting to run from Windows a Browser. That's something `wslview` does for you.

What you need is to set the command that should be used. From [this StackOverflow article](https://stackoverflow.com/a/47773389/140618) here's a brief script to do the trick:

#### ~/bin/jupyter-notebook-browser

I've put this shell script in my `$PATH` - I have `$HOME/bin` always in my path, so I dropped it there.

```
#!/bin/bash
file=$(echo "$1" | sed 's/file:\/\///')
url=$(grep -oP 'href="\K([^"]*localhost[^"]+)' "$file")
wslview "$url"

```
> NOTE: Jupyter notebook relies on the webbrowser python module to discover and run the command. While a CLI switch `--browser=...` is documented (as well as for the config for Jupyter) I could not get this to work and just backed down to using the `BROWSER` environment variable.

### command to run and launch

Again, I'm using Poetry for my package virtual and package management (along with Pipenv).

```
 BROWSER=jupyter-notebook-browser poetry run jupyter notebook

```

After that you should see somethign like this:

```
07:32 $ BROWSER=jupyter-notebook-browser poetry run jupyter notebook
[I 07:33:41.022 NotebookApp] Serving notebooks from local directory: /c/g/njit/njit-ml-scratch
[I 07:33:41.023 NotebookApp] The Jupyter Notebook is running at:
[I 07:33:41.023 NotebookApp] http://localhost:8888/?token=f7ff98f62a5bf6f07bd0e9c255aff72163c857f11b3672a0
[I 07:33:41.023 NotebookApp]  or http://127.0.0.1:8888/?token=f7ff98f62a5bf6f07bd0e9c255aff72163c857f11b3672a0
[I 07:33:41.024 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[C 07:33:41.239 NotebookApp]

    To access the notebook, open this file in a browser:
        file:///home/cicorias/.local/share/jupyter/runtime/nbserver-15218-open.html
    Or copy and paste one of these URLs:
        http://localhost:8888/?token=f7ff98f62a5bf6f07bd0e9c255aff72163c857f11b3672a0
     or http://127.0.0.1:8888/?token=f7ff98f62a5bf6f07bd0e9c255aff72163c857f11b3672a0

```

If you don't see anything or a message about not finding a valid browser, that means the script isn't being found or failing for some reason.

For interest, if you'd like to try Poetry and run a good baseline virtual environment, the contents of my Poetry files and my `direnv .envrc` files are below. I'm also a big fan of [Direnv](https://direnv.net/) for local `ENV` settings, kinda along the lines of a `dotenv` but just another more opinionated approach.

#### pyproject.toml

```
[tool.poetry]
name = "njit-ml-scratch"
version = "0.1.0"
description = ""
authors = ["Shawn Cicoria <z@cicoria.com>"]

[tool.poetry.dependencies]
python = "^3.7"
jupyter = "^1.0.0"
notebook = "^6.0.2"
numpy = "^1.18.1"
scipy = "^1.4.1"
matplotlib = "^3.1.2"
pandas = "^0.25.3"
scikit-learn = "^0.22.1"
jupyter_contrib_nbextensions = "^0.5.1"

[tool.poetry.dev-dependencies]

[build-system]
requires = ["poetry>=0.12"]
build-backend = "poetry.masonry.api"

```

#### .envrc

```
export PIPENV_IGNORE_VIRTUALENVS="yes"
export PIPENV_VENV_IN_PROJECT="yes"
export POETRY_VIRTUALENVS_IN_PROJECT="true"
export POETRY_VIRTUALENVS_CREATE="true"

```
