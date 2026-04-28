---
title: "Generate OpenTelemetry Compliant TraceParent TraceContext Headers using Bash"
date: 2022-07-11T16:13:32+0000
lastmod: 2022-07-11T16:13:32+0000
slug: "generate-opentelemetry-compliant-traceparent-tracecontext-headers-using-bash"
tags: ["azure", "bash", "cloud", "utilities"]
feature_image: "https://www.cicoria.com/content/images/2022/07/ot.jpg"
aliases:
  - /generate-opentelemetry-compliant-traceparent-tracecontext-headers-using-bash/
---

For the past year or so I've been working with Observability and quite a bit of Open Telemetry.  One of the requirements of triggering a great front-to-back trace is providing a W3C compliant header in the Open Telemetry format. That format detailed in [W3C Trance Context](<https://www.w3.org/TR/trace-context/#examples-of-http-traceparent-headers>).

Very simply in bash, we were able to use the following, which when we lit up for example Application Insights in Azure, a fully holistic view with all sub-spans appears providing a great analytics experience.

```bash
#!/usr/bin/env bash

# set -eox

# see spec: https://www.w3.org/TR/trace-context
# version-format   = trace-id "-" parent-id "-" trace-flags
# trace-id         = 32HEXDIGLC  ; 16 bytes array identifier. All zeroes forbidden
# parent-id        = 16HEXDIGLC  ; 8 bytes array identifier. All zeroes forbidden
# trace-flags      = 2HEXDIGLC   ; 8 bit flags. Currently, only one bit is used. See below for detail

VERSION="00" # fixed in spec at 00
TRACE_ID="$(cat /dev/urandom | tr -dc 'a-f0-9' | fold -w 32 | head -n 1)"
PARENT_ID="00$(cat /dev/urandom | tr -dc 'a-f0-9' | fold -w 14 | head -n 1)"
TRACE_FLAG="01"   # sampled
TRACE_PARENT="$VERSION-$TRACE_ID-$PARENT_ID-$TRACE_FLAG"
TRACE_STATE="mystate"

MESSAGE="Lorem ipsum $(cat /dev/urandom | tr -dc 'a-zA-Z' | fold -w 20 | head -n 1)"

URL="http://localhost:8080/messages"

echo "sending to host $URL"
echo "sending a trace-parent of: $TRACE_PARENT"

curl --location --request POST "${URL}" \
--header "traceparent: $TRACE_PARENT" \
--header "Content-Type: application/json" \
--data-raw "{\"message\":\"$MESSAGE\",\"traceparent\":\"$TRACE_PARENT\" }"
```
