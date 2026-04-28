---
title: "Office Web Apps–WOPI Host and url paths"
date: 2013-06-24T10:37:45+0000
lastmod: 2013-06-24T10:37:45+0000
slug: "office-web-appswopi-host-and-url-paths"
aliases:
  - /office-web-appswopi-host-and-url-paths/
---

If you’re following along with the post on creating a WOPI host, it’s never fully apparent that you MUST adhere to the path shown in the article here:

<http://blogs.msdn.com/b/officedevdocs/archive/2013/03/20/introducing-wopi.aspx>

That is, the path to your host must contain ‘/wopi/files’.  It wasn’t clear to me in that article, nor could I find it in the WOPI spec. <http://msdn.microsoft.com/en-us/library/hh622722(v=office.12).aspx>

So, for example, here are some Routes I used in MVC

```
        config.Routes.MapHttpRoute(
            name: "FileInfo",
            routeTemplate: "api/wopi/files/{name}",
            defaults: new { controller = "Files", action = "Get" }
            );

```

Here are the Actions

```
    IFileHelper _fileHelper;
    public FilesController() : this(new FileHelper())
    {

    }

    public FilesController(IFileHelper fileHelper)
    {
        _fileHelper = fileHelper;
    }

    /// &lt;summary&gt;
    /// Required for WOPI interface - on initial view
    /// &lt;/summary&gt;
    /// &lt;param name="name"&gt;&lt;/param&gt;
    /// &lt;param name="access_token"&gt;&lt;/param&gt;
    /// &lt;returns&gt;&lt;/returns&gt;
    public CheckFileInfo Get(string name, string access_token)
    {
        var fileInfo = _fileHelper.GetFileInfo(name);
        return fileInfo;
    }

    /// &lt;summary&gt;
    /// Required for View WOPI interface - returns stream of document.
    /// &lt;/summary&gt;
    /// &lt;param name="name"&gt;&lt;/param&gt;
    /// &lt;param name="access_token"&gt;&lt;/param&gt;
    /// &lt;returns&gt;&lt;/returns&gt;
    public HttpResponseMessage GetFile(string name, string access_token)
    {
        try
        {
            var file = HostingEnvironment.MapPath("~/App_Data/" + name);
            var rv = new HttpResponseMessage(HttpStatusCode.OK);
            var stream = new FileStream(file, FileMode.Open, FileAccess.Read);

            rv.Content = new StreamContent(stream);
            rv.Content.Headers.ContentType = new MediaTypeHeaderValue("application/octet-stream");
            return rv;

        }
        catch (Exception ex)
        {
            var rv = new HttpResponseMessage(HttpStatusCode.InternalServerError);
            var stream = new MemoryStream(UTF8Encoding.Default.GetBytes(ex.Message ?? ""));
            rv.Content = new StreamContent(stream);
            return rv;
        }
    }

}</pre></div>

```
