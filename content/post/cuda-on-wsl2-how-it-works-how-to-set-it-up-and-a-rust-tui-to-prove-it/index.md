---
title: "CUDA on WSL2: How It Works, How to Set It Up, and a Rust TUI to Prove It"
date: 2026-04-06T14:55:41+0000
lastmod: 2026-04-06T15:34:59+0000
slug: "cuda-on-wsl2-how-it-works-how-to-set-it-up-and-a-rust-tui-to-prove-it"
summary: "Nvidia cuda on wsl quick setup and benchmarks"
tags: ["code", "containers", "gpu", "linux", "pytorch", "ubuntu", "vm", "windows", "wsl"]
feature_image: "/images/2026/04/image-2.jpg"
aliases:
  - /cuda-on-wsl2-how-it-works-how-to-set-it-up-and-a-rust-tui-to-prove-it/
---

## Overview

Running CUDA workloads on Windows used to mean either dual-booting into Linux or fighting with Windows-native toolchains. WSL2 changed that. You get a real Linux kernel, real GPU access, and near-native performance — all from a Windows terminal.

I built a set of setup scripts and a Rust TUI tool called `cuda-checker` to automate the setup and verify everything actually works end to end. This post covers how WSL2 GPU passthrough works under the hood, the setup process, and the tool itself.

## How WSL2 GPU access works

WSL2 runs a real Linux kernel inside a lightweight Hyper-V VM. GPU access is not emulated — it's direct hardware passthrough via a mechanism Microsoft and NVIDIA built together called [GPU-PV (GPU Paravirtualization)](https://learn.microsoft.com/en-us/windows-hardware/drivers/display/gpu-paravirtualization).

The key pieces:

1. **The Windows NVIDIA driver** exposes a paravirtualized GPU device to the WSL2 VM. The VM sees `/dev/dxg`, a DirectX Graphics kernel device that proxies GPU commands from Linux userspace back to the Windows kernel-mode driver.
2. **`/usr/lib/wsl/lib/`** is automatically mounted into every WSL2 distro. It contains `libcuda.so.1`, `libnvidia-ml.so.1`, `nvidia-smi`, and other driver stubs. These are not Linux GPU drivers — they're thin shims that forward calls through `/dev/dxg` to the real Windows driver.
3. **`/dev/dxg`** is the bridge. When CUDA code calls into `libcuda.so.1`, the call goes through this device node to the Windows GPU driver, which dispatches it to the actual hardware. There's no GPU device emulation and no translation layer for compute operations.
4. **`nvidia-smi`** in WSL2 is the same binary from `/usr/lib/wsl/lib/`. It talks to the Windows driver through the same path. That's why it reports the Windows driver version.

This architecture means you **must not install a Linux NVIDIA GPU driver** inside WSL2. Doing so overwrites the Windows driver stubs and breaks the passthrough chain. You only install the CUDA *toolkit* (compiler, libraries, headers) — the driver comes from Windows.

For Docker containers, the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) maps `/dev/dxg` and the WSL lib directory into the container, giving containerized workloads the same GPU access.

## Reference documentation

The official docs are spread across several sites. These are the ones that matter:

