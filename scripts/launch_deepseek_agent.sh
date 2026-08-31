#!/usr/bin/env bash
set -euo pipefail

agent_name="${1:-}"

case "$agent_name" in
  pre-award-agent|other-transaction-agent|govcon-growth-agent)
    ;;
  *)
    printf 'Usage: %s {pre-award-agent|other-transaction-agent|govcon-growth-agent}\n' "$0" >&2
    exit 2
    ;;
esac

script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
repo_root="$(CDPATH= cd -- "$script_dir/.." && pwd)"
plugin_root="$repo_root/plugins/$agent_name"

if ! command -v dsh >/dev/null 2>&1; then
  printf 'DeepSeek Harness is not installed or dsh is not on PATH.\n' >&2
  exit 1
fi

if ! command -v uvx >/dev/null 2>&1; then
  printf 'uvx is required for the packaged federal data connections. Install uv first.\n' >&2
  exit 1
fi

export DSH_BUNDLED_SKILL_DIR="$plugin_root/skills"
exec dsh web --patch "$plugin_root/deepseek-harness.patch.yml" "${@:2}"
