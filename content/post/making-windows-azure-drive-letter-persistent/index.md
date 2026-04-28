---
title: "Making Windows Azure Drive Letter Persistent"
date: 2012-01-19T07:42:31+0000
lastmod: 2012-01-19T07:42:31+0000
slug: "making-windows-azure-drive-letter-persistent"
aliases:
  - /making-windows-azure-drive-letter-persistent/
---

Windows Azure Fieldnote

### Summary

Windows Azure Drives [1] provide a means to represent a file based (disk drive) persistent storage option for the various role types within Windows Azure Compute. Each of the roles within Windows Azure can mount and utilize for persistent storage (that survives reboot, reimaging, and updated deployments, of a role instances).

During the mounting of a VHD as a **CloudDrive**, the managed classes have no means to control the drive letter assignment this directly through the **CloudDrive** managed classes that are provided through the Windows Azure SDK.

### Problem

Many solutions today require the use of standard Windows File IO based access and instead of refactoring solutions to leverage the storage options available in the PaaS part of the Windows Azure platform, solutions deployed to Windows Azure can mount a Virtual Hard Disk (VHD) that is persisted in a storage account inside of a running instance. That Page Blob backed VHD is then represented through Virtual Disk Services and Windows Cloud Drive services to the running instances as a Disk Drive and addressable through File IO using a Drive Letter.

While a persistent drive option is available, the drive letter assignment is determined at runtime during the mounting process. This potentially presents a problem with existing solutions, codebases, libraries that require a setting to be established prior to runtime. For example, an application configuration setting that provides a full path, including the drive letter to a location for read/write access for File IO.

### Solution

The following solution takes advantage of the Virtual Disk Services through the **DiskPart.exe** operating system utility to first identify what the VHD is mounted as and, select that volume, and re-assign the letter to the target drive letter.

The original idea for the approach comes from this blog post here: <http://techyfreak.blogspot.com/2011/02/changing-drive-letter-of-azure-drive.html>

While there is a COM interface available that could be wrapped via an interop layer, the choice was made to initiate a process to take the actions required for remapping the drive letter due to simplicity. Additionally, while there is an existing managed Interop assembly available (**Microsoft.Storage.Vds**) that is an undocumented and unsupported assembly.

The example scenario presented does the following:

1. Leverages a Windows Azure Web Role (could be a Worker Role or VM Role as well)

2. Implements a Windows Console applications that:

> a. Is a Startup task – in elevated mode and background
>
> b. Runs elevated in order to affect Virtual Disk Services
>
> c. At startup:

- Mounts the VHD from Windows Azure Storage
- Detects if target drive letter and re-assigns as needed to target drive letter \*\*

> d. Then Continuously (every 30 seconds)

- i. Checks if drive is mounted on target drive letter
- ii. If not, reassigns drive letter \*\*

**\*\* Drive Letter reassignment is done through a *System.Process* startup object that runs Diskpart.exe with a “select volume” and “assign drive letter” command sequence.**

### Implementation

The sample solution contains the following:

1. Windows Azure Web Role – simple MVC3 application that just lists the mapped **CloudDrives** using the **CloudDrive.GetMountedDrives()** method

2. **CloudDriveManager** class library – helper class that provides the CloudDrive management actions leveraged by the caller (either Console or other code)

3. **CloudDriveManagerConsole** – Windows console application intended to be a startup project and running in elevated mode in order to affect the assigned driver letter

4. **CloudDriveManagerRole** – implementation of **Microsoft.WindowsAzure.ServiceRuntime.RoleEntryPoint** – which allows this class to be used from within a Windows Azure Web or Worker role – however, that role entry point would need to be elevated (via the “**Runtime**” and “**NetFxEntryPoint**” Elements)

5. **Logger** – simple logger class that writes to a Queue for debugging purposes

6. **ResponseViewer** – simple WPF application that reads Queue messages so you can view log messages from your cloud instances – purely for debugging purposes

7. **TestListDrives** – simple Windows console application that lists the mapped **CloudDrives** – usable from within the Role instance by using Remote Desktop and connecting to the instance

#### Instance Initialization

During role startup, Windows Azure will execute the Task defined in the Service definition in background mode and elevated (running as system). Inside of the console application, the implementation of **OnStart** does the following:

