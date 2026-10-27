#!/usr/bin/env bash
set -euo pipefail

diagram_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
mermaid_cli=${MMDC:-}
if [[ -z "$mermaid_cli" ]]; then
  if command -v mmdc >/dev/null 2>&1; then
    mermaid_cli=$(command -v mmdc)
  else
    mermaid_cli=/workspace/pqc-environment/mermaid/node_modules/.bin/mmdc
  fi
fi
test -x "$mermaid_cli"

# Managed Chromium permits HTTP but blocks file:// navigation. The locally
# installed CLI has a one-line compatibility patch to accept this HTML URL.
cli_source=/workspace/pqc-environment/mermaid/node_modules/@mermaid-js/mermaid-cli
if [[ "$mermaid_cli" == /workspace/pqc-environment/mermaid/node_modules/.bin/mmdc ]]; then
  python3 "$diagram_dir/patch_cli.py" "$cli_source/src/index.js"
  port_file=$(mktemp /tmp/pqc-mermaid-port.XXXXXX)
  python3 "$diagram_dir/serve_cli.py" "$cli_source/dist/index.html" "$port_file" &
  html_server_pid=$!
  trap 'kill "$html_server_pid" 2>/dev/null || true; rm -f "$port_file"' EXIT
  for ((attempt=0; attempt<100; attempt++)); do
    [[ -s "$port_file" ]] && break
    sleep 0.05
  done
  [[ -s "$port_file" ]]
  export MMDC_RENDER_HTML_URL="http://127.0.0.1:$(cat "$port_file")/index.html"
fi

# Mermaid CLI 12 uses --size; older installations use viewport dimensions.
if "$mermaid_cli" --help | rg -q -- '--size'; then
  sizing=(--size 4200)
else
  sizing=(-w 2400 -H 1600)
fi

shopt -s nullglob
sources=("$diagram_dir"/*.mmd)
(( ${#sources[@]} > 0 ))
for source in "${sources[@]}"; do
  target=${source%.mmd}
  "$mermaid_cli" -i "$source" -o "$target.svg" \
    -c "$diagram_dir/mermaid-config.json" -p "$diagram_dir/puppeteer-config.json" \
    -b white "${sizing[@]}"
  "$mermaid_cli" -i "$source" -o "$target.png" \
    -c "$diagram_dir/mermaid-config.json" -p "$diagram_dir/puppeteer-config.json" \
    -b white "${sizing[@]}" -s 2
done
