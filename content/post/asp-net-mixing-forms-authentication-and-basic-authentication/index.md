---
title: "ASP.NET - Mixing Forms Authentication and Basic Authentication..."
date: 1969-12-31T19:00:00+0000
lastmod: 2021-07-01T18:02:29+0000
slug: "asp-net-mixing-forms-authentication-and-basic-authentication"
aliases:
  - /asp-net-mixing-forms-authentication-and-basic-authentication/
---

Recently, I was on a project that required access to both internal and external users.  The internal users identities are present in Active Directory.  The external users would not be.

Now, SharePoint has the ability (WSS 3.0 and MOSS 2007) to provide access to a single Content Store / Site Structure with a mix of Authentication providers - such as Active Directory and the Membership Provider framework that is part of ASP.NET 2.0.  However, this was a straight ASP.NET 2.0 implementation.

One requirement was for existing internal users to access the site from an existing Web application that was already protected with Basic Authentication over SSL.  Their experience needs to be Single Signon - that is, I don't want them to view the Forms Authentication login screen - if they're already authenticated via Basic AuthN (or Windows Integrated for that matter) then the site, that is protected with Forms Authentication, should recognize them and proceed with no challenge.

So, we had a few options (probably more, but in the interest of time...), one being build out the entire site out, create 2 distinct web applications, copy to both locations.  Another option was to write our own (or borrow one from MSDN - see links) Authentication Module.

What we're looking for is another option, which is the simplest, allows for as much out-of-the-box ASP.NET capability and no duplication of code/content.

That option is to create a simple site that will create a Forms Authentication ticket (cookie), then is then used to on the primary site.
