---
title: "Fixing mise shims not working in VS Code on Ubuntu: avoid the Snap build"
date: 2025-12-22T15:57:48+0000
lastmod: 2025-12-22T15:57:48+0000
slug: "fixing-mise-shims-not-working-in-vs-code-on-ubuntu-avoid-the-snap-build"
summary: "Fixing mise shims not working in VS Code on Ubuntu: avoid the Snap build "
tags: ["vscode", "ubuntu", "linux", "snap", "deb", "mise"]
feature_image: "https://www.cicoria.com/content/images/2025/12/Screenshot-2025-12-22-105547.png"
aliases:
  - /fixing-mise-shims-not-working-in-vs-code-on-ubuntu-avoid-the-snap-build/
---

## TL;DR

If `mise` shims work in your normal terminal but *not* in the VS Code integrated terminal on Ubuntu (especially with `zsh`), the fastest fix may be:

- **Do not use the Ubuntu Snap for VS Code**
- Install the official `.deb` package from `code.visualstudio.com` for your architecture instead

After switching from Snap to `.deb`, the integrated terminal typically behaves like a standard shell session and `mise` shims resolve correctly.

---

## The symptom

You have `mise` set up and working fine in a regular terminal:

- `node`, `python`, etc. resolve via `~/.local/share/mise/shims`
- `mise doctor` looks good
- Your `~/.zprofile` / `~/.zshrc` configuration is correct

But inside **VS Code → Terminal**, one or more of the following happens:

- `command not found` for tools that should be shimmed
- `which node` points to a system binary (or nothing) instead of a shim
- `$PATH` in VS Code is missing `~/.local/share/mise/shims`
- Shell initialization seems inconsistent compared to your external terminal

---

## Why this happens (in practice)

On Ubuntu, the **Snap build** of VS Code runs inside Snap confinement. That confinement can affect:

- Environment variable propagation (including `PATH`)
- Shell startup behavior in the integrated terminal
- Access to or resolution of user-level paths and toolchains

The net effect: even with correct `mise` setup, the VS Code integrated terminal may not see the same environment as your regular terminal session, so shims fail to resolve.

---

## The fix: install VS Code via `.deb` instead of Snap

### 1) Remove the Snap build

```bash
sudo snap remove code
```

### 1) Remove the Snap build

```bash
sudo snap remove code

```

### 2) Install the official `.deb` package

Download the `.deb` for your architecture from the official Visual Studio Code site:

- Go to `https://code.visualstudio.com/`
- Download the **Debian/Ubuntu (.deb)** package that matches your CPU (x64, ARM64, etc.)

Then install it:

```bash
sudo apt install ./code_*.deb

```

(Use the exact filename you downloaded.)

### 3) Reopen VS Code and re-check the terminal

Open a **new** integrated terminal and verify that shims are on `PATH`:

```bash
echo "$PATH" | tr ':' '\n' | head -n 20
command -v mise
command -v node python ruby go 2>/dev/null || true

```

You should see `~/.local/share/mise/shims` early in the output, and tool lookups should resolve through mise again.

---

## Notes and tips

- If you use `zsh`, ensure mise activation is configured appropriately (commonly in `~/.zprofile` and/or `~/.zshrc`).
- If you rely heavily on VS Code’s integrated terminal for toolchains, using the `.deb` build generally reduces surprises on Ubuntu compared to Snap confinement.
- If you manage VS Code updates via apt repositories, consider adding Microsoft’s repo (optional) for smoother updates.

---

## Conclusion

This was a classic “everything is configured correctly, but the environment differs” situation. In my case, the root cause wasn’t mise or zsh at all—it was the **Snap packaging of VS Code**. Switching to the official **`.deb`** build immediately restored normal PATH/shim behavior and made `mise` work in the integrated terminal as expected.
