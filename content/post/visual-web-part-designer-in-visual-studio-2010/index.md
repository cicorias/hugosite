---
title: "Visual Web Part Designer in Visual Studio 2010"
date: 2009-10-03T02:28:35+0000
lastmod: 2009-10-03T02:28:35+0000
slug: "visual-web-part-designer-in-visual-studio-2010"
aliases:
  - /visual-web-part-designer-in-visual-studio-2010/
---

In the October edition of MSDN Magazine, there’s a great article that does a quick rundown of building a component that can be surfaced as a Web Part via the Gallery and placed in Web Part zones on pages.

The article by Steve Fox is here: [Steve Fox - Visual Studio 2010 Tools for SharePoint Development – MSDN Magazine October 2009](http://msdn.microsoft.com/en-us/magazine/ee309510.aspx)

There’s a couple very important aspect that might not be 100% clear from the title – 1st, you’re really visually designing a User Control (ASCX).  So, this is really just a “visual user control designer and web part cookbook combination deployment helper”…

And 2nd– this all works today, you just don’t get the magical build of the CAML based manifests, feature.xml, DDF, etc. to rapidly get into the “code –> build –> debug –> test –> code” cycles needed to increase the velocity of development.  Well, actually you can – with a couple of 3rd party tools.

I’m not saying this isn’t a good thing – having VS2010 provide this capability.  In fact, what they are providing is industrialization of development patterns into a model that provided directly in the VS 2010 environment that was “cobbled” together either through the [VseWss](http://www.microsoft.com/downloads/details.aspx?familyid=FB9D4B85-DA2A-432E-91FB-D505199C49F6&displaylang=en) extensions or tools such as [WSP Builder](http://www.codeplex.com/wspbuilder).

#### User Controls

Now, why are User Controls potentially a concern.  In one word “versioning”.  Since, even in the example, most user controls are deployed to the farm into the “12” or “Root” hive of SharePoint – they are Farm based artifacts – in that you get 1 and only 1 of these “ASCX” files to be reused wherever they are statically referenced.

That doesn’t give you true “Side-by-Side” (SxS) installation – which we can get with an Assembly that packages our Server control or Web Part Server control into a strong named that we can explicitly reference at runtime.

That means if you have 2 Web Apps, Sites, whatever, that want to use distinct versions, you have to provide a way to have basically 2 complete “sets” of all these artifacts and using the way the example code was presented, you’d have to come up with a way to put a version name in the “filename”.

So, how would you change the ASCX portion of the component for site #2 and redeploy?  Well, one way is to change the following – which is in your truly compiled class that probably made it into the GAC:  You can change a couple of things – 1st, the name of the ASCX file:

```
private const string _ascxPath =
@"~/CONTROLTEMPLATES/SampleWebPartProject/ProductInfo/" +
@"ProductInfoUserControl.ascx";
```

If you change the name of the ASCX file, well, that didn’t buy you much.  Because, all instances across the Farm will still use this.

#### Option 1

Another way is to change the prefix of the path “~/CONTROLTEMPLATES/” – to something unique.  For that one, in the past I’ve simply use IIS virtual path mapping to a specific feature folder that contains the version name in the folder.  So, for example:

**Site1: “~/\_MYCONTROLS”  is mapped to   “..\12\TEMPLATE\FEATURE\ControlsV1”**

**Site2: “~/\_MYCONTROLS”  is mapped to   “..\12\TEMPLATE\FEATURE\ControlsV2”**

The only difference being that it’s physically mapped to a different location (physical directory) – so at runtime it picks up the mapped version through IIS virtual directory magic.

This can be automated, creation of process through AppCmd as follows: (I've left out the full 12\14 hive path).

```
AppCmd.exe ADD vdir /app.name:"LitwareInc/" /path:/_MYCONTROLS /physicalPath:c:\...\FEATURE\ControlsV2
```

So, what’ve got now is a single assembly, the true “web part server control” instantiating the version you really need. All for just a little bit more on the configuration side.

#### Option 2

An option that I’d like the template to automatically provide is to externalize the control name (ASCX) file to use at Web Part configuration time through the use of a property on the web part.  This could then be managed through the Web Part property editors that we get for free in SharePoint.

This way at Page or Web Part configuration time, you either explicitly set this property or you provide some default in the code.  So, a property like the following would surface in the property editor allowing an “administrator”.

So, this is what I’ve done in the past that works:  In the web part define a configurable property as follows:

```
[WebBrowsable]
[WebDisplayName("Control File Name")]
[WebDescription("Name of the ASCX file in the feature folder")]
[Category("Custom")]
[Personalizable(PersonalizationScope.Shared)]
public string ControlFileName {
    get;
    set;
}
```

Then change the code in the Web Part class to the following (in fact, this is where you can now have a “universal” User Control loader and just one way to wrap these User Controls from a single GAC deployed Web Part shell

```
protected override void CreateChildControls()
{
string ctrlPath= @"~/_MYCONTROLS/" + this.ControlFileName;  //maybe validate this - er, does it end in ASCX?
Control control = this.Page.LoadControl(ctrlPath);
Controls.Add(control);
base.CreateChildControls();
}
```

del.icio.us Tags: [SharePoint](http://del.icio.us/popular/SharePoint),[Development](http://del.icio.us/popular/Development),[Visual Studio](http://del.icio.us/popular/Visual+Studio)
