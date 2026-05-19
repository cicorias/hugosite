---
name: generate-heroes
description: Generate 1200x630 JPEG hero images for Hugo posts that are missing a feature_image, and update their front matter automatically
---

Run the hero image generation script:

```bash
uv run python scripts/generate_hero_images.py
```

After it completes, show the output summary. Then remind the user to stage the new files before committing:

```bash
git add static/images/ content/post/
```
