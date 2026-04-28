---
title: "Getting PyTorch + ROCm Working on a Framework 13 (Ryzen AI 9) Using a Dev Container"
date: 2025-11-23T20:14:26+0000
lastmod: 2025-11-23T20:32:39+0000
slug: "getting-pytorch-rocm-working-on-a-framework-13-ryzen-ai-9-using-a-dev-container"
summary: "Getting PyTorch with ROCm running on a Framework 13 with Ryzen AI 9 was surprisingly fragile, so I moved everything into an AMD ROCm PyTorch devcontainer and used HSA_OVERRIDE_GFX_VERSION=11.0.0 to finally make the integrated Radeon GPU usable for local experiments."
tags: ["containers", "amd", "ryzen", "pytorch", "machine learning", "ai"]
feature_image: "https://images.unsplash.com/photo-1717444309226-c0809d4b5bde?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMTc3M3wwfDF8c2VhcmNofDR8fGFtZHxlbnwwfHx8fDE3NjM5MjgwNTF8MA&ixlib=rb-4.1.0&q=80&w=2000"
aliases:
  - /getting-pytorch-rocm-working-on-a-framework-13-ryzen-ai-9-using-a-dev-container/
---

I’ve been using a Framework Laptop 13 with the AMD Ryzen AI 9 HX 370 as my lab machine with local model experimentation, learning etc..

On paper, it’s a perfect little AI dev box:

- **Laptop:** Framework 13, AMD Ryzen AI 9 HX 370
- **GPU:** Integrated AMD Radeon 890M
- **OS:** Linux on bare metal
- **Goal:** Run PyTorch with ROCm on the iGPU for local training and experiments

What I wanted was straightforward: **get PyTorch + ROCm running on the integrated GPU without turning the host into a science project.**

That was… optimistic.

This post walks through why running PyTorch directly on the host was painful, how I ended up with a **Docker-based dev container**, and the one obscure setting that made the whole thing finally work:

```json
"containerEnv": {
  "HSA_OVERRIDE_GFX_VERSION": "11.0.0"
}

```

