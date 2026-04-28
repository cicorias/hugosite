---
title: "Extending SQL 2008 R2 Master Data Services (MDS) with IWorkflowTypeExtender"
date: 2010-11-14T08:57:30+0000
lastmod: 2010-11-14T08:57:30+0000
slug: "extending-sql-2008-r2-master-data-services-mds-with-iworkflowtypeextender"
aliases:
  - /extending-sql-2008-r2-master-data-services-mds-with-iworkflowtypeextender/
---

During hierarchy changes, MDS provides some basic rules for validating hierarchy members against some logic that is defined in the model within the MDS interface or through the Services interface.  Behind the scenes, MDS is generating all sorts of T-SQL to ultimately enforce these rules.

There is the ability to extend these rules with your own custom implementation if the configuration driven rules don’t suffice – either a SharePoint workflow or through custom CLR code packaged as an assembly.

For the custom code approach, you need to extend IWorkflowTypeExtender which is present in the “Microsoft.MasterDataServices.Core” [1] assembly.

Before you proceed is best to get the latest cumulative updates for MDS – see [2] – for this sample, I’ve used CU #4 [3].  There are some important fixes to MDS that address basic things and ensure you have a much better experience configuring your rules.

There are 2 options for custom workflows:

1. Call a SharePoint workflow hosted in a site

2. Provide an implementation of IWorkflowTypeExtender [4]

