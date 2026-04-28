---
title: "Querying a SharePoint 2013 Task List for Subtasks"
date: 2013-02-28T11:11:01+0000
lastmod: 2013-02-28T11:11:01+0000
slug: "querying-a-sharepoint-2013-task-list-for-subtasks"
aliases:
  - /querying-a-sharepoint-2013-task-list-for-subtasks/
---

The CAML for the query easily enough includes a ParentID reference.  However, if you’re spelunking around in SP 2013 using the OData services, you might have a hard time finding the ParentID field.

However, if you just issue the query:

[//web/\_api/Web/Lists/getByTitle('TaskListName')/Items/?$filter=ParentID">https://<server>/<mp>/web/\_api/Web/Lists/getByTitle('TaskListName')/Items/?$filter=ParentID](https://<server>/<mp>/web/_api/Web/Lists/getByTitle('TaskListName')/Items/?$filter=ParentID) eq ‘101’

You’ll be able to retrieve all Tasks that have task #101 as their parent.
