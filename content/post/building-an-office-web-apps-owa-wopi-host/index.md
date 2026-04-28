---
title: "Building an Office Web Apps (OWA) WOPI Host"
date: 2013-07-22T12:21:37+0000
lastmod: 2013-07-22T12:21:37+0000
slug: "building-an-office-web-apps-owa-wopi-host"
aliases:
  - /building-an-office-web-apps-owa-wopi-host/
---

**UPDATE: January 31, 2014**

**The solution and project have been updated to MVC5, and Web API 2.  In addition, editing PowerPoint (PPTX), and Excel files has been added.  Word Editing is not part of the solution. Also, PDF viewing is enabled.  See the updated post here:**

[http://blogs.msdn.com/b/scicoria/archive/2014/01/31/wopi-host-sample-has-been-updated.aspx](http://blogs.msdn.com/b/scicoria/archive/2014/01/31/wopi-host-sample-has-been-updated.aspx "http://blogs.msdn.com/b/scicoria/archive/2014/01/31/wopi-host-sample-has-been-updated.aspx")

//end

The latest version of OWA in an on-premises deployment decouples the dependency on SharePoint. For those organizations that perhaps have invested somewhat in non-SharePoint content or document management systems, this offers an opportunity to provide the OWA experience with content from your site.

[Get the solution zip](https://www.cicoria.com/downloads/wopi/CL-OwaWopiNetFx4520130722.zip)

## WOPI Host

The WOPI host protocol is defined at this location: <http://msdn.microsoft.com/en-us/library/hh643135(v=office.12).aspx>

There’s a great overview, introducing WOPI in a blog post from the Office development team here: <http://blogs.msdn.com/b/officedevdocs/archive/2013/03/21/introducing-wopi.aspx>

In addition, a good overview of the architecture in 2013 (vs. 2010) is shown here:

<http://technet.microsoft.com/en-us/library/jj219437.aspx>

## Callback interface

Note that a WOPI host has to respond to a direct call from OWA for the content. That is illustrated in the above post with this sequence diagram:

[![image](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/2538.image_thumb_1175A3B1.png "image")](https://msdnshared.blob.core.windows.net/media/MSDNBlogsFS/prod.evol.blogs.msdn.com/CommunityServer.Blogs.Components.WeblogFiles/00/00/00/99/56/metablogapi/8867.image_047BC3A0.png)

## Building WOPI Host

So, for this post, we’re going to cover a working WOPI host that will utilize OWA for display content (Word, Excel, and PowerPoint) with an OWA on-premises deployment.

## Primary Interfaces

To get started, the bare minimum implementation, for viewing, requires 2 interfaces implemented as REST endpoints on your WOPI Host.

The solution contains a series of API controllers. The FilesController implements the 2 prmiamry interfaces – the first is a GET which returns the file information; the second returns the content as a stream.

#### Files

|  |  |
| --- | --- |
| **API** | **Description** |
| [GET api/wopi/files/{name}?access\_token={access\_token}](http://localhost:55574/Help/Api/GET-api-wopi-files-name_access_token) | Required for WOPI interface - on initial view |
| [GET api/wopi/files/{name}/contents?access\_token={access\_token}](http://localhost:55574/Help/Api/GET-api-wopi-files-name-contents_access_token) | Required for View WOPI interface - returns stream of document. |

## Discovery XML

Within the ~/App\_Data location, there’s a discovery.xml file. This is retrieved using the following URL from the OWA server. That XML just needs to be saved to the location.

<http://owa1.wingtip.com/hosting/discovery>

The solution builds the proper full URL based upon the file type, by examining this file.

## Uploading Files / Link Generation

For the sake of testing, you can upload files using the Upload API. This will accept multiple files and return a JSON result that is a collection of Links, with access tokens for each file.

The Link generation is used to generate a fully qualified link that can be used to view an Office file on OWA which will be consumed from the WOPI host.

## Access Token

OWA supports the WOPI host use of an access token. Note that the sample provides a HMACSHA256 of the file name using a random generated salt value.

## Deployment

Note that the WOPI host MUST be HTTP addressable from the OWA server. In this sample, you also have to turn off HTTPS. Check the OWA TechNet articles on how.

## Source Code:

The solution file is here…

### Here’s the GetInfo portion

```
        var fileInfo = _fileHelper.GetFileInfo(name);
        return fileInfo;
    }

```

### And the Contents portion

```
     rv.Content = new StreamContent(stream);
     rv.Content.Headers.ContentType = new MediaTypeHeaderValue(&quot;application/octet-stream&quot;);
     return rv;

 }
 catch (Exception ex)
 {
     var rv = new HttpResponseMessage(HttpStatusCode.InternalServerError);
     var stream = new MemoryStream(UTF8Encoding.Default.GetBytes(ex.Message ?? &quot;&quot;));
     rv.Content = new StreamContent(stream);
     return rv;
 }

```

### And, KeyGen – which generates the hash values

```
    bool Validate(string name, string access_token);
}
public class KeyGen : IKeyGen
{
    byte[] _key;
    int _saltLength = 8;

    static RNGCryptoServiceProvider s_rngCsp = new RNGCryptoServiceProvider();

    public KeyGen()
    {
        var key = WebConfigurationManager.AppSettings[&quot;appHmacKey&quot;];
        if (string.IsNullOrEmpty(key))
            throw new ArgumentNullException(&quot;must supply a HmacKey - check config&quot;);
        _key = Encoding.UTF8.GetBytes(key);
    }

    public string GetHash(string value)
    {
        byte[] salt = new byte[_saltLength];
        s_rngCsp.GetBytes(salt);

        var saltStr = Convert.ToBase64String(salt);
        return GetHash(value, saltStr);
    }

    private string GetHash(string value, string saltStr)
    {
        //Not really secure; must use random salt to ensure non-repeat....
        HMACSHA256 hmac = new HMACSHA256(_key);
        var hash = hmac.ComputeHash(Encoding.UTF8.GetBytes(saltStr + value));
        var rv = Convert.ToBase64String(hash);
        return saltStr + rv;
    }

    public bool Validate(string name, string access_token)
    {
        var targetHash = GetHash(name, access_token.Substring(0,_saltLength + 4));  //hack for base64 form
        return String.Equals(access_token, targetHash);
    }

}

```

### File Helper

```
    using (FileStream stream = File.OpenRead(fileName))
    using (var sha = SHA256.Create())
    {
        byte[] checksum = sha.ComputeHash(stream);
        sha256 = Convert.ToBase64String(checksum);
    }

    var rv = new CheckFileInfo
    {
        BaseFileName = info.Name,
        OwnerId = &quot;admin&quot;,
        Size = info.Length,
        SHA256 = sha256,
        Version = info.LastWriteTimeUtc.ToString(&quot;s&quot;)
    };

    return rv;
}

internal string GetFileName(string name)
{
    var file = HostingEnvironment.MapPath(&quot;~/App_Data/&quot; + name);
    return file;
}

```

### Finally, for this Post a WOPI helper class

```
public WopiAppHelper(string discoveryXml)
{
    _discoveryFile = discoveryXml;

    using (StreamReader file = new StreamReader(discoveryXml))
    {
        XmlSerializer reader = new XmlSerializer(typeof(WopiHost.wopidiscovery));
        var wopiDiscovery = reader.Deserialize(file) as WopiHost.wopidiscovery;
        _wopiDiscovery = wopiDiscovery;
    }
}

public WopiHost.wopidiscoveryNetzoneApp GetZone(string AppName)
{
    var rv = _wopiDiscovery.netzone.app.Where(c =&gt; c.name == AppName).FirstOrDefault();
    return rv;
}

public string  GetDocumentLink(string wopiHostandFile)
{
    var fileName = wopiHostandFile.Substring(wopiHostandFile.LastIndexOf('/') + 1);
    var accessToken = GetToken(fileName);
    var fileExt = fileName.Substring(fileName.LastIndexOf('.') + 1);
    var tt = _wopiDiscovery.netzone.app.AsEnumerable().Where(c =&gt; c.action.Where(d =&gt; d.ext == fileExt).Count() &gt; 0);

    var appName = tt.FirstOrDefault();

    if (null == appName) throw new ArgumentException(&quot;invalid file extension &quot; + fileExt);

    var rv = GetDocumentLink(appName.name, fileExt, wopiHostandFile, accessToken);

    return rv;
}

string GetToken(string fileName)
{
    KeyGen keyGen = new KeyGen();
    var rv = keyGen.GetHash(fileName);

    return HttpUtility.UrlEncode(rv);
}

const string s_WopiHostFormat = &quot;{0}?WOPISrc={1}&amp;access_token={2}&quot;;
public string GetDocumentLink(string appName, string fileExtension, string wopiHostAndFile, string accessToken)
{
    var wopiHostUrlsafe = HttpUtility.UrlEncode(wopiHostAndFile.Replace(&quot; &quot;, &quot;%20&quot;));
    var appStuff = _wopiDiscovery.netzone.app.Where(c =&gt; c.name == appName).FirstOrDefault();

    if (null == appStuff)
        throw new ApplicationException(&quot;Can't locate App: &quot; + appName);

    var appAction = appStuff.action.Where(c =&gt; c.ext == fileExtension).FirstOrDefault();
                if (null == appAction)
        throw new ApplicationException(&quot;Can't locate UrlSrc for : &quot; + appName);

    var endPoint = appAction.urlsrc.IndexOf('?');
    var fullPath = string.Format(s_WopiHostFormat, appAction.urlsrc.Substring(0, endPoint), wopiHostUrlsafe, accessToken); 

    return fullPath;
}

```
