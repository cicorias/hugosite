---
title: "Windows 10 Hyper-V - Finally a NAT Option..."
date: 2016-08-19T16:47:51+0000
lastmod: 2016-08-19T16:47:51+0000
slug: "windows-10-hyper-v-finally-a-nat-option"
feature_image: "https://www.cicoria.com/content/images/2016/08/network-virtualization-sdn.jpg"
aliases:
  - /windows-10-hyper-v-finally-a-nat-option/
---

Not sure about you but I've been waiting a long time for NAT to be part of HyperV on Windows client. The "other" guys have it - and for a long time too.

Now, with [Nested Virtualization](https://msdn.microsoft.com/en-us/virtualization/hyperv_on_windows/user_guide/nesting) and [NAT](https://msdn.microsoft.com/en-us/virtualization/hyperv_on_windows/user_guide/setup_nat_network) support, my world is nearly complete...

To enable it though on Windows 10, I don't believe there's anything in HyperV Manager that allows that.

But, [PowerShell](https://azure.microsoft.com/en-us/blog/powershell-is-open-sourced-and-is-available-on-linux/), and now that's x-plat too, to the rescue.

The below will create a single NAT device on the Virtual Switch and machines will be in the `192.168.10.0/24` network. If you want to change that range, just be sure to update the gateway IP (below it's the `192.168.10.1`) - there's some CIDR notation too.

```
$natName = "NATSwitch"

New-VMSwitch -SwitchName $natName -SwitchType Internal

$interface = Get-NetAdapter | where {$_.name -like "*$natName*" }

New-NetIPAddress -IPAddress 192.168.10.1 -PrefixLength 24 -InterfaceIndex $interface.ifIndex
New-NetNat -Name "MyNATNetwork" -InternalIPInterfaceAddressPrefix 192.168.10.0/24

```
