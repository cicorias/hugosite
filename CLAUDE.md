# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Hugo static site for **cicoria.com** (Shawn Cicoria — CedarLogic, LLC), migrated from Ghost 6.19. Uses the **XMin** theme (git submodule at `themes/hugo-xmin/`). Deployed to GitHub Pages via Actions on push to `main`.

Hugo version: **0.161.0 extended**. Search is powered by Pagefind (indexed post-build via `npx pagefind --site public`).

## Commands

```bash
# Local dev server with drafts
hugo server -D

# Production build
hugo --minify

# Clean and rebuild
hugo --gc --cleanDestinationDir

# Create a new post
hugo new content/post/my-new-post/index.md

# Generate hero images for posts missing feature_image
uv run python scripts/generate_hero_images.py

# Run Ghost → Hugo migration (one-time; source JSON is .gitignored)
uv run python migrate.py
```

## Python Tooling

**Hard rule: use `uv` exclusively.** Never use `pip`, `python -m venv`, `poetry`, `pipenv`, or `conda`.

| Task | Command |
|---|---|
| Sync deps from lockfile | `uv sync` |
| Run a script | `uv run python <script.py>` |
| Add a dependency | `uv add <package>` |
| Add dev dependency | `uv add --dev <package>` |

Always commit `pyproject.toml` and `uv.lock`. Never commit `.venv/`.

## Architecture

### Content Model

All posts are **leaf bundles**: `content/post/<slug>/index.md`. Pages live at `content/<slug>/index.md`.

**Front matter template:**
```yaml
---
title: "Post Title"
date: 2024-01-15T09:00:00-05:00
slug: "url-friendly-slug"
tags: ["containers", "linux"]
summary: "Brief description for list pages and SEO"
feature_image: "/images/2024/01/slug-hero.jpg"
aliases:
  - /old-ghost-slug/
---
```

- `aliases` preserve Ghost URLs so existing links don't break.
- `feature_image` references `static/images/` — **do not colocate images in leaf bundle dirs**; XMin does not resolve bundle-relative images.

### Images

All images live in `static/images/<year>/<month>/`. Reference them in Markdown as `/images/...`. The `scripts/generate_hero_images.py` script (requires Pillow, uses `.venv-charts/` or project venv) generates 1200×630 JPEG hero images for posts that lack a `feature_image`, writing the path back into front matter automatically.

**Never duplicate the `feature_image` as a Markdown image at the top of the post body.** The XMin theme already renders `feature_image` for the post; pasting `![alt](/images/...)` immediately after the front matter creates a visible duplicate hero. The same rule applies to any other image already referenced from front matter — reference it once. Inline images further down the body that are *not* the hero are fine.

### XMin Theme Customization

- Override partials by copying from `themes/hugo-xmin/layouts/partials/` into `layouts/partials/`. **Never edit files inside `themes/hugo-xmin/` directly.**
- Custom CSS goes in `static/css/custom.css`.
- Navigation is in `hugo.toml` under `[[menu.main]]`.

### Ghost Migration

`migrate.py` reads the Ghost JSON export (`dr-shawn-cicoria-cedarlogic-llc.ghost.*.json`, gitignored) and converts posts to Hugo leaf bundles. It uses a custom `GhostConverter` (subclass of `markdownify.MarkdownConverter`) to handle Ghost-specific HTML: fenced code blocks with language hints, `<figure>/<img>` patterns, and YouTube `<iframe>` → `{{< youtube >}}` shortcodes. Ghost internal image URLs (`__GHOST_URL__/content/images/`) are rewritten to `/images/`.

### CI/CD

`.github/workflows/hugo.yaml` builds on push to `main` using Hugo extended, Dart Sass, Go, and Node.js. It runs `npx pagefind` after the build and deploys to GitHub Pages. Cache key is per `run_id` with `hugo-` restore prefix.
