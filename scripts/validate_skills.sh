#!/usr/bin/env bash
# Validate all Agent Skills against the official agentskills.io specification.
#
# Uses the official reference library `skills-ref` (https://github.com/agentskills/agentskills).
# No global install required: the script runs it through `uvx` or `pipx run`.
#
# Usage:
#   scripts/validate_skills.sh                 # validate every plugins/*/skills/*
#   scripts/validate_skills.sh <skill-dir> ... # validate specific skill directories
#
# Exit code is non-zero if any skill fails validation.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# Resolve a runner for the official `agentskills` CLI from the `skills-ref` package.
if command -v uvx >/dev/null 2>&1; then
  RUN=(uvx --from skills-ref agentskills)
elif command -v pipx >/dev/null 2>&1; then
  RUN=(pipx run --spec skills-ref agentskills)
elif command -v agentskills >/dev/null 2>&1; then
  RUN=(agentskills)
else
  echo "ERROR: need 'uvx' (astral uv) or 'pipx' to run the official skills-ref validator." >&2
  echo "       Install uv (https://docs.astral.sh/uv/) or 'pip install skills-ref'." >&2
  exit 127
fi

# Build the list of skill directories to validate.
declare -a SKILLS
if [[ $# -gt 0 ]]; then
  SKILLS=("$@")
else
  while IFS= read -r skill_md; do
    SKILLS+=("$(dirname "$skill_md")")
  done < <(find plugins -type f -name SKILL.md | sort)
fi

if [[ ${#SKILLS[@]} -eq 0 ]]; then
  echo "No skills found under plugins/*/skills/*." >&2
  exit 0
fi

pass=0
fail=0
declare -a FAILED
for dir in "${SKILLS[@]}"; do
  dir="${dir%/}"
  if output="$("${RUN[@]}" validate "$dir" 2>&1)"; then
    pass=$((pass + 1))
  else
    fail=$((fail + 1))
    FAILED+=("$dir")
    echo "FAIL  $dir"
    echo "$output" | sed 's/^/      /'
  fi
done

echo "----------------------------------------"
echo "Agent Skills validation: ${pass} passed, ${fail} failed."
if [[ $fail -gt 0 ]]; then
  echo "Non-conformant skills:" >&2
  printf '  - %s\n' "${FAILED[@]}" >&2
  exit 1
fi
