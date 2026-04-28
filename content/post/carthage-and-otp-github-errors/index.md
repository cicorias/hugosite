---
title: "Carthage and OTP GitHub Errors"
date: 2016-09-24T16:26:01+0000
lastmod: 2016-09-24T16:26:01+0000
slug: "carthage-and-otp-github-errors"
feature_image: "/images/2016/09/Re--carthage-and-OTP-errors---Inbox-2016-09-24-16-14-49.jpg"
aliases:
  - /carthage-and-otp-github-errors/
---

As a reminder to my self...

In [Carthage](https://github.com/Carthage/Carthage) if you start seeing errors `"Must specify two-factor authentication OTP code"...`

One way is to specify via an environment variable:

```
export GITHUB_ACCESS_TOKEN= <get this from Github

```

This comes from here: [Line 145](https://github.com/Carthage/Carthage/blob/49da52b7570f71416a1a1edbcc377bdf3efff5a6/Source/CarthageKit/GitHub.swift#L145)

The other option is to ensure the GitHub credential helper is working and force a credential challenge that will capture your GitHub credentials.

See this: <https://help.github.com/articles/caching-your-github-password-in-git/>

```
git credential-osxkeychain

```
