---
title: "Strings are UTF-16…. There is an error in XML document (1, 1)."
date: 2010-05-28T10:36:23+0000
lastmod: 2010-05-28T10:36:23+0000
slug: "strings-are-utf-16-there-is-an-error-in-xml-document-1-1"
aliases:
  - /strings-are-utf-16-there-is-an-error-in-xml-document-1-1/
---

I had a situation today where an xml document had a directive indicating it was utf-8.  So, the code in question was reading in the “string” of that xml then attempting to de-serialize it using an Xsd generated type.

What you end up with is an exception indicating that there’s an error in the Xml document at (1,1) or something to that effect.

The fix is, run it through a memory stream – which reads the string, but at utf8 bytes – if you have things that fall outside of 8 bit chars, you’ll get an exception.

```
//Need to read it to bytes, to undo the fact that strings are UTF-16 all the time.
//We want it to handle it as UTF8.
byte[] bytes = Encoding.UTF8.GetBytes(_myXmlString);

TargetType myInstance = null;  

using (MemoryStream memStream = new MemoryStream(bytes))  

{  

XmlSerializer tokenSerializer = new XmlSerializer(typeof(TargetType));  

myInstance = (TargetType)tokenSerializer.Deserialize(memStream);  

}

```

Writing is similar – also, adding the default namespace prevents the additional xmlns additions that aren’t necessary:

```
XmlWriterSettings settings = new XmlWriterSettings()
{
    Encoding = Encoding.UTF8,
    Indent = true,
    NewLineOnAttributes = true,
};

XmlSerializerNamespaces xmlnsEmpty = new XmlSerializerNamespaces();
xmlnsEmpty.Add("", "http://www.wow.thisworks.com/2010/05");

MemoryStream memStr = new MemoryStream();
using (XmlWriter writer = XmlTextWriter.Create(memStr, settings))
{
    XmlSerializer tokenSerializer = new XmlSerializer(typeof(TargetType));
    tokenSerializer.Serialize(writer, theInstance, xmlnsEmpty);
}
```
