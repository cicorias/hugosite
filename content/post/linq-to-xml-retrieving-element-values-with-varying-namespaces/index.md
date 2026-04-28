---
title: "LINQ to XML - retrieving Element values with varying namespaces..."
date: 2008-11-24T14:07:37+0000
lastmod: 2008-11-24T14:07:37+0000
slug: "linq-to-xml-retrieving-element-values-with-varying-namespaces"
aliases:
  - /linq-to-xml-retrieving-element-values-with-varying-namespaces/
---

Recently I had to deal with some XML supplied to a development group that wasn't the greatest in structure.  For one, there was inconsistent use of namespaces and each repeating element had the namespace duplicated.

The goal was to retrieve from the XML various element values for a business object.

So, using LINQ to XML, there's some pretty neat ways to go about this.  The most succinct that I came up with is below - of course it could be tiny bit more succinct in terms of not using locally scoped variable names but it's there for readability

The trick is use of the XNamespace type, which has an implied constructor, then just passing the namespace qualifier on the LINQ statement as a concatenated variable.

12 public void Test2(string xmlContents)

   13 {

   14     XDocument doc = XDocument.Load(new StringReader xmlContents));

   15     XNamespace ns0 = "http://mysimpleXml/rootStuff";

   16     XNamespace ns1 = "http://mysimpleXml/customer";

   17

   18     var query = from c in doc.Elements( ns0 + "myRoot" ).Elements( ns1 + "customer" )

   19                 select c;

   20

   21

   22     foreach (XElement order in query)

   23     {

   24         string firstname = (from c in order.Elements( ns1 + "firstName" ) select c).First().Value;

   25         string lastname = (from c in order.Elements( ns1 + "lastName" ) select c).First().Value;

   26

   27         Console.WriteLine("firstName: " + firstname);

   28         Console.WriteLine("lastName: " + lastname);

   29

   30     }

   31

   32 }

The sample XML is below

1 <?xml version="1.0" encoding="utf-8" ?>

    2 <myRoot xmlns="http://mysimpleXml/rootStuff">

    3   <customer xmlns="http://mysimpleXml/customer">

    4     <firstName>John</firstName>

    5     <lastName>Lennon</lastName>

    6   </customer>

    7   <customer xmlns="http://mysimpleXml/customer">

    8     <firstName>Ringo</firstName>

    9     <lastName>Starr</lastName>

   10   </customer>

   11 </myRoot>
