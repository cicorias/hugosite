---
title: "Copying Properties between 2 Different Types…"
date: 2010-03-11T04:26:34+0000
lastmod: 2010-03-11T04:26:34+0000
slug: "copying-properties-between-2-different-types"
aliases:
  - /copying-properties-between-2-different-types/
---

I’m not sure where I had seen some of this base code, but this comes up time & time again on projects.

Here’s a little method that copies all the R/W properties (public) between 2 distinct class definitions:

It’s called as follows:

```
private static void Test1()
{
MyClass obj1 = new MyClass()
{
    Prop1 = "one",
    Prop2 = "two",
    Prop3 = 100
};

MyOtherClass obj2 = null;

obj2 = CopyClass<myclass  , MyOtherClass>(obj1);

Console.WriteLine(obj1);  

Console.WriteLine(obj2);  

}

namespace Space1  

{  

public class MyClass  

{  

public string Prop1 { get; set; }  

public string Prop2 { get; set; }  

public int Prop3 { get; set; }

public override string ToString()  

{  

var rv = string.Format("MyClass: {0} Prop2: {1} Prop3 {2}", Prop1, Prop2, Prop3);  

return rv;  

}  

}  

}

namespace Space2  

{  

public class MyOtherClass  

{  

public string Prop1 { get; set; }  

public string Prop2 { get; set; }  

public int Prop3 { get; set; }

public override string ToString()  

{  

var rv = string.Format("MyOtherClass: {0} Prop2: {1} Prop3 {2}", Prop1, Prop2, Prop3);  

return rv;  

}  

}

```

Source of the method:

```
/// 
/// Provides a Copy of Public fields between 2 distinct classes
/// 
/// Source class name
/// Target class name
/// Instance of type Source
/// An instance of type Target copying all public properties matching name from the Source.
public static T CopyClass<s  , T>(S source) where T : new()
{

    T target = default(T);
    BindingFlags flags = BindingFlags.Public | BindingFlags.Instance;

    if (source == null)
    {
        return (T)target;
    }

    if (target == null) target = new T();

    PropertyInfo[] objProperties = target.GetType().GetProperties(flags);

    foreach (PropertyInfo pi in objProperties)
    {
        string name = pi.Name;
        PropertyInfo sourceProp = source.GetType().GetProperty(name, flags);

        if (sourceProp == null)
        {
            throw new ApplicationException(string.Format("CopyClass - object type {0} & {1} mismatch in property:{2}", source.GetType(), target.GetType(), name));
        }
        if (pi.CanWrite && sourceProp.CanRead)
        {
            object sourceValue = sourceProp.GetValue(source, null);
            pi.SetValue(target, sourceValue, null);
        }
        else
        {
            throw new ApplicationException(string.Format("CopyClass - can't read/write a property object types {0} & {1}  property:{2}", source.GetType(), target.GetType(), name));
        }
    }

    return target;
}
```