```
public override bool OnStart()
{
    try
    {
        Initialize();
        MountAllDrives();
    }
    catch (Exception ex)
    {
        _logger.Log("fail on onstart", ex);
    }
    return true;
}

void MountAllDrives()  

{  

try  

{  

var driveSettings = RoleEnvironment.GetConfigurationSettingValue(DRIVE_SETTINGS);  

string[] settings = driveSettings.Split(':');  

CloudStorageAccount account =CoudStorageAccount.FromConfigurationSetting(STORAGE_ACCOUNT_SETTING);  

string dCacheName = RoleEnvironment.GetConfigurationSettingValue(DCACHE_NAME);  

LocalResource cache = RoleEnvironment.GetLocalResource(dCacheName);  

int cacheSize = cache.MaximumSizeInMegabytes / 2;  

_cloudDriveManager = new CloudDriveManager(account, settings[0], settings[1][0], cache);  

_cloudDriveManager.CreateDrive();  

_cloudDriveManager.Mount();  

}  

catch (Exception ex)  

{  

_logger.Log("fail on mountalldrives", ex);  

throw;  

}  

}

```

Mostly, the startup routine calls into the custom class **CloudDriveManager**, which provides the simple abstraction to the Windows Azure **CloudDrive** managed class.

The custom **CreateDrive** method calls the **CloudDrive** create drive method in a non-destructive manner – and, for this sample, creates the initial VHD in storage if it does not already exist.

Mounting calls the managed classes **CloudDrive.Moun**t along with calling into a custom **VerifyDriveLetter** method.

```
public void Mount()
{
    _logger.Log(string.Format("mounting drive {0}", _vhdName));
    _cloudDrive = _account.CreateCloudDrive(_vhdName);

    var driveLetter = _cloudDrive.Mount(_cacheSize, DriveMountOptions.Force);
    _logger.Log(string.Format("mounted drive letter {0}", driveLetter));

    var remounted = VerifyDriveLetter();
}
```

Within **VerifyDriveLetter** there’s some logic to validate the current state of the mounted drives. And then verification if the mounted drive is the intended drive letter.

```
public bool VerifyDriveLetter()
{
    _logger.Log("verifying drive letter");
    bool rv = false;
    if (RoleEnvironment.IsEmulated)
    {
        _logger.Log("Can't change drive letter in emulator");
        //return;
    }

    try
    {
        DriveInfo d = new DriveInfo(_cloudDrive.LocalPath);
        if (string.IsNullOrEmpty(_cloudDrive.LocalPath))
        {
            _logger.Log("verifydriveLetter: Not Mounted?");
            throw new InvalidOperationException("drive is notmounted");
        }

        if (!char.IsLetter(_cloudDrive.LocalPath[0]))
        {
            _logger.Log("verifiydriveLeter: Not a letter?");
            throw new InvalidOperationException("verifydriveletter - not a letter?");
        }

        if (IsSameDrive())
        {
            _logger.Log("is same drive; no need to diskpart...");
            return true;
        }

        char mountedDriveLetter = CurrentLocalDrive(_vhdName);
        RunDiskPart(_driveLetter, mountedDriveLetter);

        if (!IsSameDrive())
        {
            var msg = "Drive change failed to change";
                   _logger.Log(msg);
                   throw new ApplicationException(msg);
               }
               else
               {
                   Mount();
               }

               _logger.Log("verifydriveletter done!!");
               return rv;

           }
           catch (Exception ex)
           {
               _logger.Log("error verifydriveletter", ex);
               return rv;
           }

       }
```

The **IsSameDrive** method validates if the current mapped drive is indeed the planned drive letter. If not, it will return “false”.

```
bool IsSameDrive()
{
    char targetDrive = _driveLetter.ToString().ToLower()[0];
    char currentDrive = CurrentLocalDrive(_vhdName);

    string msg = string.Format(
        "target drive: {0} - current drive: {1}",
        targetDrive,
        currentDrive);

    _logger.Log(msg);

    if (targetDrive == currentDrive)
    {
        _logger.Log("verifydriveLetter: already same drive");
        return true;
    }
    else
        return false;

}
```

Finally, the **RunDiskPart** method initiates the action of spawning a new process with the dynamically created **DiskPart** script file that selects the existing volume name (by drive letter) and assigns the target drive letter.

