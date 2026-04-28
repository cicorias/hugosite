---
title: "Welcomed updates to VSeWSS – now x64 support"
date: 2009-01-13T03:17:26+0000
lastmod: 2009-01-13T03:17:26+0000
slug: "welcomed-updates-to-vsewss-now-x64-support"
aliases:
  - /welcomed-updates-to-vsewss-now-x64-support/
---

If you’ve been running x64 WSS/MOSS in development VSeWSS has been a challenge (wouldn’t install – albeit I believe the Bamboo solutions folks had some hack…)

Now, the CTP of VSeWSS 1.3 has been announced

[SharePoint Team Blog](http://blogs.msdn.com/sharepoint/default.aspx)

[CTP Preview of VSeWSS](http://blogs.msdn.com/sharepoint/archive/2009/01/12/announcing-community-technology-preview-of-visual-studio-2008-extensions-for-sharepoint-v1-3.aspx)

Key capabilities in 1.3

- The extensions now install on x64 bit OS. Visual Studio 2008 and SharePoint must be already installed.
- Command Line Build option for TFS and MSBuild integration
- Separate WSP Package and Retract commands. You can now build the WSP without deploying it
- SPSolGen to Support Exporting from Content Management Publishing Sites
- New Item Template for RootFiles Deployment
- Automatically Remove conflicting existing features on development SharePoint server
- WSP View New Feature Dialog Improvements: scope, receiver checkbox, element checkbox
- WSP View can now be used to merge features and it blocks site features being merged into web features
- Allow adding separate binary files such as Workflow assemblies
- Some refactoring allowing for Web Part renaming and removing lines from feature.xml Item Removed
- Allow selection of GAC or BIN deployment for Web Part Project not including CAS generation
- Increase visibility of hidden features that VSeWSS creates
- Add fast update deploy for DLL only or file only changes to solutions
- Numerous Bug Fixes and improvements to error messages
