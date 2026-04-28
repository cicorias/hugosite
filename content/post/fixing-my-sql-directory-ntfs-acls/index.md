---
title: "Fixing my SQL Directory NTFS ACLS"
date: 2010-03-12T05:26:29+0000
lastmod: 2010-03-12T05:26:29+0000
slug: "fixing-my-sql-directory-ntfs-acls"
aliases:
  - /fixing-my-sql-directory-ntfs-acls/
---

I run my development server by boot to VHD (Windows Server 2008 R2 x64).  In that instance, I also have an attached VHD (I attach via script at boot up time using Task Scheduler).  That VHD I have my SQL instances installed.

So, the other day, acting hasty, I chmod my ACLS – wow, what a day after that.

So, in order to fix it I created this set of BAT commands that resets it back to operational state – not 100% of all what you get, I also didn’t want to run a “repair” – but, all operational again.

```
setlocal

SET Inst100Path=H:\Program Files\Microsoft SQL Server\100

REM GOTO SQLE

SET InstanceName=MSSQLSERVER  

SET InstIdPath=H:\Program Files\Microsoft SQL Server\MSSQL10.%InstanceName%  

SET Group=SQLServerMSSQLUser$SCICORIA-HV1$%InstanceName%  

SET AgentGroup=SQLServerSQLAgentUser$SCICORIA-HV1$%InstanceName%

ICACLS "%InstIdPath%\MSSQL"  /T /Q /grant "%Group%":(OI)(CI)FX  

ICACLS "%InstIdPath%\MSSQL\backup"  /T /Q /grant "%Group%":(OI)(CI)F  

ICACLS "%InstIdPath%\MSSQL\data"  /T /Q /grant "%Group%":(OI)(CI)F  

ICACLS "%InstIdPath%\MSSQL\FTdata" /T /Q /grant "%Group%":(OI)(CI)F  

ICACLS "%InstIdPath%\MSSQL\Jobs" /T /Q /grant "%Group%":(OI)(CI)F  

ICACLS "%InstIdPath%\MSSQL\binn"  /T /Q /grant "%Group%":(OI)(CI)RX  

ICACLS "%InstIdPath%\MSSQL\Log"  /T /Q /grant "%Group%":(OI)(CI)F

ICACLS "%Inst100Path%"  /T /Q /grant "%Group%":(OI)(CI)RX  

ICACLS "%Inst100Path%\shared\Errordumps"  /T /Q /grant "%Group%":(OI)(CI)RXW

ICACLS "%InstIdPath%\MSSQL"  /T /Q /grant "%AgentGroup%":(OI)(CI)RX  

ICACLS "%InstIdPath%\MSSQL\binn"  /T /Q /grant "%AgentGroup%":(OI)(CI)F  

ICACLS "%InstIdPath%\MSSQL\Log"  /T /Q /grant "%AgentGroup%":(OI)(CI)F

ICACLS "%Inst100Path%"  /T /Q /grant "%AgentGroup%":(OI)(CI)RX

REM THIS IS THE SQL EXPRESS INSTANCE

:SQLE

SET InstanceName=SQLEXPRESS  

SET InstIdPath=H:\Program Files\Microsoft SQL Server\MSSQL10.%InstanceName%  

SET Group=SQLServerMSSQLUser$SCICORIA-HV1$%InstanceName%  

SET AgentGroup=SQLServerSQLAgentUser$SCICORIA-HV1$%InstanceName%

ICACLS "%InstIdPath%\MSSQL"  /T /Q /grant "%Group%":(OI)(CI)FX  

ICACLS "%InstIdPath%\MSSQL\backup"  /T /Q /grant "%Group%":(OI)(CI)F  

ICACLS "%InstIdPath%\MSSQL\data"  /T /Q /grant "%Group%":(OI)(CI)F  

ICACLS "%InstIdPath%\MSSQL\FTdata" /T /Q /grant "%Group%":(OI)(CI)F  

ICACLS "%InstIdPath%\MSSQL\Jobs" /T /Q /grant "%Group%":(OI)(CI)F  

ICACLS "%InstIdPath%\MSSQL\binn"  /T /Q /grant "%Group%":(OI)(CI)RX  

ICACLS "%InstIdPath%\MSSQL\Log"  /T /Q /grant "%Group%":(OI)(CI)F

ICACLS "%Inst100Path%"  /T /Q /grant "%Group%":(OI)(CI)RX  

ICACLS "%Inst100Path%\shared\Errordumps"  /T /Q /grant "%Group%":(OI)(CI)RXW

ICACLS "%InstIdPath%\MSSQL"  /T /Q /grant "%AgentGroup%":(OI)(CI)RX  

ICACLS "%InstIdPath%\MSSQL\binn"  /T /Q /grant "%AgentGroup%":(OI)(CI)F  

ICACLS "%InstIdPath%\MSSQL\Log"  /T /Q /grant "%AgentGroup%":(OI)(CI)F

ICACLS "%Inst100Path%"  /T /Q /grant "%AgentGroup%":(OI)(CI)RX

endlocal

```
