---
title: "Emitting XML via LINQ"
date: 2008-12-03T02:49:42+0000
lastmod: 2008-12-03T02:49:42+0000
slug: "emitting-xml-via-linq"
aliases:
  - /emitting-xml-via-linq/
---

Just posted about reading XML via LINQ. Now, this post is about the opposite direction - emitting XML from a collection. The simplicity of LINQ provides a straightforward interaction with XML makes LINQ to XML for me one of the easiest and most natural ways to interact with XML.

The following emits a collection of objects out to an XElement (which can be streamed elsewhere as required.

```
   35 Customer[] customers = new Customer[]{
```
```
   36    new Customer{
```
```
   37     firstName="john", lastName="lennon"},
```
```
   38    new Customer{
```
```
   39       firstName="ringo", lastName="starr"} };
```
```
   40 
```
```
   41 XNamespace ns1 = "UGLY_NAMESPACE";
```
```
   42 
```
```
   43 XElement custs = new XElement("myRoot",
```
```
   44 from c in customers
```
```
   45  select new XElement(ns1 + "customer",
```
```
   46   new XElement(ns1 + "firstName", c.firstName),
```
```
   47   new XElement(ns1 + "lastName", c.lastName)));
```
```
 
```
```
 
```

This creates the following XML

```
 
```

```
    1 <myRoot>
```
```
    2   <customer xmlns="UGLY_NAMESPACE">
```
```
    3     <firstName>john</firstName>
```
```
    4     <lastName>lennon</lastName>
```
```
    5   </customer>
```
```
    6   <customer xmlns="UGLY_NAMESPACE">
```
```
    7     <firstName>ringo</firstName>
```
```
    8     <lastName>starr</lastName>
```
```
    9   </customer>
```
```
   10 </myRoot>
```
