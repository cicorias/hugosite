---
title: "Azure DevOps PowerShell Tasks Fail with NativeCommandError RemoteException"
date: 2020-05-08T12:48:13+0000
lastmod: 2020-05-08T12:48:13+0000
slug: "azure"
feature_image: "https://www.cicoria.com/content/images/2020/05/image-1.png"
aliases:
  - /azure/
---

If you run into the error mentioned with the Hosted Build Agents on Windows - I've seen this with the Windows-2019 images -- and you're truly not using PowerShell remoting - a simple switch to the PowerShell core version of the task works - `pwsh`

```
CategoryInfo          : NotSpecified: (:String) [], RemoteException
FullyQualifiedErrorId : NativeCommandError

```

### So, the following

```
  steps:
  - checkout: curl
  - powershell: |

```

### Becomes:

```
  steps:
  - checkout: curl
  - pwsh: |

```
