# Repository Guidelines

## Project Structure & Module Organization

This repository is a Hugo static site for `cicoria.com`. Blog posts are Hugo leaf bundles under `content/post/<slug>/index.md`; standalone pages live under `content/<page>/index.md`. Theme overrides belong in `layouts/`, while the upstream XMin theme is a git submodule at `themes/hugo-xmin/` and should not be edited directly. Site images live in `static/images/<year>/<month>/` and are referenced from content as `/images/...`. Python helper scripts live in `scripts/`, with migration support in `migrate.py`.

## Build, Test, and Development Commands

- `hugo server -D`: run a local development server, including draft content.
- `hugo --minify`: build the production site into `public/`.
- `hugo --gc --cleanDestinationDir`: clean old generated files and rebuild.
- `hugo new content/post/my-new-post/index.md`: scaffold a new post bundle.
- `uv sync`: install Python dependencies from `uv.lock`.
- `uv run python scripts/generate_hero_images.py`: generate missing post hero images.
- `uv run python migrate.py`: run the Ghost-to-Hugo migration when needed.

## Coding Style & Naming Conventions

Use Markdown content with complete front matter, including `title`, `date`, `slug`, `tags`, `summary`, and `aliases` when preserving old URLs. Keep post directory names URL-friendly and aligned with the post slug. Use `uv` exclusively for Python workflows; do not use `pip`, Poetry, Conda, or ad hoc virtualenv commands. Override theme behavior through `layouts/` partials or templates, and place custom static assets under `static/`.

## Testing Guidelines

There is no dedicated automated test suite. Validate changes with `hugo --minify` before submitting. For content changes, also run `hugo server -D` and inspect the rendered post or page, checking front matter, aliases, image paths, tags, and summaries. For generated assets, confirm files land under `static/images/...` and are referenced with absolute `/images/...` paths.

## Commit & Pull Request Guidelines

Recent commits use short, imperative messages such as `fix image`, `new article`, and `pg extension`; follow that concise style. Pull requests should summarize the content or code changed, list validation commands run, link related issues when applicable, and include screenshots for layout, styling, or image changes. Mention any migration or generated-image scripts used so reviewers can reproduce the output.
