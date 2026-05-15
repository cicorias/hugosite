---
title: "Running VS Code Agents in WSL Using WSLg"
date: 2026-05-15T08:55:00-04:00
slug: "running-vscode-agents-in-wsl-with-wslg"
feature_image: "/images/2026/05/WSLg_ArchitectureOverview.png"
tags: ["vscode", "wsl", "linux", "windows"]
summary: "A workaround to run the new GitHub VS Code Agents app natively inside WSL2 by leveraging WSLg and a simple shell function."
aliases:
  - /running-vscode-agents-in-wsl-with-wslg/
---

## The Problem

The new [Visual Studio Code Agents](https://code.visualstudio.com/) app (the standalone GitHub "Agents" product) does not yet support WSL remote connections. If you work primarily in WSL2 with your repos on the Linux filesystem, you are stuck: the Agents app runs on Windows and cannot open WSL directories properly. UNC paths via `\\wsl.localhost` cause file-attribute confusion, CR/LF issues, and the integrated terminal does not spawn a proper WSL shell.

This is tracked in [microsoft/vscode#307568](https://github.com/microsoft/vscode/issues/307568).

## The Workaround: Run VS Code Agents Natively in WSL via WSLg

Since WSL2 with WSLg supports running Linux GUI applications that render on the Windows desktop, you can run the **Linux build** of VS Code Agents directly inside your WSL distro. This sidesteps the remote-connection problem entirely because the editor is running natively on Linux, right where your files are.

### Step 1: Download the Linux Build

Download the Linux x64 `.tar.gz` archive of VS Code (or VS Code Insiders / Agents build) and extract it to a location that is **not** on your `$PATH`:

```bash
mkdir -p "$HOME/bin"
# Download and extract (adjust URL for the Agents/Insiders build)
tar -xzf code-stable-x64.tar.gz -C "$HOME/bin/"
```

This gives you `$HOME/bin/VSCode-linux-x64/code`. Do **not** add `$HOME/bin/VSCode-linux-x64` to your `$PATH`. Keeping it off the path avoids conflicts with the Windows `code` command that the regular VS Code installation exposes at `/mnt/c/Users/<USERNAME>/AppData/Local/Programs/Microsoft VS Code/bin/code`.

### Step 2: Create a Shell Function

Add the following function to your `~/.bashrc` or `~/.zshrc`:

```bash
lcode() {
  local logfile="/tmp/lscode-$(date +%Y%m%d-%H%M%S)-$$.log"
  DBUS_SESSION_BUS_ADDRESS="disabled:" /home/cicorias/bin/VSCode-linux-x64/code --disable-gpu "$@" >"$logfile" 2>&1 &
  disown
}
```

A few things to note:

- **`lcode`** is used instead of `code` to avoid shadowing the Windows VS Code command.
- **`DBUS_SESSION_BUS_ADDRESS="disabled:"`** tells the D-Bus client library to skip connecting to a session bus entirely. WSLg does not run a full desktop session, so there is no session bus available. Without this, VS Code attempts to connect, times out or throws errors, and features like the file-change watcher and clipboard integration may misbehave. The special `disabled:` address is recognized by `libdbus` as "do not attempt any connection."
- **`--disable-gpu`** disables Chromium's GPU-accelerated rendering. Under WSLg the virtual GPU (`/dev/dxg`) may not expose the extensions that Chromium expects, which leads to black windows, rendering glitches, or crashes on launch. Software rendering is slower but completely reliable inside WSLg.
- **Redirecting to `/tmp`** captures both stdout and stderr in a timestamped, PID-tagged log file (`/tmp/lscode-YYYYMMDD-HHMMSS-PID.log`). This is more useful than discarding output with `/dev/null` because VS Code can emit startup warnings or crash traces that are hard to reproduce. If something goes wrong you can inspect the log; the files are cleaned up automatically on reboot since `/tmp` is a tmpfs inside WSL.
- **`disown`** detaches the process from the shell so closing the terminal does not kill the editor.

### Step 3: Use It

```bash
# Open the current directory
lcode .

# Open a specific project
lcode ~/projects/my-repo
```

The VS Code Agents window renders on your Windows desktop via WSLg, but the editor process and all file I/O happen natively on the Linux filesystem. Extensions, the integrated terminal, and Git all work as expected because everything is running inside WSL.

## Why This Works

WSLg provides a Wayland/X11 compositor that bridges Linux GUI apps to the Windows desktop. By running the Linux build of VS Code Agents inside WSL, the editor sees a normal Linux environment. There is no remote connection, no UNC path translation, and no cross-OS filesystem boundary. Your files, your shell, and your tools are all in one place.

## References

- [microsoft/vscode#307568 - Agent host: Support WSL connections](https://github.com/microsoft/vscode/issues/307568)
- [WSLg on GitHub](https://github.com/microsoft/wslg)
- [My comment on the issue](https://github.com/microsoft/vscode/issues/307568#issuecomment-4459787995)