With the first option, SharePoint hosted workflow, in the rules editor you’ll provide a “key” of SPWF as the identifier for the workflow type, along with the URL of the site/web.  From this the MDS Workflow Windows service will then using the SharePoint object model (you’ll have to have this service running on the same box as SharePoint as it makes calls to the Server side SP Object Model (SPSite, SPWeb, SPWorkflowManager, et.al.)

For anything other than SPWF, the MDS Workflow service will resolve your type from assemblies as defined in the config file.  Rules for fusion apply.

The architecture of this custom rules is that MDS, when a rule is configured to use a workflow, will write a message to a SQL Service Broker queue.  Right now, out-of-the-box, the MDS Workflow service is designed to read these messages that are written there. In reality, you could write your own process/code hosted somewhere else that retrieves these messages.

[![image](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/3554.image_thumb_0E97EC99.png "image")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/4213.image_02E2A567.png)

1. Configure a rule to use a Workflow – the the rule below the condition forces it to fire on all changes.

[![image](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/7268.image_thumb_1E57819D.png "image")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/3058.image_3F4AF444.png)

For the Actions, the Workflow type in a custom extender references a key value in the config file for the service.  You can provide as many as you need in the config that implement the interface IWorkflowTypeExtender.

Note that I’ve also supplied both a Workflow site and Workflow name setting.  These tags are sent along in the “message” so, even for non-SP Workflows, our custom types can use these as additional values for logic. Again, not needed, but helps provide more context for our rule.

2. Modify an entity

Once you modify an entity, since our rule is without condition, MDS will write a message to the service broker queue.  At this point, whoever is listening will see the message.  For MDS, the Workflow service (Microsoft.MasterDataServices.Workflow.exe)  calls the Stored Procedure “EXEC [mdm].[udpExternalActionsGet” which returns the XML to the Workflow Service and de-queues the message.  This is done outside of a System.Transactions.TransactionScope – so, could be a good reason to write your own Workflow handler.

Once the message is de-queued, the extender is called  - there is one instance that it get’s instantiated once at Workflow Service startup – calling the StartWorkflow method with the key (type of Workflow specified in the rules editor) and an XmlElement – similar to the following:

```
<ExternalAction>
  <Type>PAC</Type>
  <SendData>1</SendData>
  <Server_URL>http://mysite</Server_URL>
  <Action_ID>simpleWF</Action_ID>
  <Model_ID>2</Model_ID>
  <Model_Name>SimpleModel1</Model_Name>
  <Entity_ID>6</Entity_ID>
  <Entity_Name>SimpleModel1</Entity_Name>
  <Version_ID>2</Version_ID>
  <MemberType_ID>1</MemberType_ID>
  <Member_ID>1</Member_ID>
  <MemberData>
    <ID>1</ID>
    <Version_ID>2</Version_ID>
    <ValidationStatus_ID>3</ValidationStatus_ID>
    <ChangeTrackingMask>0</ChangeTrackingMask>
    <EnterDTM>2010-11-13T21:00:43.040</EnterDTM>
    <EnterUserID>1</EnterUserID>
    <EnterUserName>cicorias-xps15\cicorias</EnterUserName>
    <EnterUserMuid>548AFA9A-B8A1-42D7-8575-6F266CD4055A</EnterUserMuid>
    <EnterVersionId>2</EnterVersionId>
    <EnterVersionName>VERSION_1</EnterVersionName>
    <EnterVersionMuid>FEDE9599-7AF4-4960-960E-C900D9A78457</EnterVersionMuid>
    <LastChgDTM>2010-11-14T21:44:58.070</LastChgDTM>
    <LastChgUserID>1</LastChgUserID>
    <LastChgUserName>cicorias-xps15\cicorias</LastChgUserName>
    <LastChgUserMuid>548AFA9A-B8A1-42D7-8575-6F266CD4055A</LastChgUserMuid>
    <LastChgVersionId>2</LastChgVersionId>
    <LastChgVersionName>VERSION_1</LastChgVersionName>
    <LastChgVersionMuid>FEDE9599-7AF4-4960-960E-C900D9A78457</LastChgVersionMuid>
    <Name>Main</Name>
    <Code>1234</Code>
    <ValidCheck>222.00</ValidCheck>
  </MemberData>
</ExternalAction>
```

For the Workflow Service to load the sample type I just put a post build event to copy the Assembly (DLL) to the custombin path of where the Workflow Service is run from

C:\Program Files\Microsoft SQL Server\Master Data Services\WebApplication\bin

You must modify the the config file Microsoft.MasterDataServices.Workflow.exe.config specifing your types, and for this I modified the probing settings so my assembly can be in a sub directory.  You can also deploy to the GAC.

```
  <runtime>
    <assemblyBinding xmlns="urn:schemas-microsoft-com:asm.v1">
      <probing privatePath="bin;custombin"/>
    </assemblyBinding>
  </runtime>
```

Also, the project runs the Microsoft.MasterDataServices.Workflow.exe process, passing the “-console” switch to the executable so it can start in console mode instead of running it as a service and making debugging a little easier.

The appSettings section of the Workflow Service config file determines what DB to attach to along with what Workflow Extenders to load.  All the types are specified as a single value semicolon separated “;” and prefixed with the <KEY>=<full assembly name>

A sample is below that loads 2 types:

```
  <applicationSettings>
    <Microsoft.MasterDataServices.Workflow.Properties.Settings>
      <setting name="ConnectionString"
               serializeAs="String">
        <value>Server=.;Database=SQL_MDS1;Integrated Security=SSPI</value>
      </setting>
      <setting name="WorkflowTypeExtenders"
               serializeAs="String">
        <value>PAC=WorkflowTasks.SimpleHello, WorkflowTasks, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null;OOB=Microsoft.MasterDataServices.Workflow.WorkflowTypeTest, Microsoft.MasterDataServices.Workflow, Version=10.0.0.0, Culture=neutral, PublicKeyToken=89845dcd8080cc91</value>
      </setting>
    </Microsoft.MasterDataServices.Workflow.Properties.Settings>
  </applicationSettings>
```

Solution File [SQL\_MDS\_WorkflowTest.zip](http://cicoria.com/downloads/SQL_MDS_WorkflowTest.zip)

[1] C:\Program Files\Microsoft SQL Server\Master Data Services\WebApplication\bin\Microsoft.MasterDataServices.Core.dll

[2] [http://sqlblog.com/blogs/mds\_team/archive/2010/08/25/downloading-and-installing-sql-server-2008-r2-master-data-services-mds-cumulative-updates.aspx](http://sqlblog.com/blogs/mds_team/archive/2010/08/25/downloading-and-installing-sql-server-2008-r2-master-data-services-mds-cumulative-updates.aspx "http://sqlblog.com/blogs/mds_team/archive/2010/08/25/downloading-and-installing-sql-server-2008-r2-master-data-services-mds-cumulative-updates.aspx")

[3] [http://support.microsoft.com/kb/2345451](http://support.microsoft.com/kb/2345451 "http://support.microsoft.com/kb/2345451")

[4] Microsoft.MasterDataServices.Core.Workflow.IWorkflowTypeExtender – there is a sample Microsoft.MasterDataServices.Workflow.WorkflowTypeTest in the EXE assembly