The working dev container lives here if you want to jump straight to the code: `cicorias/devcontainer-pytorch-amd-rocm-ryzen-ai-9`.[1](https://github.com/cicorias/devcontainer-pytorch-amd-rocm-ryzen-ai-9)

---

## The obvious approach: just install ROCm + PyTorch on the host

My first attempt was the “by the book” path:

1. Install AMDGPU/ROCm drivers on the host.
2. Follow AMD’s PyTorch-on-ROCm guidance with `pip` or the ROCm wheels.2
3. Create a Python env, install PyTorch with ROCm, run `torch.cuda.is_available()` and call it a day.

In reality:

- The **support matrix for Ryzen AI APUs is still moving** and often lags behind the hardware shipping in laptops like the Framework 13. AMD is adding support in recent ROCm and PyTorch builds, but it’s still in “preview” territory in docs and blogs.
- I didn’t want my **host Python environment pinned** to whatever ROCm-era PyTorch version happened to work this week.
- Some combinations of distro kernel, ROCm driver, and PyTorch wheels **simply refused to cooperate**, and rolling back was messy.

After a couple of cycles of “works in one shell, explodes in another”, I stopped treating this as a host configuration problem and started treating PyTorch + ROCm as **an appliance problem**.

---

## Moving PyTorch + ROCm into a dev container

Instead of building the stack on the host, I leaned on a strategy AMD itself recommends: [use a pre-built Docker image with PyTorch and ROCm that they actually test](https://rocm.docs.amd.com/projects/install-on-linux/en/develop/install/3rd-party/pytorch-install.html#using-docker-with-pytorch-pre-installed).

I ended up using this base image in a VS Code dev container:

```text
rocm/pytorch:rocm7.1_ubuntu24.04_py3.12_pytorch_release_2.8.0

```

That image gives me:

- **Ubuntu 24.04**
- **Python 3.12**
- **PyTorch 2.8.0** built for **ROCm 7.1**
- A ROCm stack that’s internally consistent

The repo wraps this in a VS Code devcontainer definition so that opening the folder and choosing **“Reopen in Container”** gives you a fully configured PyTorch + ROCm environment on Ryzen AI.1

The split looks like this:

- The **host** only needs:
  - AMD GPU/ROCm drivers
  - Docker with GPU support
  - VS Code + Dev Containers extension6
- The **container**:
  - Runs the AMD PyTorch ROCm image
  - Mounts the GPU devices from the host
  - Sets a couple of magic environment variables so ROCm recognizes the Ryzen AI GPU

The most important one of those env vars is `HSA_OVERRIDE_GFX_VERSION`.

---

## The critical `HSA_OVERRIDE_GFX_VERSION` knob

On current Ryzen AI / RDNA3-based iGPUs, ROCm isn’t always fully wired up out of the box. A common workaround is to **tell the HSA runtime to pretend the GPU is a specific GFX version** using `HSA_OVERRIDE_GFX_VERSION`.

You’ll see this pattern in various community threads: map GPU families to graphics core (GFX) versions and use `HSA_OVERRIDE_GFX_VERSION` to get ROCm to treat newer hardware as a supported class.7

For RDNA 3–class GPUs (like the Radeon 890M in the Framework 13), the value that worked for me was:

```bash
HSA_OVERRIDE_GFX_VERSION=11.0.0

```

Without that, I saw behavior like:

- `rocm-smi` mostly working
- But crashes in Juptyer with unknown exceptions

Once I set this **inside the container**, things snapped into place:

- `torch.cuda.is_available()` → `True`
- `torch.cuda.get_device_name(0)` → expected Radeon iGPU
- Simple test models ran on the GPU without drama

Because I wanted this to be automatic in VS Code, I put it in the `containerEnv` section of `.devcontainer/devcontainer.json`:

```json
"containerEnv": {
  "HSA_OVERRIDE_GFX_VERSION": "11.0.0"
}

```

That one line is the difference between “this laptop is useless for PyTorch” and “this is a perfectly fine dev box.”

---

## Wiring the GPU into the container

The other critical piece is giving the container access to the actual GPU devices.

In this setup, the container gets:

- `/dev/kfd` – HSA/ROCm kernel driver interface
- `/dev/dri` – Direct Rendering Interface devices (DRM, GPU nodes)

The devcontainer uses `runArgs` to pass those through and ensure the container’s user is in the right group:

```jsonc
"runArgs": [
  "--device=/dev/kfd",
  "--device=/dev/dri",
  "--group-add=video",
  "--ipc=host",
  "--shm-size=8g"
]

```

A few notes:

- `--group-add=video` is needed because on most distros, the GPU devices are owned by `root:video`. If your user isn’t in that group, access fails.
- `--ipc=host` and a larger `--shm-size` are just practical ML dev settings (Jupyter, dataloaders, etc.).
- In the template I run the container as `root` to avoid permission whack-a-mole; you can harden this later if you want.1

---

## Why this pattern matters

On newer AMD hardware like the **Ryzen AI 9 HX 370**, support is evolving:

- ROCm versions are incrementally adding preview support for these APUs.234
- PyTorch ROCm builds need to line up with the ROCm version, driver stack, and Python version.

If you try to line all of that up **on the host**, you get:

- A fragile combination of distro packages, kernel versions, ROCm builds, and Python environments.
- A setup that’s hard to reproduce on another machine or even the same model with a slightly different distro.

By using:

- **AMD’s own `rocm/pytorch` images**, which are built and tested as a unit,25
- **A devcontainer** that wires in only the GPU devices and a small set of env vars,

you get a few non-obvious benefits:

1. **Reproducibility**  
   Clone the repo on another Ryzen AI machine, open in VS Code, “Reopen in Container”, and you’re running the same stack.
2. **Host sanity**  
   Your host Python environments stay clean. If ROCm or PyTorch break on some future update, it’s a container rebuild, not an OS reinstall.
3. **Clear abstraction boundary**  
   The host is responsible for:
   - GPU drivers
   - Docker  
     The AI/ML stack lives entirely in the container and can evolve independently.
4. **Easy upgrades**  
   When AMD publishes a new `rocm/pytorch` tag (e.g., a newer ROCm or PyTorch), you bump the image reference in `devcontainer.json` and test it without touching the host.

In short: **containers let you treat PyTorch + ROCm on AMD as an appliance**, and `HSA_OVERRIDE_GFX_VERSION=11.0.0` is the knob that actually lets that appliance talk to the Ryzen AI GPU.

---

## Full `.devcontainer/devcontainer.json`

Here’s a self-contained `.devcontainer/devcontainer.json` that has been working on the Framework 13 / Ryzen AI 9:

```jsonc
{
  "name": "pytorch-rocm-ryzen-ai-9",
  "image": "rocm/pytorch:rocm7.1_ubuntu24.04_py3.12_pytorch_release_2.8.0",

  // Give the container direct access to the AMD iGPU
  "runArgs": [
    "--device=/dev/kfd",
    "--device=/dev/dri",
    "--group-add=video",
    "--ipc=host",
    "--shm-size=8g"
  ],

  // Critical for Ryzen AI / RDNA3-class iGPUs
  "containerEnv": {
    "HSA_OVERRIDE_GFX_VERSION": "11.0.0"
  },

  // Install your Python deps into an isolated venv
  "postCreateCommand": "python -m venv /opt/venv && /opt/venv/bin/pip install -r requirements.txt",

  "remoteUser": "root",

  "customizations": {
    "vscode": {
      "settings": {
        "python.defaultInterpreterPath": "/opt/venv/bin/python",
        "jupyter.jupyterServerType": "local"
      },
      "extensions": [
        "ms-python.python",
        "ms-toolsai.jupyter",
        "GitHub.copilot-chat"
      ]
    }
  },

  "features": {}
}

```

A minimal `requirements.txt` to go with it:

```text
jupyterlab==4.5.0
matplotlib==3.10.7
pandas==2.3.3
scikit-learn==1.6.1
# add any other project-specific deps here

```

That’s essentially what the `devcontainer-pytorch-amd-rocm-ryzen-ai-9` repo contains, just trimmed down for the core scenario.1

---

## Verifying that the GPU is actually being used

Once the container is up:

Then verify from Python:

```python
import torch

print(f"PyTorch version: {torch.__version__}")
print(f"ROCm available: {torch.cuda.is_available()}")

if torch.cuda.is_available():
    print(f"GPU device: {torch.cuda.get_device_name(0)}")
    x = torch.randn(1024, 1024, device="cuda")
    y = torch.matmul(x, x)
    print("Matmul OK on GPU, shape:", y.shape)
else:
    print("No ROCm GPU detected")

```

Open a terminal **inside** the devcontainer and run:

```bash
rocm-smi

```

You should see your GPU entry (Radeon 890M / GFX11-class).

If `torch.cuda.is_available()` is `False`, the first things to check:

- Does `rocm-smi` see the GPU from **inside** the container?
- Are `/dev/kfd` and `/dev/dri` present in the container?
- Is `HSA_OVERRIDE_GFX_VERSION` actually set to `11.0.0` inside the container environment?

---

## Running the same setup without VS Code (plain Docker)

If you don’t want to use VS Code devcontainers, the equivalent raw `docker run` command is:

```bash
docker run -it --rm \
  --device=/dev/kfd \
  --device=/dev/dri \
  --group-add video \
  --ipc=host \
  --shm-size 8g \
  -e HSA_OVERRIDE_GFX_VERSION=11.0.0 \
  -v "$PWD":/workspace \
  -w /workspace \
  rocm/pytorch:rocm7.1_ubuntu24.04_py3.12_pytorch_release_2.8.0 \
  bash

```

From there you can:

```bash
python -m venv /opt/venv
source /opt/venv/bin/activate
pip install -r requirements.txt
python your_script.py

```

Same environment, just without the VS Code glue.

---

## Footnotes

- GitHub – devcontainer for PyTorch + AMD ROCm + Ryzen AI 9:  
  <https://github.com/cicorias/devcontainer-pytorch-amd-rocm-ryzen-ai-9>
- AMD ROCm documentation – Installing PyTorch for ROCm:  
  <https://rocm.docs.amd.com/projects/install-pytorch/en/latest/>
- AMD GPUOpen – Beginner’s guide to deploying LLMs with AMD on Windows using PyTorch (Ryzen AI 9 HX 370):  
  <https://gpuopen.com/learn/ai-ml/beginners-guide-to-llm-deployment-amd/>
- Linuxcontainers – community notes on ROCm and `HSA_OVERRIDE_GFX_VERSION` usage for GFX11:  
  <https://discuss.linuxcontainers.org/t/rocm-and-lxd-gpu-access/>
- Framework Community – ROCm support for Ryzen AI / Framework AMD laptops:  
  <https://community.frame.work/>
- Docker Hub – official AMD ROCm PyTorch images (`rocm/pytorch`):  
  <https://hub.docker.com/r/rocm/pytorch>
- Visual Studio Code – Dev Containers documentation:  
  <https://code.visualstudio.com/docs/devcontainers/containers>
