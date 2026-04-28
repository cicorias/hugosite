---
title: "Cleaning up Visual Studio Code Extensions"
date: 2025-06-13T16:08:01+0000
lastmod: 2025-06-13T16:13:52+0000
slug: "cleaning-up-visual-studio-code-extensions"
summary: "Cleaning up Visual Studio Code Extensions with a simple script. From my experience it helps to keep the Default profile empty as possible. And set the setting \"for new windows use default\" – or whatever that setting is."
tags: ["bash", "code", "shell", "utilities"]
feature_image: "https://images.unsplash.com/photo-1516116216624-53e697fedbea?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMTc3M3wwfDF8c2VhcmNofDJ8fHZpc3VhbCUyMHN0dWRpb3xlbnwwfHx8fDE3NDk4MzA4MjB8MA&ixlib=rb-4.1.0&q=80&w=2000"
aliases:
  - /cleaning-up-visual-studio-code-extensions/
---

Overtime I often need to cleanup the various extensions installed in the Default profile. For some reason in VS Code it's not possible to "recreate" the Default or reset it. In fact, I haven't seen it synchronize for some time.

So, I created the following scripts in both PowerShell and Bash. It takes a parameter to the profile name, or falls back to Default.

From my experience it helps to keep the Default profile empty as possible. And set the setting "for new windows use default" – or whatever that setting is.

Source is here as well:

![](https://www.cicoria.com/content/images/icon/pinned-octocat-093da3e6fa40-1.svg)

## PowerShell - RemoveExtensions.ps1

```pwsh
#!/usr/bin/env pwsh

param (
    [string]$Profile = "Default"
)

# List all extensions for the specified profile
$extensions = code --profile $Profile --list-extensions

if (-not $extensions) {
    Write-Host "No extensions found for profile '$Profile'."
    exit
}

# Confirm before proceeding
Write-Host "The following extensions will be uninstalled from the '$Profile' profile:"
$extensions | ForEach-Object { Write-Host $_ }

$confirmation = Read-Host "Are you sure you want to uninstall all these extensions? (y/n)"
if ($confirmation -ne 'y') {
    Write-Host "Operation cancelled."
    exit
}

# Uninstall each extension
foreach ($ext in $extensions) {
    Write-Host "Uninstalling $ext..."
    code --profile $Profile --uninstall-extension $ext
}

Write-Host "All extensions have been uninstalled from the '$Profile' profile."
```

## Bash - removeExtensions.sh

```shell
#!/bin/bash

# Get the profile name from the first argument, default to "Default"
PROFILE="${1:-Default}"

# Get the list of extensions
extensions=$(code --profile "$PROFILE" --list-extensions)

if [ -z "$extensions" ]; then
  echo "No extensions found for profile '$PROFILE'."
  exit 0
fi

echo "The following extensions will be uninstalled from the '$PROFILE' profile:"
echo "$extensions"

read -p "Are you sure you want to uninstall all these extensions? (y/n): " confirm
if [[ "$confirm" != "y" ]]; then
  echo "Operation cancelled."
  exit 0
fi

# Uninstall each extension
while IFS= read -r ext; do
  echo "Uninstalling $ext..."
  code --profile "$PROFILE" --uninstall-extension "$ext"
done <<< "$extensions"

echo "All extensions have been uninstalled from the '$PROFILE' profile."
```
