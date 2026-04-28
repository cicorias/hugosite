---
title: "Getting Azure Defender Security Scores into JSON"
date: 2025-12-11T21:12:15+0000
lastmod: 2025-12-11T21:12:15+0000
slug: "getting-azure-defender-security-scores-into-json"
summary: "getting json for azure defender scores"
tags: ["azure", "bash", "cloud", "security"]
feature_image: "https://images.unsplash.com/photo-1485230405346-71acb9518d9c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3wxMTc3M3wwfDF8c2VhcmNofDR8fHNlY3VyaXR5fGVufDB8fHx8MTc2NTQxNzc0OHww&ixlib=rb-4.1.0&q=80&w=2000"
aliases:
  - /getting-azure-defender-security-scores-into-json/
---

This is kinda simple but I keep needing to come back to it...

```shell
#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   ./export-azure-security.sh [SUBSCRIPTION_ID] [OUTPUT_DIR]
#
# Examples:
#   ./export-azure-security.sh
#   ./export-azure-security.sh 00000000-0000-0000-0000-000000000000 security-export

SUBSCRIPTION_ID="${1-}"
OUT_DIR="${2:-azure-security-export}"

mkdir -p "$OUT_DIR"

# Build subscription argument if provided
SUB_ARG=()
if [[ -n "${SUBSCRIPTION_ID}" ]]; then
  SUB_ARG=(--subscription "$SUBSCRIPTION_ID")
fi

echo "Exporting Azure security dashboard data to '$OUT_DIR'..."

echo "1/4 Secure scores..."
az security secure-scores list \
  "${SUB_ARG[@]}" \
  --output json > "$OUT_DIR/secure-scores.json"

echo "2/4 Security assessments (recommendations)..."
az security assessment list \
  "${SUB_ARG[@]}" \
  --output json > "$OUT_DIR/security-assessments.json"

echo "3/4 Security alerts..."
az security alert list \
  "${SUB_ARG[@]}" \
  --output json > "$OUT_DIR/security-alerts.json"

echo "4/4 Regulatory compliance (standards and controls)..."
az security regulatory-compliance-standards list \
  "${SUB_ARG[@]}" \
  --output json > "$OUT_DIR/regulatory-standards.json"

az security regulatory-compliance-controls list \
  "${SUB_ARG[@]}" \
  --output json > "$OUT_DIR/regulatory-controls.json"

echo "Done."
echo "Files created in: $OUT_DIR"
ls -1 "$OUT_DIR"

```
