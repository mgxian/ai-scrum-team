#!/usr/bin/env bash
# Setup script: adapt project structure for Kiro IDE, Kiro CLI, and OpenCode
#
# Skills source of truth: skills/ (project root)
# - Kiro IDE expects skills at .kiro/skills/ → symlink
# - Kiro CLI uses .kiro/agents/*.json with skill:// resources → direct path
# - OpenCode uses .opencode/agent/*.md + opencode.json instructions → direct path

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "Setting up AI Scrum Team for multi-tool compatibility..."
echo ""

# --- Kiro IDE: Skills symlink ---
SKILLS_SOURCE="$PROJECT_ROOT/skills"
SKILLS_TARGET="$PROJECT_ROOT/.kiro/skills"

if [ -L "$SKILLS_TARGET" ]; then
  echo "✓ Kiro IDE: .kiro/skills symlink already exists"
elif [ -d "$SKILLS_TARGET" ]; then
  echo "⚠ Kiro IDE: .kiro/skills is a real directory, skipping (remove it manually if you want the symlink)"
elif [ -d "$SKILLS_SOURCE" ]; then
  ln -s ../../skills "$SKILLS_TARGET"
  echo "✓ Kiro IDE: Created symlink .kiro/skills -> ../../skills"
else
  echo "✗ skills/ directory not found at project root"
  exit 1
fi

# --- OpenCode: verify agent files ---
if [ -d "$PROJECT_ROOT/.opencode/agent" ]; then
  AGENT_COUNT=$(find "$PROJECT_ROOT/.opencode/agent" -name "*.md" | wc -l | tr -d ' ')
  echo "✓ OpenCode: $AGENT_COUNT agent(s) found in .opencode/agent/"
else
  echo "⚠ OpenCode: .opencode/agent/ not found, OpenCode agents not available"
fi

if [ -f "$PROJECT_ROOT/opencode.json" ]; then
  echo "✓ OpenCode: opencode.json config found"
else
  echo "⚠ OpenCode: opencode.json not found, skill instructions not loaded"
fi

# --- Kiro CLI: verify agent files ---
if [ -d "$PROJECT_ROOT/.kiro/agents" ]; then
  JSON_COUNT=$(find "$PROJECT_ROOT/.kiro/agents" -name "*.json" | wc -l | tr -d ' ')
  echo "✓ Kiro CLI: $JSON_COUNT agent(s) found in .kiro/agents/"
else
  echo "⚠ Kiro CLI: .kiro/agents/ not found"
fi

echo ""
echo "Done. Project is ready for Kiro IDE, Kiro CLI, and OpenCode."
