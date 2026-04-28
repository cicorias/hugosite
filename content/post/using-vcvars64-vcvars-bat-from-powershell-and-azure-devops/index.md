---
title: "Using vcvars64 vcvars.bat from PowerShell and Azure Devops"
date: 2020-05-05T16:44:54+0000
lastmod: 2020-05-08T10:52:30+0000
slug: "using-vcvars64-vcvars-bat-from-powershell-and-azure-devops"
feature_image: "https://www.cicoria.com/content/images/2020/05/image.png"
aliases:
  - /using-vcvars64-vcvars-bat-from-powershell-and-azure-devops/
---

**UPDATE: 2020-05-8 -- non-hard-coded paths!!**

Added step for using `vswhere`..

Recently in order to build Curl, I needed to just simply use the Native x64 command prompt and just `nmake` - unfortunately, that's not so direct.

So, the following is a PowerShell inline script that runs this on the build box, and this works on Azure Cloud Hosted too.

Thanks to <https://stackoverflow.com/a/2124759/140618>

```
      $vswhere = "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe"

      $vcvarspath = &$vswhere -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath
      Write-Output "vc tools located at: $vcvarspath"

      cmd.exe /c "call `"$vcvarspath\VC\Auxiliary\Build\vcvars64.bat`" && set > %temp%\vcvars.txt"
    
      Get-Content "$env:temp\vcvars.txt" | Foreach-Object {
        if ($_ -match "^(.*?)=(.*)$") {
          Set-Content "env:\$($matches[1])" $matches[2]
        }
      }
    
      .\buildconf.bat
      Set-Location .\winbuild
    
      $prefixRelease="libcurl-vc16-x64-release-dll-ipv6-sspi-winssl"
      $prefixDebug="libcurl-vc16-x64-debug-dll-ipv6-sspi-winssl"
    
      #release build
      nmake /f Makefile.vc mode=dll MACHINE=x64 GEN_PDB=yes WITH_PREFIX=$(Build.ArtifactStagingDirectory)\$prefixRelease
    
      #debug build
      nmake /f Makefile.vc mode=dll MACHINE=x64 DEBUG=yes GEN_PDB=yes WITH_PREFIX=$(Build.ArtifactStagingDirectory)\$prefixDebug

```

Hardcoded yes - but this is what works now.

\*\*Here's the full Pipeline yaml.

```
name: buildcurlmaster
resources:
  repositories:
  - repository: curl
    type: github
    name: curl/curl
    ref: refs/heads/master
    endpoint: github-curl

pool:
  name: windows-vm-scicoria
  demands:
  - Agent.OS -equals Windows_NT
  - Agent.OSArchitecture -equals X64
  - MSBuild_x64
  - VisualStudio
  - VisualStudio_16.0
  - azureps

#trigger: none # when done to suppress auto-triggers on branc
jobs:
- job: curlmaster
  displayName: 'building curl curl/curl'
  workspace:
    clean: all
  steps:
  - checkout: curl
  - powershell: |
      $vswhere = "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe"

      $vcvarspath = &$vswhere -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath
      Write-Output "vc tools located at: $vcvarspath"

      cmd.exe /c "call `"$vcvarspath\VC\Auxiliary\Build\vcvars64.bat`" && set > %temp%\vcvars.txt"
    
      Get-Content "$env:temp\vcvars.txt" | Foreach-Object {
        if ($_ -match "^(.*?)=(.*)$") {
          Set-Content "env:\$($matches[1])" $matches[2]
        }
      }
    
      .\buildconf.bat
      Set-Location .\winbuild
    
      $prefixRelease="libcurl-vc16-x64-release-dll-ipv6-sspi-winssl"
      $prefixDebug="libcurl-vc16-x64-debug-dll-ipv6-sspi-winssl"
    
      #release build
      nmake /f Makefile.vc mode=dll MACHINE=x64 GEN_PDB=yes WITH_PREFIX=$(Build.ArtifactStagingDirectory)\$prefixRelease
    
      #debug build
      nmake /f Makefile.vc mode=dll MACHINE=x64 DEBUG=yes GEN_PDB=yes WITH_PREFIX=$(Build.ArtifactStagingDirectory)\$prefixDebug
    displayName: 'conf-winbuild'

  - task: PublishBuildArtifacts@1
    displayName: 'Publish Artifact: drop'

  - task: ArchiveFiles@2
    displayName: 'Archive $(Build.ArtifactStagingDirectory)'
    inputs:
      rootFolderOrFile: '$(Build.ArtifactStagingDirectory)'
      includeRootFolder: false
      archiveFile: '$(Build.ArtifactStagingDirectory)/$(Build.DefinitionName).zip'

  - task: AzureFileCopy@3
    displayName: 'push-to-azure-storage'
    inputs:
      SourcePath: '$(Build.ArtifactStagingDirectory)/$(Build.DefinitionName).zip'
      azureSubscription: '$(mystoragesubscription)'
      Destination: AzureBlob
      #need variables for following - fallback settings too.
      storage: $(storageaccount)
      ContainerName: $(curldrops)
      BlobPrefix: 'slb-curl/$(Build.BuildNumber)'

```
