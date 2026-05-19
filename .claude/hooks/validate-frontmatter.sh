#!/bin/bash
# Warn when a post is saved with missing required front matter fields
input=$(cat)
file_path=$(echo "$input" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_input',{}).get('file_path',''))" 2>/dev/null)

if [[ "$file_path" != *"content/post"* ]] || [[ "$file_path" != *".md" ]]; then
  exit 0
fi

for field in "title:" "date:" "slug:"; do
  if ! grep -q "^$field" "$file_path" 2>/dev/null; then
    echo "WARNING: front matter missing required field: $field" >&2
  fi
done
exit 0
