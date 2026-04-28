---
title: "Jupyter Lab Build Failures under Wsl shutil.Error [Errno 13] Permission denied"
date: 2020-05-10T11:12:25+0000
lastmod: 2020-05-10T11:12:33+0000
slug: "post-post"
feature_image: "https://www.cicoria.com/content/images/2020/05/image-2.png"
aliases:
  - /post-post/
---

If you're seeing the following running under wsl in Windows it's not a Linux permission, it's a Windows permission issue. Easiest route it to elevate in Windows, move to wsl environment, the run your rebuild.

### I hate these errors

```
11:02 $ jupyter lab build --dev-build=False --minimize=False
[LabBuildApp] JupyterLab 1.2.11
[LabBuildApp] Building in /c/g/njit/njit-ml-project-spring-2020/.venv/share/jupyter/lab
[LabBuildApp] Building jupyterlab assets (build:prod)
An error occured.
shutil.Error: [('/c/g/njit/njit-ml-project-spring-2020/.venv/lib/python3.7/site-packages/jupyterlab/staging/templates', '/c/g/njit/njit-ml-project-spring-2020/.venv/share/jupyter/lab/staging/templates', "[Errno 13] Permission denied: '/c/g/njit/njit-ml-project-spring-2020/.venv/share/jupyter/lab/staging/templates'")]
See the log file for details:  /tmp/jupyterlab-debug-v2j1pzet.log

```

1. open up a PowerShell as "admin"
2. Navigate to the location of your `.venv`
3. start wsl
4. run the build command  
   jupyter lab build --dev-build=False --minimize=False

### things look much nicer now..

```
(.venv) ✔ /c/g/njit/njit-ml-project-spring-2020 [master|✚ 1…2⚑ 2]
11:08 $ jupyter lab build
[LabBuildApp] JupyterLab 1.2.11
[LabBuildApp] Building in /c/g/njit/njit-ml-project-spring-2020/.venv/share/jupyter/lab
[LabBuildApp] Building jupyterlab assets (build:prod:minimize)
(.venv) ✔ /c/g/njit/njit-ml-project-spring-2020 [master|✚ 1…2⚑ 2]

```
