---
title: "Spring Initializer from the Command Line - Tighten the Developer Loop"
date: 2022-01-19T14:05:27+0000
lastmod: 2022-01-19T14:17:13+0000
slug: "spring-initailizer-from-the-command-line"
tags: ["spring boot", "java", "kotlin"]
feature_image: "/images/2022/01/Screenshot-2022-01-19-090110.png"
aliases:
  - /spring-initailizer-from-the-command-line/
---

For the past year I've had my head buried in Spring Boot for Java, and now Kotlin. A developer approach that I've always followed is that before introducing novel approaches, patterns, recipes, etc. is to implement a bare bones skeleton project first. This is essential to get that "clean room" validation that can prove assumptions, crush them if necessary. But most importantly it can be done in a way that is "as few things as possible" to ensure I understand what is going on.

This is also helpful in tightening the developer loop in the early discovery part. Your brain requires lots of cycles of trying, failing, trying, failing. So, sitting and waiting for a larger app to startup, etc. is Flow killer. Why hurt yourself? Developer Loop is one of my critical areas of focus on what I try to add as value on projects. Make the developer experience "better".

Spring Boot is an extensive platform and framework. Configuration is at the core along with all the helper areas. So, when I'm scaffolding a quick solution, I hate wasting time. Surely, I can do this inside of JetBrains IDE or using the Spring Boot Initializer site - but another cool thing is you an issue a web request (via curl or your favorite tool) with the proper set of parameters and you get a tar Gzip file that you just decompress – then you're off and running.

```
curl https://start.spring.io/starter.tgz \
    -d type=gradle-project \
    -d language=kotlin \
    -d platformVersion=2.6.2 \
    -d packaging=jar \
    -d jvmVersion=11 \
    -d groupId=ms.reference \
    -d artifactId=ReferenceApp \
    -d name=ReferenceApp \
    -d description=Reference%20App%20for%20Spring%20Boot%20Kotlin%20Gradle \
    -d packageName=ms.reference.ReferenceApp \
    -d dependencies=web \
    --output - \
| tar -xzvf -

```

An alternative is via a URL as follows, which provides the same as above, just the query string parameters are explicit curl parameters above.

```bash
https://start.spring.io/#!type=gradle-project&language=kotlin&platformVersion=2.6.2&packaging=jar&jvmVersion=11&groupId=ms.reference&artifactId=ReferenceApp&name=ReferenceApp&description=Reference%20App%20for%20Spring%20Boot%20Kotlin%20Gradle&packageName=ms.reference.ReferenceApp&dependencies=web
```