- [NVIDIA CUDA on WSL User Guide](https://docs.nvidia.com/cuda/wsl-user-guide/index.html) — The primary reference. Covers architecture, installation, known limitations, and the critical "do not install Linux drivers" rule.
- [CUDA Installation Guide for Linux](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/) — Toolkit installation for all Linux platforms including WSL-Ubuntu.
- [NVIDIA Container Toolkit Install Guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) — Required for `docker run --gpus all`.
- [Microsoft WSL GPU Support](https://devblogs.microsoft.com/directx/directx-heart-linux/#:~:text=GPU%20Virtualization,-Over%20the%20last&text=This%20technology%20is%20integrated%20into,use%20in%20a%20Linux%20environment) — Microsoft's side of the story: GPU-PV architecture, DirectML, and compute support.
- [CUDA Quick Start Guide](https://docs.nvidia.com/cuda/cuda-quick-start-guide/) — Minimal steps if you just want to get nvcc working.
- [NVIDIA Developer Forums: WSL2](https://forums.developer.nvidia.com/tags/c/accelerated-computing/cuda/206/wsl/146) — Where edge cases and driver-specific issues get discussed.

## Setting up CUDA on WSL2

The repo includes six scripts that handle the full setup. They enforce the WSL2-specific rules from the NVIDIA docs:

| Rule | Why |
| --- | --- |
| Do **not** install a Linux NVIDIA GPU driver | Overwrites the Windows driver stub in `/usr/lib/wsl/lib/` |
| Use the `wsl-ubuntu` apt repository | The standard `ubuntu2404` repo pulls in Linux driver packages |
| Install `cuda-toolkit-12-x`, not `cuda` or `cuda-12-x` | The meta-packages include `cuda-drivers` which installs a Linux driver |
| Install the Windows NVIDIA driver first | It's the only driver. The Linux side just uses stubs. |

The scripts run in order:

```
# Windows (PowerShell, admin):
scripts/00-preflight-windows.ps1     # Check driver, WSL2 kernel, build version

# WSL2 Ubuntu:
bash scripts/01-preflight-wsl.sh     # Verify WSL2 environment
bash scripts/02-install-cuda.sh      # Install cuda-toolkit from wsl-ubuntu repo
bash scripts/03-configure-env.sh     # Set PATH, LD_LIBRARY_PATH, CUDA_HOME
bash scripts/04-install-container-toolkit.sh  # NVIDIA Container Toolkit for Docker
bash scripts/05-verify-all.sh        # End-to-end: nvidia-smi, nvcc, CUDA kernel, Docker

```

The verify script compiles and runs an actual CUDA kernel (not just checking that binaries exist) and tests Docker GPU access.

## cuda-checker: a Rust TUI for verification

After setup, I wanted something more persistent than a one-shot verify script — a tool that shows live GPU metrics, runs real CUDA benchmarks, and can dump JSON for automation. So I wrote `cuda-checker` in Rust.

It does four things:

- Detects NVIDIA GPUs via NVML and reports driver version, CUDA version, compute capability, and VRAM
- Polls live metrics: temperature, power draw, utilization, clock speeds
- Compiles and runs real CUDA kernels (vector add, matrix multiply, memory bandwidth) and reports throughput
- Outputs as an interactive TUI, plain text, or JSON

## The stack

| Crate | Purpose |
| --- | --- |
| [nvml-wrapper](https://crates.io/crates/nvml-wrapper) 0.12 | GPU detection and live metrics via NVIDIA Management Library |
| [cudarc](https://crates.io/crates/cudarc) 0.19 | CUDA kernel compilation (NVRTC) and execution |
| [ratatui](https://crates.io/crates/ratatui) 0.30 | Terminal UI framework |
| [clap](https://crates.io/crates/clap) 4 | CLI argument parsing |

The TUI has three tabs: an overview with live GPU gauges, a benchmark results table, and a scrolling log viewer.

## WSL2-specific gotchas

Two things tripped me up during development.

**NVML library loading.** WSL2 exposes the NVIDIA management library at `/usr/lib/wsl/lib/libnvidia-ml.so.1`, but does *not* create a bare `libnvidia-ml.so` symlink. Older versions of `nvml-wrapper` (pre-0.12) looked for the bare `.so` and failed silently. Version 0.12 defaults to `.so.1`, which resolves this.

**CUDA toolkit repo selection.** You must use the `wsl-ubuntu` apt repository (`developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/`), not the standard Ubuntu one. And you must install `cuda-toolkit-12-x` specifically — the `cuda` or `cuda-12-x` meta-packages pull in a Linux GPU driver that overwrites the Windows driver stub and breaks the `/dev/dxg` passthrough.

## Usage

```bash
# Install mise (manages Rust version + project tasks)
curl https://mise.jdx.dev/install.sh | sh
mise trust && mise install

# Build
mise run build

# Headless with benchmarks
./target/release/cuda-checker --no-tui --benchmark

# JSON output for scripting
./target/release/cuda-checker --json --benchmark

# Interactive TUI
./target/release/cuda-checker

```

Sample headless output:

```
GPU 0: NVIDIA GeForce RTX 3070 Ti Laptop GPU
  Driver: 581.95  CUDA: 13.0  CC: 8.6
  VRAM: 389.60 MiB / 8.00 GiB
  Temp: 49°C  Power: 14.1W/128.1W  GPU Util: 0%  Mem Util: 0%

=== Benchmark Results ===

Vector Add (16M elements): 576.14 µs
  throughput: 333.25 GB/s

Matrix Multiply (1024×1024): 2.18 ms
  compute: 983.40 GFLOPS

Memory Bandwidth (64M floats): 1.55 ms
  throughput: 329.61 GB/s

```

## Docker

A multi-stage Dockerfile builds against `nvidia/cuda:12.8.1-cudnn-devel-ubuntu24.04` and produces a slim runtime image. With the NVIDIA Container Toolkit installed, it runs the same benchmarks inside a container:

```bash
docker build -t cuda-checker:latest .
docker run --rm --gpus all cuda-checker:latest

```

The compose file defines three services (`cuda-checker`, `benchmark`, `json`) for convenience.

## Testing

49 tests total. Unit tests run without a GPU — they test CLI parsing, error formatting, serialization, app state logic. Integration tests are gated behind a `gpu-tests` Cargo feature and exercise actual NVML calls and CUDA kernel execution.

```bash
cargo test                          # unit + CLI tests (no GPU needed)
cargo test --features gpu-tests     # everything (needs GPU)

```

## Source

The repo is at [github.com/cicorias/cuda-wsl2-setup](https://github.com/cicorias/cuda-wsl2-setup). It also includes the shell scripts for setting up CUDA on WSL2 Ubuntu 24.04 from scratch.
