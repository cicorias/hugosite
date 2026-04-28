---
title: "Running Jetty under Windows Azure Using RoleEntryPoint in a Worker Role"
date: 2011-03-03T11:10:16+0000
lastmod: 2011-03-03T11:10:16+0000
slug: "running-jetty-under-windows-azure-using-roleentrypoint-in-a-worker-role"
aliases:
  - /running-jetty-under-windows-azure-using-roleentrypoint-in-a-worker-role/
---

This post is built upon the work of [Mario Kosmiskas](http://blogs.msdn.com/b/mariok) and [David C. Chou’s](http://blogs.msdn.com/b/dachou) prior postings – from here:

[http://blogs.msdn.com/b/mariok/archive/2011/01/05/deploying-java-applications-in-azure.aspx](http://blogs.msdn.com/b/mariok/archive/2011/01/05/deploying-java-applications-in-azure.aspx "http://blogs.msdn.com/b/mariok/archive/2011/01/05/deploying-java-applications-in-azure.aspx")

[http://blogs.msdn.com/b/dachou/archive/2010/03/21/run-java-with-jetty-in-windows-azure.aspx](http://blogs.msdn.com/b/dachou/archive/2010/03/21/run-java-with-jetty-in-windows-azure.aspx "http://blogs.msdn.com/b/dachou/archive/2010/03/21/run-java-with-jetty-in-windows-azure.aspx")

As Mario points out in his post, when you need to have more control over the process that starts, it generally is better left to a RoleEntryPoint capability that as of now, requires the use of a CLR based assembly that is deployed as part of the package to Azure.

There were things I liked especially about Mario’s post – specifically, the ability to pull down the JRE and Jetty runtimes at role startup and instantiate the process using the extracted bits.  The way Mario initialized the java process (and Jetty) was to take advantage of a role startup task configured as part of the service definition.  This is a great quick way to kick off processes or tasks prior to your role entry point.  However, if you need access to service configuration values or role events, that’s where RoleEntryPoint comes in.  For this PoC sample I moved the logic for retrieving the bits for the jre and jetty to the worker roles OnStart – in addition to moving the process kickoff to the OnStart method.  The Run method at this point is there to loop and just report the status of the java process. Beyond just making things more parameterized, both Mario’s and David’s articles still form the essence of the approach.

The solution that accompanies this post provides all the necessary .NET based Visual Studio project.  In addition, you’ll need:

1. Jetty 7 runtime [http://www.eclipse.org/jetty/downloads.php](http://www.eclipse.org/jetty/downloads.php "http://www.eclipse.org/jetty/downloads.php")

2. JRE [http://www.oracle.com/technetwork/java/javase/downloads/index.html](http://www.oracle.com/technetwork/java/javase/downloads/index.html "http://www.oracle.com/technetwork/java/javase/downloads/index.html")

Once you have these the first step is to create archives (zips) of the distributions.  For this PoC, the structure of the archive requires that the root of the archive looks as follows:

JRE6.zip

[![3-3-2011 6-55-32 PM](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/2318.3-3-2011-6-55-32-PM_thumb_524199B2.png "3-3-2011 6-55-32 PM")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/0576.3-3-2011-6-55-32-PM_7AC07BC6.png)

jetty---.zip

[![3-3-2011 6-56-37 PM](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/8081.3-3-2011-6-56-37-PM_thumb_03EC913B.png "3-3-2011 6-56-37 PM")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/1663.3-3-2011-6-56-37-PM_6A65040D.png)

Upload the contents to a storage container (block blob), and for this example I used /archives as the location.  The service configuration has several settings that allow, which is the advantage of using RoleEntryPoint, the ability to provide these things via native configuration support from Azure in a worker role.

Storage Explorer

[![3-3-2011 7-00-17 PM](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/0160.3-3-2011-7-00-17-PM_thumb_19F2FCCD.png "3-3-2011 7-00-17 PM")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/1256.3-3-2011-7-00-17-PM_1C0FFB96.png)

You can use development storage for testing this out – the zipped version of the solution is configured for development storage.  When you’re ready to deploy, you update the two settings – 1 for diagnostics and the other for the storage container where the /archives are going to be stored.

```
<?xml version="1.0" encoding="utf-8"?>
<ServiceConfiguration serviceName="HostedJetty"
       xmlns="http://schemas.microsoft.com/ServiceHosting/2008/10/ServiceConfiguration"
       osFamily="2"
       osVersion="*">
  <Role name="JettyWorker">
    <Instances count="1" />
    <ConfigurationSettings>
      <!--<Setting name="Microsoft.WindowsAzure.Plugins.Diagnostics.ConnectionString"
value="DefaultEndpointsProtocol=https;AccountName=<accountName>;AccountKey=<accountKey>" />-->
      <Setting name="Microsoft.WindowsAzure.Plugins.Diagnostics.ConnectionString"
value="UseDevelopmentStorage=true" />
      <Setting name="JettyArchive"
value="jetty-distribution-7.3.0.v20110203b.zip" />
      <Setting name="StartRole"
value="true" />
      <Setting name="BlobContainer"
value="archives" />
      <Setting name="JreArchive"
value="jre6.zip" />
      <!--<Setting name="StorageCredentials"
value="DefaultEndpointsProtocol=https;AccountName=<accountName>;AccountKey=<accountKey>"/>-->
      <Setting name="StorageCredentials"
value="UseDevelopmentStorage=true" />
```

For interacting with Storage you can use several tools – one tool that I like is from the Windows Azure CAT team located here: [http://appfabriccat.com/2011/02/exploring-windows-azure-storage-apis-by-building-a-storage-explorer-application/](http://appfabriccat.com/2011/02/exploring-windows-azure-storage-apis-by-building-a-storage-explorer-application/ "http://appfabriccat.com/2011/02/exploring-windows-azure-storage-apis-by-building-a-storage-explorer-application/")  and shown in the prior picture

At runtime, during role initialization and startup, Azure will call into your RoleEntryPoint.  At that time the code will do a dynamic pull of the 2 archives and extract – using the Sharp Zip Lib <link> as Mario had demonstrated in his sample.  The only different here is the use of CLR code vs. PowerShell (which is really CLR, but that’s another discussion).

At this point, once the 2 zips are extracted, the Role’s file system looks as follows:

Worker Role approot

[![3-3-2011 6-17-12 PM](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/0576.3-3-2011-6-17-12-PM_thumb_16253230.png "3-3-2011 6-17-12 PM")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/3730.3-3-2011-6-17-12-PM_02E47B91.png)

From there, the OnStart method (which also does the download and unzip using a simple StorageHelper class) kicks off the Java path and now you have Java!

Task Manager

[![3-3-2011 6-16-10 PM](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/2727.3-3-2011-6-16-10-PM_thumb_05C9BA77.png "3-3-2011 6-16-10 PM")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/0160.3-3-2011-6-16-10-PM_20765690.png)

Jetty Sample Page

[![3-3-2011 6-58-49 PM](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/5466.3-3-2011-6-58-49-PM_thumb_103A68CA.png "3-3-2011 6-58-49 PM")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/2555.3-3-2011-6-58-49-PM_3CC398B0.png)

A couple of things I’m working on to enhance this is to extract the jre and jetty bits not to the appRoot but to a resource location defined as part of the service definition.

ServiceDefinition.csdef

```
<?xml version="1.0" encoding="utf-8"?>
<ServiceDefinition name="HostedJetty" xmlns="http://schemas.microsoft.com/ServiceHosting/2008/10/ServiceDefinition">
  <WorkerRole name="JettyWorker">
<Imports>
  <Import moduleName="Diagnostics" />
  <Import moduleName="RemoteAccess" />
  <Import moduleName="RemoteForwarder" />
</Imports>
<Endpoints>
  <InputEndpoint name="JettyPort" protocol="tcp" port="80" localPort="8080" />
</Endpoints>
<LocalResources>
  <LocalStorage name="Archives" cleanOnRoleRecycle="false" sizeInMB="100" />
</LocalResources>
```

As the concept matures a bit, being able to update dynamically the content or jar files as part of a running java solution is something that is possible through continued enhancement of this simple model.

The Visual Studio 2010 Solution is located here:

[HostingJavaSln\_NDA.zip](http://cicoria.com/downloads/waz/HostingJavaSln_NDA.zip "http://cicoria.com/downloads/waz/HostingJavaSln_NDA.zip")