```
void RunDiskPart(char destinationDriveLetter, char mountedDriveLetter)
{
    string diskpartFile = Path.Combine(_cache.RootPath, "diskpart.txt");

    if (File.Exists(diskpartFile))
    {
        File.Delete(diskpartFile);
    }

    string cmd = "select volume = " + mountedDriveLetter + "\r\n" + "assign letter = " + destinationDriveLetter;
      File.WriteAllText(diskpartFile, cmd);

      //start the process
      _logger.Log("running diskpart now!!!!");
      _logger.Log("using " + cmd);
      using (Process changeletter = new Process())
      {
          changeletter.StartInfo.Arguments = "/s" + " " + diskpartFile;
          changeletter.StartInfo.FileName = 
     System.Environment.GetEnvironmentVariable("WINDIR") + "\\System32\\diskpart.exe";
        //#if !DEBUG
        changeletter.Start();
        changeletter.WaitForExit();
        //#endif
    }

    File.Delete(diskpartFile);

}
```

### Output and Results

As an example of the interaction and how the drive appears within the running Windows Azure Role, the following screen shots illustrate the results.

#### Program Startup

At program startup the drive is initially mounted by the Console application – immediately the drive is mounted as the F: drive – the startup code verifies if this is the intended drive – as shown below in the logs, it isn’t, so the code initiates the RunDiskPart method setting M: as the mapped drive.

[![image](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/3618.image_thumb_6A1CD651.png "image")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/3125.image_4BB29568.png)

The following shows how a Windows Azure Drive appears after the custom code reassigns the drive letter to the Operating system using Windows Explorer – the drive is selected below.

[![image](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/0181.image_thumb_2E7CC791.png "image")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/7345.image_0887173B.png)

Within the custom MVC3 application, which simply just lists the Mounted Windows Azure drive (which runs in a separate Process non-elevated – the drive appears as a regular Operating System drive – accessible for File IO as required using the intended drive letter.

[![image](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/7433.image_thumb_6576A5CA.png "image")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/3716.image_1193A2BC.png)

#### Forced Letter Change

The following shows what happens if the drive letter is intentionally changed – in this example, I just initiate a **DiskPart** set of commands to assign the mounted drive the letter L:

[![image](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/6036.image_thumb_6359A701.png "image")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/6740.image_0B6C5621.png)

As you can see in the Windows Explorer window the letter now appears as L: for the **WindowsAzureDrive**.

Within approximately 30 seconds (which is the value used in the **Run** method by the custom code) **VerifyDriveLetter** detects it’s not the intended drive and initiates a change.

[![image](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/6740.image_thumb_12C815CE.png "image")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/8883.image_745DD4E4.png)

And the below image shows the drive again, appearing as the M: drive:

[![image](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/1638.image_thumb_3E2C36C8.png "image")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/2046.image_3851932F.png)

### Future Options

Since capabilities in the Windows Azure platform change over time the ability to dictate the specific letter to be used may come available. Until then, this approach, by means of the Windows Azure Drive and Virtual Disk Services abstraction provided by the platform offers a means to accommodate codebase and application logic that is dependent upon predetermined drive letters.

### References

[1] Windows Azure Drives <http://www.windowsazure.com/en-us/develop/net/fundamentals/cloud-storage/#drives>

[2] Virtual Disk Service <http://msdn.microsoft.com/en-us/library/windows/desktop/bb986750(v=vs.85).aspx>

[3] CloudDrive Storage Client <http://msdn.microsoft.com/en-us/library/microsoft.windowsazure.storageclient.clouddrive.aspx>

[4] Diskpart.exe <http://technet.microsoft.com/en-us/library/cc770877(v=WS.10).aspx>

[5] Task element <http://msdn.microsoft.com/en-us/library/windowsazure/gg557552.aspx#Task>

[6] Runtime element <http://msdn.microsoft.com/en-us/library/windowsazure/gg557552.aspx#Runtime>

[7] NetFxEntryPoint element <http://msdn.microsoft.com/en-us/library/windowsazure/gg557552.aspx#NetFxEntryPoint>

[Solution File: MountXDriveSameLetter.zip](http://cicoria.com/downloads/waz/MountXDriveSameLetter.zip "http://cicoria.com/downloads/waz/MountXDriveSameLetter.zip")
