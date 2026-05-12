# Copilot Instructions — getblog

## Project Overview

This is a Hugo static site migrating **cicoria.com** from Ghost 6.19. The site is a personal tech blog ("Dr. Shawn Cicoria — CedarLogic, LLC") using the **XMin** theme. Content covers topics like containers, GPU/CUDA, Linux, Windows/WSL, cloud infrastructure, and software development.

## Tooling Rules

- **Python:** Use `uv` and `.venv/` exclusively. Never use `pip`, `poetry`, `pipenv`, `conda`, or `python -m venv` directly. See [.github/instructions/python.instructions.md](.github/instructions/python.instructions.md) for the full rules.

## Build and Development Commands

```bash
# Local dev server with drafts
hugo server -D

# Production build (output goes to public/)
hugo --minify

# Build including drafts
hugo --buildDrafts

# Create a new post
hugo new content/post/my-new-post/index.md

# Clean cache and rebuild
hugo --gc --cleanDestinationDir
```

## Architecture

### Directory Layout

```
├── hugo.toml              # Site configuration (XMin uses TOML)
├── content/
│   ├── post/              # Blog posts (leaf bundles: post-slug/index.md)
│   ├── about/index.md     # Static pages
│   └── resume/index.md
├── assets/                # Processed assets (SCSS, JS pipelines)
├── static/
│   ├── css/custom.css     # XMin style overrides
│   └── images/            # Global images (favicon, site background)
├── layouts/
│   └── partials/          # Override XMin partials (head, footer, etc.)
├── data/                  # Data files (JSON/TOML/YAML)
├── archetypes/            # Templates for `hugo new`
└── themes/xmin/           # XMin theme (git submodule)
```

### Content Model (Ghost → Hugo mapping)

| Ghost concept     | Hugo equivalent                                          |
|-------------------|----------------------------------------------------------|
| Post              | `content/post/<slug>/index.md` (leaf bundle)             |
| Page              | `content/<slug>/index.md`                                |
| Tags              | Front matter `tags: [...]` → taxonomy at `/tags/`        |
| Featured image    | `image` param in front matter, referencing `/images/<file>` in `static/images/` |
| Author            | Single author; set in `hugo.toml` `[params]`             |
| Post excerpt      | `summary` in front matter or `<!--more-->` marker        |
| Internal images   | Stored in `static/images/` and referenced as `/images/<file>` in Markdown |

### Post Front Matter Template

```yaml
---
title: "Post Title"
date: 2024-01-15T09:00:00-05:00
draft: false
slug: "url-friendly-slug"
tags: ["containers", "linux", "gpu"]
summary: "Brief description for list pages and SEO"
aliases:
  - /old-ghost-url/
---
```

- **`aliases`** preserve Ghost URLs so existing links don't break.
- **`slug`** should match the original Ghost slug for URL parity.

## Key Conventions

### Ghost Migration

- Export Ghost content via the Ghost Admin API or JSON export (`ghost export`).
- Convert Ghost HTML/Mobiledoc content to Markdown. Tools like [`ghost-to-hugo`](https://github.com/jbarone/ghostToHugo) can automate this.
- Place images in `static/images/` and reference them as `/images/<file>` in Markdown and front matter. Do **not** colocate images in the post's leaf bundle directory — the XMin theme does not resolve bundle-relative images.
- Preserve original Ghost URLs using `aliases` in front matter to avoid broken links.
- Ghost's `<!--kg-card-begin: code-->` blocks should be converted to fenced code blocks with language hints.

### XMin Theme

- XMin is intentionally minimal — no JavaScript, no complex CSS framework.
- Customize styles in `static/css/custom.css` and reference via `[params]` in `hugo.toml`.
- Override theme partials by copying from `themes/xmin/layouts/partials/` into `layouts/partials/`. Never edit files inside `themes/xmin/` directly.
- Navigation is configured in `hugo.toml` under `[[menu.main]]`.

### Features Carried Over from Ghost

The Ghost site uses several features that need Hugo equivalents:

- **Code syntax highlighting**: Hugo uses Chroma (built-in). No external JS needed. Configure in `hugo.toml` under `[markup.highlight]`.
- **Mermaid diagrams**: Add a partial or shortcode that loads the Mermaid JS library. Only include on pages that use it.
- **Google Analytics**: Use Hugo's built-in `googleAnalytics` config key and the `google_analytics` internal template, or a partial for gtag.js.
- **Structured data (JSON-LD)**: Implement via a `layouts/partials/schema.html` template.
- **Open Graph / Twitter meta tags**: Hugo has built-in OG templates (`{{ template "_internal/opengraph.html" . }}`).
- **RSS**: Built into Hugo by default at `/index.xml`.
- **Cookie consent**: Add via a partial that loads the CookieYes script.

### Hugo Shortcodes

Prefer Hugo shortcodes over raw HTML in Markdown content. Create custom shortcodes in `layouts/shortcodes/` for:

- Mermaid diagram blocks
- YouTube/Vimeo embeds (Hugo has built-in ones)
- Image figures with captions
- Code blocks with special formatting

### Configuration

- Use `hugo.toml` (TOML format) for all configuration — XMin examples use TOML.
- Environment-specific config goes in `config/` directory (e.g., `config/production/hugo.toml`).
- The base URL for production is `https://www.cicoria.com/`.
