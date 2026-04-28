---
title: "Deployment of Theme and Resource files via Feature / Timer Jobs"
date: 2010-01-31T05:33:01+0000
lastmod: 2010-01-31T05:33:01+0000
slug: "deployment-of-theme-and-resource-files-via-feature-timer-jobs"
aliases:
  - /deployment-of-theme-and-resource-files-via-feature-timer-jobs/
---

Recently, we had a deployment scenario where we needed to deploy a custom theme and some resource files (resx) to the Farm and the Web Application zones respectively.

### Theme Deployment via Feature / Timer Job

For the first feature, deployment of a theme, we initially went down the path assuming that we could scope the feature at Farm, and SharePoint would call the FeatureInstalled method in our Feature Receiver. Unfortunately, this all worked in development on our single machine environments. When it came time to deploy to a multi-server SharePoint environment we found that the FeatureInstalled event NEVER fired on all machines; however, the FeatureDeactivating and FeatureUninstalling fired every time when we de-activated/retracted the solution respectively. Even the FeatureActivated didn’t fire on all machines.

While I’ve been told and seen many instances on blogs and internal messages that FeatureInstalled should be firing on all the machines, I just never saw it happen (I had added lots of logging and saw nothing in the ULS logs) – this was tried on a couple of Farms.

So, in comes the timer job. The more I picked apart how jobs are created in the SharePoint timer jobs, the more it was evident that was the only solution that would be reliable and this issue could be put to bed.

So, the feature definition is scoped to Farm, and pointing to a simple Feature Receiver that on Activation:

```
<?xml version="1.0" encoding="utf-8" ?>
<Feature xmlns="http://schemas.microsoft.com/sharepoint/"
         Id="604C0C13-D59B-4cd4-BCD2-A90F8AF2266C"
         SolutionId="db6b8735-a4a0-47dc-a012-64e85373f150"
         Title="Theme to deploy"
         Description="Provides deployment of Theme to the Farm"
         Hidden="FALSE"
         ActivateOnDefault="FALSE"
         Scope="Farm"
         ReceiverAssembly="..."
         ReceiverClass ="...."
         Version="1.0.0.0">

<Properties>  

<Property Key="TemplateId" Value="THEMESAMPLE" />  

<Property Key="DisplayName" Value="Theme Sample"/>  

<Property Key="Description" Value="Theme Sample"/>  

<Property Key="Thumbnail" Value="images/thwheat.gif"/>  

<Property Key="Preview" Value="images/thwheat.gif"/>  

</Properties>  

</Feature>

```

The FeatureActivated method just creates a custom type that contains the properties, then makes a call into the custom timer job’s static method to CreateJob, which is as follow:

```
/// <summary>
/// Call this to create the job - set the properties as required
/// If you want to delete (remove) the theme setting from the SPTHEMES.xml file pass in 
/// delete == true and the TemplateID
/// </summary>
/// <param name="jobProperties"></param>
public static void CreateJob(ThemeDeploymentJobProperties jobProperties)
{
    LogHelper.Log("creating job {0}", JOBNAME);
    SPWebService wsvc = SPFarm.Local.Services.GetValue<SPWebService>();

    foreach (SPServer server in SPFarm.Local.Servers)
    {
        switch (server.Role)
        {
            case SPServerRole.Application:
            case SPServerRole.SingleServer:
            case SPServerRole.WebFrontEnd:
                LogHelper.Log("submitting job {0} for server {1}", JOBNAME, server.Name);
                ThemeDeploymentJob job = new ThemeDeploymentJob(wsvc, jobProperties);
                job.SubmitJobNow(JOBNAME);
                break;
            default:
                break;
        }
    }
    LogHelper.Log("done creating job {0}", JOBNAME);
}
```

The key to the above is getting the Web Service (which is present on any machine that has the Web Front End role) and use that in the base type for SPJobDefinition’s constructor, as shown below.  Also, submitting the job for each server – this actually assumes that the service is present on all machines in the farm, and generally that’s what / how I configure a Farm and recommend that approach.

```
public ThemeDeploymentJob() : base() { }

public ThemeDeploymentJob(SPWebService webService, ThemeDeploymentJobProperties properties)
    : base(JOBNAME, webService, null, SPJobLockType.None)
{
    SetProperties(properties);
}
```

The rest of the code, and and much inspiration comes from the following samples, etc..

[http://solutionizing.net/2008/07/09/updating-spthemesxml-through-a-feature/](http://solutionizing.net/2008/07/09/updating-spthemesxml-through-a-feature/ "http://solutionizing.net/2008/07/09/updating-spthemesxml-through-a-feature/")

[http://www.devexpertise.com/2009/02/11/installing-a-theme-as-a-sharepoint-feature/](http://www.devexpertise.com/2009/02/11/installing-a-theme-as-a-sharepoint-feature/ "http://www.devexpertise.com/2009/02/11/installing-a-theme-as-a-sharepoint-feature/")

[http://alonsorobles.com/2008/06/26/packaging-branding-and-themes-for-deployment-in-sharepoint-environments/](http://alonsorobles.com/2008/06/26/packaging-branding-and-themes-for-deployment-in-sharepoint-environments/ "http://alonsorobles.com/2008/06/26/packaging-branding-and-themes-for-deployment-in-sharepoint-environments/")

Next post – Resource File Deployment (Resx) to the App\_GlobalResources path…\

Thanks to Joe McPeak, Ketan Shah for feedback, discussions…

Full source to Timer Jobs and WinForm application for job submission here:

[SharePointTimerJobSlnV3.zip](www.cicoria.com/downloads/SharePointTimerJobSlnV3.zip)
