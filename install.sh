#!/bin/sh
set -eu

if [ -n "${CODEX_HOME:-}" ]; then
  codex_home=$CODEX_HOME
else
  codex_home=$HOME/.codex
fi

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
instruction_source=$script_dir/defaults/AGENTS.md
agents_target=$codex_home/AGENTS.md
config_target=$codex_home/config.toml
timestamp=$(date +%Y%m%d-%H%M%S)
start_marker='<!-- codex-efficiency-setup:start -->'
end_marker='<!-- codex-efficiency-setup:end -->'

mkdir -p "$codex_home"

backup_if_present() {
  if [ -f "$1" ]; then
    cp "$1" "$1.bak-$timestamp"
  fi
}

backup_if_present "$agents_target"
backup_if_present "$config_target"

agents_tmp=$(mktemp)
config_tmp=$(mktemp)
trap 'rm -f "$agents_tmp" "$config_tmp"' EXIT HUP INT TERM

if [ -f "$agents_target" ]; then
  awk -v start="$start_marker" -v end="$end_marker" '
    $0 == start { skipping=1; next }
    $0 == end { skipping=0; next }
    !skipping { print }
  ' "$agents_target" > "$agents_tmp"
fi

if [ -s "$agents_tmp" ]; then
  printf '\n' >> "$agents_tmp"
fi
printf '%s\n' "$start_marker" >> "$agents_tmp"
cat "$instruction_source" >> "$agents_tmp"
printf '%s\n' "$end_marker" >> "$agents_tmp"
mv "$agents_tmp" "$agents_target"

if [ -f "$config_target" ]; then
  cp "$config_target" "$config_tmp"
else
  : > "$config_tmp"
fi

update_top_level() {
  key=$1
  value=$2
  next_tmp=$(mktemp)
  awk -v key="$key" -v value="$value" '
    BEGIN { section=0; replaced=0 }
    /^[[:space:]]*\[/ { section=1 }
    !section && !replaced && $0 ~ "^[[:space:]]*" key "[[:space:]]*=" {
      print key " = " value
      replaced=1
      next
    }
    { print }
    END {
      if (!replaced) {
        # Exit status 3 tells the shell to prepend the missing key.
        exit 3
      }
    }
  ' "$config_tmp" > "$next_tmp" || status=$?
  status=${status:-0}
  if [ "$status" -eq 3 ]; then
    { printf '%s = %s\n' "$key" "$value"; cat "$config_tmp"; } > "$next_tmp"
  elif [ "$status" -ne 0 ]; then
    rm -f "$next_tmp"
    return "$status"
  fi
  mv "$next_tmp" "$config_tmp"
  unset status
}

update_top_level model '"gpt-5.6-terra"'
update_top_level model_reasoning_effort '"medium"'
update_top_level service_tier '"default"'
mv "$config_tmp" "$config_target"

printf 'Installed Codex efficiency defaults in %s\n' "$codex_home"
printf '%s\n' 'Start a new Codex task for the global instructions to take effect.'

