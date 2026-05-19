#!/bin/bash
# Block direct edits to the hugo-xmin git submodule
input=$(cat)
file_path=$(echo "$input" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_input',{}).get('file_path',''))" 2>/dev/null)

if [[ "$file_path" == *"themes/hugo-xmin"* ]]; then
  echo "ERROR: Do not edit the hugo-xmin theme submodule directly." >&2
  echo "Copy the file to layouts/ and edit it there instead." >&2
  exit 1
fi
exit 0
