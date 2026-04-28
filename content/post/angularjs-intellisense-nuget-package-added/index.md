---
title: "AngularJS intellisense NuGet package added"
date: 2015-02-27T09:09:33+0000
lastmod: 2015-02-27T09:09:33+0000
slug: "angularjs-intellisense-nuget-package-added"
aliases:
  - /angularjs-intellisense-nuget-package-added/
---

Using the work of [John Bledsoe](https://twitter.com/jmbledsoe), a [NuGet](http://nuget.org) package has been added that takes a dependency on [AngularJS.Core](https://www.nuget.org/packages/AngularJS.Core/) – and provides the [angular.intellisense.js](https://raw.githubusercontent.com/jmbledsoe/angularjs-visualstudio-intellisense/master/src/Scripts/angular.intellisense.js) file to your project.

Via Nuget.org: [https://www.nuget.org/packages/AngularJS.Intellisense/](https://www.nuget.org/packages/AngularJS.Intellisense/ "https://www.nuget.org/packages/AngularJS.Intellisense/")

Referenced here: [http://blogs.msdn.com/b/visualstudio/archive/2015/02/05/using-angularjs-in-visual-studio-2013.aspx](http://blogs.msdn.com/b/visualstudio/archive/2015/02/05/using-angularjs-in-visual-studio-2013.aspx "http://blogs.msdn.com/b/visualstudio/archive/2015/02/05/using-angularjs-in-visual-studio-2013.aspx")

This approach takes the ‘per’ project approach and puts this into the /scripts directory of your project.

### \_references.js – auto-update

In addition, the package delivers a default \_references.js file that allows for auto-update. If you want to at any time regernated the references, in Visual Studio open \_references.js and then choose “Update JavaScript References”.

```
/// <autosync enabled="true" />
/// <reference path="angular.js" />
/// <reference path="angular-mocks.js" />
/// <reference path="project.js" />

```

The source for the intellisense is here:

[https://github.com/jmbledsoe/angularjs-visualstudio-intellisense](https://github.com/jmbledsoe/angularjs-visualstudio-intellisense "https://github.com/jmbledsoe/angularjs-visualstudio-intellisense")

Thanks to Jim Bledsoe for his hard work on this…  [https://twitter.com/jmbledsoe](https://twitter.com/jmbledsoe "https://twitter.com/jmbledsoe")
