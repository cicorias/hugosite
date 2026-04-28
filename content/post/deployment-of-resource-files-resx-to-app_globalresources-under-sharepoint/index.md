---
title: "Deployment of Resource files (*.resx) to App_GlobalResources under SharePoint"
date: 2010-01-31T05:45:43+0000
lastmod: 2010-01-31T05:45:43+0000
slug: "deployment-of-resource-files-resx-to-app_globalresources-under-sharepoint"
aliases:
  - /deployment-of-resource-files-resx-to-app_globalresources-under-sharepoint/
---

This is a continuation from

[Deployment of Theme and Resource files](http://cicoria.com/CS1/blogs/cedarlogic/archive/2010/01/31/deployment-of-theme-and-resource-files-via-feature-timer-jobs.aspx)

Resource File Deployment (Resx)

The second item was deploying Resource files to the App\_GlobalResource directory present as a subdirectory under each IIS site for each SharePoint Web Application zone. Remember that you can have multiple IIS Sites for each “Logical” SharePoint Web Application.

The other requirement we had was that each Web Application needed to have its own set of resource files and were to be deployed and scoped as a Web Application feature.

The way the Timer job for resource was written was it would take a list of full file paths along with the target Web Application.  So, it’s the responsibility of the Feature code when it’s calling the CreateJob method to get that list of files, populate the string[] of files, and also obtain the target Web Application instance on the call.  All of these things are done in the feature activation code – which, I’ve left out of this sample just for brevity.

The CreateJob method as mentioned is below:

```
/// <summary>
/// Submit a App_GlobalResources copy job providing a list of files with full path
/// </summary>
/// <param name="webApp"></param>
/// <param name="files"></param>
public static void CreateJob(SPWebApplication webApp, string[] files)
{
    try
    {
        // Create new job
        GlobalResourceDeployJob grdj = new GlobalResourceDeployJob(webApp, files);
        grdj.SubmitJobNow(JOBNAME);
    }
    catch (Exception ex)
    {
        LogHelper.Log("Failed to create job {0} - {1}", JOBNAME, ex.Message);
        throw;
    }
}
```

Pretty straight forward, and the constructor is as follows:

```
/// <summary>
/// Here as it's required by the platform
/// </summary>
public GlobalResourceDeployJob() : base() { }

/// <summary>
/// Primary constructor used
/// </summary>
/// <param name="webApp"></param>
/// <param name="files"></param>
public GlobalResourceDeployJob(SPWebApplication webApp, string[] files)
    : base(JOBNAME, webApp, null, SPJobLockType.None)
{
    _files = files;
}
```

Again, no big deal..

The Execute override does most of the work as follows:

```
/// <summary>
/// Main method to actualy do the copy of the files
/// </summary>
/// <param name="targetInstanceId"></param>
public override void Execute(Guid targetInstanceId)
{
    try
    {
        this.Log("starting job {0}", JOBNAME);
        SPWebApplication webApp = this.Parent as SPWebApplication;

        if (webApp == null)
        {
            this.Log("job {0} - invalide WebApp found (isNull)", JOBNAME);

        }
        foreach (SPUrlZone zone in webApp.IisSettings.Keys)
        {
            // The settings of the IIS application to update
            SPIisSettings oSettings = webApp.IisSettings[zone];

            // Determine the destination path
            string destPath = Path.Combine(oSettings.Path.ToString(), "App_GlobalResources");

            foreach (var filePath in _files)
            {
                string fileName = Path.GetFileName(filePath);
                if (File.Exists(filePath))
                    this.Log("File {0} exists - will be overwriting", fileName);

                if ( !File.Exists(filePath ))
                {
                    this.Log("File {0} to copy doesn't exist at the source - skipping", filePath);
                    continue;
                }

                string destination = Path.Combine(destPath, fileName);
                this.Log("Copying filePath {0} to  {1}", filePath, destination);
                try
                {
                    File.Copy(filePath, destination, true);
                }
                catch (Exception ex)
                {
                    this.Log("Err - couldn't copy file {0} with exception {1}", filePath, ex.Message);
                }
            }

            this.Log("job {0} - For WebApp {1}: zone path: {2}", JOBNAME, webApp.Name, oSettings.Path); 
        }

        this.Log("ending job {0}", JOBNAME);
    }
    catch (Exception ex)
    {
        this.Log("Failed Job {0}  : {1}", JOBNAME, ex.Message);
        throw;
    }
}
```

An finally, to make life a little easier, A couple of extension methods that i use:

```
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Microsoft.SharePoint.Administration;
using Microsoft.SharePoint;

namespace SharePointJobs
{
    public static class TimerJobExtensions
    {
        public static void SubmitJobNow(this SPJobDefinition jobDef, string jobName)
        {
            if (jobDef.Farm.TimerService.Instances.Count < 1)
            {
                jobDef.Log("Could not find TimerService on this box");
                throw new SPException("Could not run job. Timer service not found.");
            }

            foreach (SPJobDefinition job in  jobDef.Service.JobDefinitions)
                if (job.Name == jobName)
                {
                    jobDef.Log("Found existing job {0}- deleteing", jobName);
                    job.Delete();
                    jobDef.Log("Done deleting existing job {0}", jobName);
                }

            jobDef.Log("Scheduling job {0}", jobName);
            jobDef.Schedule = new SPOneTimeSchedule(DateTime.Now);
            jobDef.Update();

        }

        public static void Log(this SPJobDefinition jobDef, string message)
        {
            LogHelper.Log(jobDef.Name + ":" + message);
        }

        public static void Log(this SPJobDefinition jobDef, string message, params object[] args)
        {
            LogHelper.Log(jobDef.Name + ":" + message, args);
        }
    }

    
}
```

Again, the source for the sample is below, it just contains the Timer Jobs, no feature code (it’s simple to wire it up) and a WinForm app for submitting the jobs.

[SharePointTimerJobSlnV3.zip](https://www.cicoria.com/downloads/SharePointTimerJobSlnV3.zip)

Enjoy…

Again, thanks to the following:

<http://solutionizing.net/2008/07/09/updating-spthemesxml-through-a-feature/>

<http://www.devexpertise.com/2009/02/11/installing-a-theme-as-a-sharepoint-feature/>

<http://alonsorobles.com/2008/06/26/packaging-branding-and-themes-for-deployment-in-sharepoint-environments/>

Thanks to Joe McPeak, Ketan Shah for feedback, discussions…
