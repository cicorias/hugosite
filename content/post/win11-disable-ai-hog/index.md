---
title: "Windows 11 AI Features -- 8 Gig of RAM -- what I don't need"
date: 2026-02-04T14:03:29+0000
lastmod: 2026-02-04T14:08:15+0000
slug: "win11-disable-ai-hog"
tags: ["amd", "utilities", "windows"]
feature_image: "https://images.unsplash.com/photo-1557831488-38f006e78c1b?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMTc3M3wwfDF8c2VhcmNofDF8fHdpbmRvd3MlMjAxMSUyMGZpcmV8ZW58MHx8fHwxNzcwMjEzOTU3fDA&ixlib=rb-4.1.0&q=80&w=2000"
aliases:
  - /win11-disable-ai-hog/
---

## AI features using over 8 Gig of RAM

- **What’s happening:** `WorkloadsSessionHost.exe` can spawn multiple background “workload” processes that support newer **AI/semantic features**, and it often **respawns** after you end it in Task Manager.
  - Source: [Microsoft Q&A thread on high CPU/RAM usage](https://learn.microsoft.com/en-us/answers/questions/3857480/workloadssessionhost-high-cpu-ram-usage) ([Microsoft Learn](https://learn.microsoft.com/en-us/answers/questions/3857480/workloadssessionhost-high-cpu-ram-usage))
- **First, disable the triggers (lowest risk):** Turn off Windows features that commonly drive these workload sessions—especially **Recall / snapshots** and “semantic”/enhanced search behaviors.
  - Context + discussion: [SuperUser: WindowsWorkload.Manager / controlling it](https://superuser.com/questions/1890361/what-is-the-windowsworkload-manager-and-how-do-you-control-or-use-it) ([Super User](https://superuser.com/questions/1890361/what-is-the-windowsworkload-manager-and-how-do-you-control-or-use-it?utm_source=chatgpt.com))
  - Community observation tying sessions to Recall-related components: [ElevenForum thread](https://www.elevenforum.com/t/new-workloadssessionhost-processes-consuming-ram.36446/) ([Windows 11 Forum](https://www.elevenforum.com/t/new-workloadssessionhost-processes-consuming-ram.36446/?utm_source=chatgpt.com))
- **If you want it *off*, disable the service most commonly associated with it:** Many reports tie the RAM-heavy WorkloadsSessionHost instances to **Windows AI Fabric Service** (often shown as `WSAIFabricSvc`). Disabling the service is the “hard off switch” people use.
  - How-to steps (services.msc + `WSAIFabricSvc`): [Acer Community walkthrough](https://community.acer.com/en/discussion/732950/why-workloadsessionhost-exe-consuming-my-ram) ([Acer Community](https://community.acer.com/en/discussion/732950/why-workloadsessionhost-exe-consuming-my-ram?utm_source=chatgpt.com))
  - Related Microsoft Q&A thread (same fix cited by users): [Microsoft Q&A discussion](https://learn.microsoft.com/en-us/answers/questions/3857480/workloadssessionhost-high-cpu-ram-usage) ([Microsoft Learn](https://learn.microsoft.com/en-us/answers/questions/3857480/workloadssessionhost-high-cpu-ram-usage?utm_source=chatgpt.com))
- **Optional: check Task Scheduler entries:** Some guides suggest disabling any scheduled task that explicitly launches WorkloadsSessionHost to prevent automatic restarts.
  - Steps: [AllThings.How guide](https://allthings.how/disable-workloadssessionhost-in-windows-environments/) ([All Things How](https://allthings.how/disable-workloadssessionhost-in-windows-environments/))
- **Security sanity check:** Right-click the process in Task Manager → **Open file location**. A legit binary is commonly under a Windows app package (WindowsWorkload manager); anything in odd paths (Temp/User folders) is suspicious.
  - Background: [SuperUser: WindowsWorkload.Manager](https://superuser.com/questions/1890361/what-is-the-windowsworkload-manager-and-how-do-you-control-or-use-it) ([Super User](https://superuser.com/questions/1890361/what-is-the-windowsworkload-manager-and-how-do-you-control-or-use-it?utm_source=chatgpt.com))

*Note:* Most public writeups reference Windows 11 (24H2-era builds) but the same components are being reported on newer builds; the workflow above is still the practical “turn it off” playbook.

```shell
<#
Disable-WorkloadsSessionHostAI.ps1
Purpose: Reduce/stop WorkloadsSessionHost-related RAM usage by disabling the most common triggers:
- Windows AI Fabric service (commonly tied to WorkloadsSessionHost)
- Scheduled tasks that relaunch AI/workload components
- Optional Windows features that include “Recall/Copilot/AI/Semantic” (only if present on your system)

Run in an elevated PowerShell (Admin).
Use -WhatIf first to preview changes.
#>

[CmdletBinding(SupportsShouldProcess=$true)]
param(
  [switch]$WhatIf,
  [switch]$NoRestart
)

function Assert-Admin {
  $isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()
  ).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

  if (-not $isAdmin) {
    throw "This script must be run as Administrator. Right-click PowerShell -> Run as administrator."
  }
}

function Stop-WorkloadsProcesses {
  Write-Host "`n== Stopping WorkloadsSessionHost processes (they may respawn) ==" -ForegroundColor Cyan
  Get-Process -Name "WorkloadsSessionHost" -ErrorAction SilentlyContinue | ForEach-Object {
    if ($PSCmdlet.ShouldProcess($_.Name, "Stop-Process (PID $($_.Id))")) {
      Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
    }
  }
}

function Disable-AIFabricServices {
  Write-Host "`n== Disabling Windows AI Fabric-related services (if present) ==" -ForegroundColor Cyan

  # Common patterns reported in the wild:
  # - Service Name often includes: AIFabric, WSAIFabricSvc
  # - DisplayName often includes: "Windows AI Fabric"
  $svcMatches = Get-Service -ErrorAction SilentlyContinue | Where-Object {
    $_.Name -match 'AIFabric|WSAIFabric' -or $_.DisplayName -match 'AI Fabric'
  }

  if (-not $svcMatches) {
    Write-Host "No AI Fabric-matching services found on this system." -ForegroundColor Yellow
    return
  }

  foreach ($svc in $svcMatches) {
    Write-Host "Found service: $($svc.Name)  ($($svc.DisplayName))  Status=$($svc.Status)  StartType=$($svc.StartType)"

    if ($PSCmdlet.ShouldProcess($svc.Name, "Stop-Service")) {
      Stop-Service -Name $svc.Name -Force -ErrorAction SilentlyContinue
    }
    if ($PSCmdlet.ShouldProcess($svc.Name, "Set-Service StartupType Disabled")) {
      Set-Service -Name $svc.Name -StartupType Disabled -ErrorAction SilentlyContinue
    }
  }
}

function Disable-RelatedScheduledTasks {
  Write-Host "`n== Disabling scheduled tasks that commonly relaunch AI/workload components (best-effort) ==" -ForegroundColor Cyan

  # These are *heuristics*. We only disable tasks whose TaskName or TaskPath contains these keywords.
  $keywords = @(
    "WorkloadsSessionHost",
    "Workload",
    "WindowsWorkload",
    "AIFabric",
    "WindowsAI",
    "Recall",
    "Copilot",
    "Semantic",
    "StudioEffects",
    "WindowsStudio"
  )

  $tasks = Get-ScheduledTask -ErrorAction SilentlyContinue | Where-Object {
    $namePath = ($_.TaskName + " " + $_.TaskPath)
    $keywords | ForEach-Object { $namePath -match [regex]::Escape($_) } | Where-Object { $_ } | Select-Object -First 1
  }

  if (-not $tasks) {
    Write-Host "No matching scheduled tasks found (or access is restricted)." -ForegroundColor Yellow
    return
  }

  foreach ($t in $tasks) {
    Write-Host "Disabling task: $($t.TaskPath)$($t.TaskName)"
    if ($PSCmdlet.ShouldProcess("$($t.TaskPath)$($t.TaskName)", "Disable-ScheduledTask")) {
      Disable-ScheduledTask -TaskName $t.TaskName -TaskPath $t.TaskPath -ErrorAction SilentlyContinue | Out-Null
    }
  }
}

function Disable-OptionalFeaturesIfPresent {
  Write-Host "`n== Disabling optional Windows features that match Recall/Copilot/AI/Semantic (only if they exist) ==" -ForegroundColor Cyan

  # We only disable features that actually exist on *your* Windows image.
  # This avoids hardcoding feature names that vary by build/edition.
  $featurePatterns = 'Recall|Copilot|WindowsAI|AIFabric|Semantic|StudioEffects|WindowsStudio'

  $features = Get-WindowsOptionalFeature -Online -ErrorAction SilentlyContinue |
    Where-Object { $_.FeatureName -match $featurePatterns -and $_.State -eq "Enabled" }

  if (-not $features) {
    Write-Host "No enabled optional features matched the patterns on this system." -ForegroundColor Yellow
    return
  }

  foreach ($f in $features) {
    Write-Host "Disabling optional feature: $($f.FeatureName)"
    if ($PSCmdlet.ShouldProcess($f.FeatureName, "Disable-WindowsOptionalFeature")) {
      Disable-WindowsOptionalFeature -Online -FeatureName $f.FeatureName -NoRestart -ErrorAction SilentlyContinue | Out-Null
    }
  }
}

# ---------------- MAIN ----------------
Assert-Admin

Write-Host "Starting disable script..." -ForegroundColor Green
Write-Host "Tip: Run with -WhatIf first to preview changes." -ForegroundColor DarkGray

Stop-WorkloadsProcesses
Disable-AIFabricServices
Disable-RelatedScheduledTasks
Disable-OptionalFeaturesIfPresent

Write-Host "`nDone." -ForegroundColor Green

if (-not $NoRestart) {
  Write-Host "A reboot is recommended to fully apply changes." -ForegroundColor Yellow
  Write-Host "Reboot now with:  Restart-Computer" -ForegroundColor DarkGray
} else {
  Write-Host "NoRestart specified; skipping reboot suggestion." -ForegroundColor DarkGray
}

```
