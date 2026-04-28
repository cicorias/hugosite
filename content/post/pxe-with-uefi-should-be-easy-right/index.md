---
title: "PXE with UEFI should be easy, right"
date: 2025-08-27T13:12:55+0000
lastmod: 2025-08-27T13:12:55+0000
slug: "pxe-with-uefi-should-be-easy-right"
summary: "UEFI PXE setup on Ubuntu simplified using scripts, TFTP, DHCP, NFS, HTTP, GRUB, Syslinux, resolving loader handoffs and configuration pitfalls."
tags: ["bash", "fun", "iot", "shell", "utilities", "vm"]
feature_image: "/images/2025/08/image.jpg"
aliases:
  - /pxe-with-uefi-should-be-easy-right/
---

I have been writing code and herding servers for four decades. I still enjoy the smell of a clean boot in the morning. So, when I set out to build a clean PXE setup for modern UEFI clients on Ubuntu Server 24.04, I figured it would be a pleasant afternoon. Then UEFI whispered to hold my beverage.

The good news is I did get it working, and I wrapped the moving parts into a tidy repo so you do not have to spelunk through ancient forum posts. The less good news is that the path from power on to installer menu still hides a few banana peels. UEFI might as well stand for You Eventually Figure It out. ([GitHub](https://github.com/cicorias/pxe-server-setup))

## What I built

The project aims for a straight Ubuntu Server 24.04 experience using native packages. No iPXE requirement. No mystery blobs. Just an automated, idempotent set of scripts that stand up TFTP, optional DHCP, NFS, and HTTP, then tie them together so clients can net boot and install multiple systems. Think batteries included with a clear wiring diagram. ([GitHub](https://github.com/cicorias/pxe-server-setup))

### Features at a glance

- Native Ubuntu packages with no iPXE dependency
- Flexible DHCP model that can be local to the box or coexist with an existing network service
- Support for multiple ISO images with simple add steps
- Idempotent installer scripts and an organized layout so you can rerun safely  
  That is the promise, and it sticks to it. ([GitHub](https://github.com/cicorias/pxe-server-setup))

## Code base tour

The layout is clean and predictable. At the top you have a README that explains the flow. Under scripts you will find a numbered series that build the stack in safe steps. There is also a config shell file for your network values. Artifacts are split by role, with separate spots for ISO storage, TFTP content, and HTTP content. When you read that, you can basically map client requests to server directories in your head. ([GitHub](https://github.com/cicorias/pxe-server-setup))

Highlights from the script set

- ├── 01-prerequisites.sh
- ├── 02-packages.sh
- ├── 03-tftp-setup.sh
- ├── 04-dhcp-setup.sh
- ├── 05-nfs-setup.sh
- ├── 06-http-setup.sh
- ├── 07-pxe-menu.sh
- ├── 08-iso-manager.sh
- ├── 09-uefi-pxe-setup.sh
- ├── 99-cleanup.sh
- ├── config.sh
- ├── config.sh.example
- ├── test-pxe-client-access.sh
- └── validate-pxe.sh

Each one is focused and can be run on its own, or you can use the `./install.sh` driver to orchestrate the full sequence. ([GitHub](https://github.com/cicorias/pxe-server-setup))

## Software used and how it fits

The build uses the standard Ubuntu services you would expect

- TFTP served by the usual hpa daemon for tiny boot files
- Optional DHCP using the ISC server if you want an isolated lab or a known pool
- NFS to provide install media and other resources where needed
- HTTP via nginx for fast delivery of larger files
- Syslinux to serve legacy BIOS clients with pxelinux dot zero
- GRUB EFI for UEFI clients with the expected `bootx64.efi` entry point

This mix keeps TFTP for the tiny bits and moves heavy lifting to HTTP or NFS where it belongs. ([GitHub](https://github.com/cicorias/pxe-server-setup))

Ports are what you would expect as well. DHCP on 67 and 68 when you run the local service. TFTP on 69. HTTP on eighty. NFS on two 2049. If you know these by heart you probably also keep a null modem cable nearby for luck. ([GitHub](https://github.com/cicorias/pxe-server-setup))

## UEFI reality check

Legacy BIOS PXE is a comfy old hoodie. UEFI adds some ceremony. The project leans on GRUB EFI for UEFI clients and keeps Syslinux for BIOS clients, so both worlds can boot from the same host. For gen two virtual machines in Hyper-V you will use the UEFI setup step, and you must disable Secure Boot on the target client machines – for now, as adding a signed image is next. Once I did that, GRUB came up and the menu behaved as expected. ([GitHub](https://github.com/cicorias/pxe-server-setup))

On the DHCP side, UEFI clients need the right architecture hints so they are handed the GRUB EFI loader rather than pxelinux. The scripts handle that mapping and keep both client types happy. Pool defaults are sensible and documented, including an example range in the `10.1.1.0/24` range for lab use. ([GitHub](https://github.com/cicorias/pxe-server-setup))

## The parts that made me mutter

Two themes showed up while I refined the flow

- Order matters more than you want to admit. Get the package set and filesystem layout in place before you touch the menus. Otherwise, you will chase missing paths that only show up when a client asks for them. The numbered scripts help keep you honest. ([GitHub](https://github.com/cicorias/pxe-server-setup))
- UEFI is picky about the loader handoff. If you see a client loop back to the menu, check that Secure Boot is off for the test VM and that GRUB EFI is reachable at the expected path under TFTP. Then verify the DHCP options for the UEFI architecture code. The UEFI script takes care of the GRUB menu and loader copy so you do not have to guess. ([GitHub](https://github.com/cicorias/pxe-server-setup))

## How to run it without losing a weekend

Here is the fast path I recommend

- Clone the repo and read the top of the README to understand the moving parts: <https://github.com/cicorias/pxe-server-setup>
- Copy the example `config.example.sh` file to `config.sh`, then set your interface, server address, subnet, mask, and gateway
- Run the install driver - `sudo ./install.sh --local-dhcp`.
- If you will boot modern clients, run the UEFI step for GRUB and menu setup
- Add one or more ISO images through the iso manager script, then reboot a client and watch the menu pop up

The README shows each step in this exact order for a reason, and you can rerun steps safely to nudge settings without tearing the whole thing down. ([GitHub](https://github.com/cicorias/pxe-server-setup))

## Why this should not be hard, but still is

A PXE stack is simple in principle. A small loader from TFTP pivots to a richer protocol for the big bits, and the installer does the rest. The complexity comes from the seams between components. DHCP needs to identify the client type and point at the right next step. TFTP has to expose the exact path the loader expects. UEFI wants its blessed loader and a menu that speaks its dialect. Miss any one of those and the client shrugs and reboots. This project stitches those seams with clear defaults and an installer that refuses to guess. ([GitHub](https://github.com/cicorias/pxe-server-setup))

## Closing notes

If you take anything from this, let it be that boring is beautiful. Use the native Ubuntu services. Keep TFTP tiny. Let HTTP and NFS do the heavy lifting. Treat DHCP as the traffic cop. With that mindset the repo becomes a repeatable template you can use in a lab or at a branch office. And if you catch yourself talking to the firmware, you are not alone. I once tried to negotiate with a boot menu. It told me to press any key to continue and I took the hint. ([GitHub](https://github.com/cicorias/pxe-server-setup))

If you want the full walkthrough, scripts, and notes, the project page has all the details and a quick start that matches the flow I described. Happy net booting. ([GitHub](https://github.com/cicorias/pxe-server-setup))
