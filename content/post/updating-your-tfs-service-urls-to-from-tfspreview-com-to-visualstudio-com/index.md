---
title: "Updating your TFS Service urls to from TfsPreview.com to VisualStudio.com"
date: 2012-11-03T01:12:42+0000
lastmod: 2012-11-03T01:12:42+0000
slug: "updating-your-tfs-service-urls-to-from-tfspreview-com-to-visualstudio-com"
aliases:
  - /updating-your-tfs-service-urls-to-from-tfspreview-com-to-visualstudio-com/
---

If you haven’t heard, TFS Service has gone live at <http://tfs.visualstudio.com/>.

While the old DNS name works, at some point it may retire.

So, [Jesse Houwing](http://blogs.msdn.com/b/willy-peter_schaub/archive/2012/07/03/introducing-the-visual-studio-alm-rangers-jesse-houwing.aspx) has a post/script that makes it easy.

<http://blog.jessehouwing.nl/2012/11/updating-your-team-foundation-service.html>

Here’s the script as well.

```

Get-ItemProperty -Path HKCU:\Software\Microsoft\VisualStudio\*\TeamFoundation\Instances\*.tfspreview.com Uri | %{set-itemproperty -Path $_.PSPath Uri -Value ( $_.Uri -Replace ".tfspreview.com/", ".visualstudio.com/" )}   Get-ItemProperty -Path HKCU:\Software\Microsoft\VisualStudio\*\TeamFoundation\Instances\*.tfspreview.com\Collections\* Uri | %{set-itemproperty -Path $_.PSPath Uri -Value ( $_.Uri -Replace ".tfspreview.com/", ".visualstudio.com/" )}   Get-ChildItem -Path HKCU:\Software\Microsoft\VisualStudio\*\TeamFoundation\Instances\*.tfspreview.com | Rename-Item -NewName { $_.PSChildName -Replace ".tfspreview.com$", ".visualstudio.com" }
```
