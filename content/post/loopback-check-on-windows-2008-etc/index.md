---
title: "Loopback Check on Windows 2008, etc."
date: 2009-11-17T05:21:38+0000
lastmod: 2009-11-17T05:21:38+0000
slug: "loopback-check-on-windows-2008-etc"
aliases:
  - /loopback-check-on-windows-2008-etc/
---

This KB article ([KB926642](http://support.microsoft.com/kb/926642)) explains 2 methods for handling the scenarios that we as developers require for using a local machine for development.  My option has been, going forward, of being explicitly in the host names that my development machine will use.  From that article:

Method 1 (recommended): Create the Local Security Authority host names that can be referenced in an NTLM authentication request

To do this, follow these steps for all the nodes on the client computer:

1. Click **Start**, click **Run**, type regedit, and then click **OK**.
2. Locate and then click the following registry subkey: **HKEY\_LOCAL\_MACHINE\SYSTEM\CurrentControlSet\Control\Lsa\MSV1\_0**
3. Right-click **MSV1\_0**, point to **New**, and then click **Multi-String Value**.
4. In the **Name** column, type BackConnectionHostNames, and then press ENTER.
5. Right-click **BackConnectionHostNames**, and then click **Modify**.
6. In the **Value** data box, type the CNAME or the DNS alias, that is used for the local shares on the computer, and then click **OK**.   
   **Note** Type each host name on a separate line.   
   **Note** If the BackConnectionHostNames registry entry exists as a REG\_DWORD type, you have to delete the BackConnectionHostNames registry entry.
7. Exit Registry Editor, and then restart the computer.
