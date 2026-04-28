---
title: "Typescript and non string Environment Variable parsing"
date: 2018-12-05T19:41:41+0000
lastmod: 2018-12-05T19:41:41+0000
slug: "typescript-and-non-string-environment-variable-parsing"
feature_image: "https://www.cicoria.com/content/images/2018/12/image-1.png"
aliases:
  - /typescript-and-non-string-environment-variable-parsing/
---

Leaving this here as just a simple get an env variable and 'cast' to boolean is a PITA. But this is what I ended up with...

```
const skipTestSetting = process.env.BOT_SKIP_KNOWN_FAILED_TESTS;
export const shouldSkip = (t: TestObj): boolean => {
    const noSkip = skipTestSetting === 'true'
        ? true :  typeof skipTestSetting === 'string'
        ? !!+skipTestSetting
        : !!skipTestSetting;

```
