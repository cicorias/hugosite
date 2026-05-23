---
name: new-post
description: Scaffold a new Hugo blog post leaf bundle with complete front matter
---

Create a new Hugo blog post leaf bundle. Accept the post title as the argument (e.g. `/new-post My Great Post`), or ask for it if not provided. Derive the slug from the title: lowercase, spaces to hyphens, strip non-alphanumeric characters.

Optionally accept tags (comma-separated) and a summary. If not provided, leave them as empty placeholders.

Create the file at `content/post/<slug>/index.md` with this exact front matter structure:

```yaml
---
title: "<TITLE>"
date: <TODAY in RFC3339, e.g. 2026-05-19T09:00:00-05:00>
slug: "<slug>"
draft: true
tags: []
summary: ""
aliases:
  - /<slug>/
---
```

Leave the body below the closing `---` empty (just a blank line). Print the full path of the file created.

**Do not paste the `feature_image` (or any other front-matter image) into the body as a Markdown image.** The XMin theme renders `feature_image` for the post automatically; duplicating it as `![alt](/images/...)` immediately after the front matter creates a visible duplicate hero.
