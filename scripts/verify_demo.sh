#!/usr/bin/env bash
# Project Mycelium — Nurturing Knowledge Without the Cloud
# Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)
#
# Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
# See LICENSE.md for full text.
#
# verify_demo.sh — Verify that the demo export is valid.
#
# Usage:
#   bash scripts/verify_demo.sh
#
# Exit codes:
#   0 = all checks passed
#   1 = one or more checks failed

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

PASS=0
FAIL=0

check() {
  local desc="$1"
  shift
  if "$@" > /dev/null 2>&1; then
    echo -e "  ${GREEN}✓${NC} $desc"
    ((PASS++))
  else
    echo -e "  ${RED}✗${NC} $desc"
    ((FAIL++))
  fi
}

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo ""
echo "=========================================="
echo "  Project Mycelium — Verification Suite"
echo "=========================================="
echo ""

# ---- File existence ----
echo "📁 Required files:"
check "LICENSE.md exists"           test -f "$ROOT/LICENSE.md"
check "README.md exists"            test -f "$ROOT/README.md"
check "NOTICE.md exists"            test -f "$ROOT/NOTICE.md"
check "CONTRIBUTING.md exists"      test -f "$ROOT/CONTRIBUTING.md"
check "SECURITY.md exists"          test -f "$ROOT/SECURITY.md"
check "CODE_OF_CONDUCT.md exists"   test -f "$ROOT/CODE_OF_CONDUCT.md"
check "PERFORMANCE.md exists"       test -f "$ROOT/PERFORMANCE.md"
check "DEPLOYMENT.md exists"        test -f "$ROOT/DEPLOYMENT.md"
check "PRESENTER.md exists"         test -f "$ROOT/PRESENTER.md"
check "FAQ.md exists"               test -f "$ROOT/FAQ.md"
check "package.json exists"         test -f "$ROOT/package.json"
check "requirements.txt exists"     test -f "$ROOT/requirements.txt"
check "pyproject.toml exists"       test -f "$ROOT/pyproject.toml"
check "Dockerfile exists"           test -f "$ROOT/Dockerfile"
check "docker-compose.yml exists"   test -f "$ROOT/docker-compose.yml"
check "deliverables.txt exists"     test -f "$ROOT/deliverables.txt"

echo ""
echo "📁 Documentation:"
check "docs/ARCHITECTURE.md exists" test -f "$ROOT/docs/ARCHITECTURE.md"
check "docs/DESIGN.md exists"       test -f "$ROOT/docs/DESIGN.md"
check "docs/validate_docs.py exists" test -f "$ROOT/docs/validate_docs.py"

echo ""
echo "📁 Backend:"
check "backend __init__.py"         test -f "$ROOT/src/backend/mycelium/__init__.py"
check "backend config.py"           test -f "$ROOT/src/backend/mycelium/config.py"
check "backend models.py"           test -f "$ROOT/src/backend/mycelium/models.py"
check "backend database.py"         test -f "$ROOT/src/backend/mycelium/database.py"
check "backend schemas.py"          test -f "$ROOT/src/backend/mycelium/schemas.py"
check "backend chunking.py"         test -f "$ROOT/src/backend/mycelium/chunking.py"
check "backend services.py"         test -f "$ROOT/src/backend/mycelium/services.py"
check "backend main.py"             test -f "$ROOT/src/backend/mycelium/main.py"
check "backend routes.py"           test -f "$ROOT/src/backend/mycelium/routes.py"

echo ""
echo "📁 Frontend:"
check "frontend package.json"       test -f "$ROOT/src/frontend/package.json"
check "frontend vite.config.ts"     test -f "$ROOT/src/frontend/vite.config.ts"
check "frontend index.html"         test -f "$ROOT/src/frontend/index.html"
check "frontend App.tsx"            test -f "$ROOT/src/frontend/src/App.tsx"
check "frontend main.tsx"           test -f "$ROOT/src/frontend/src/main.tsx"
check "frontend types.ts"           test -f "$ROOT/src/frontend/src/types.ts"
check "frontend api.ts"             test -f "$ROOT/src/frontend/src/api.ts"
check "frontend hooks.ts"           test -f "$ROOT/src/frontend/src/hooks.ts"
check "frontend index.css"          test -f "$ROOT/src/frontend/src/index.css"
check "frontend demoData.ts"        test -f "$ROOT/src/frontend/src/demoData.ts"

echo ""
echo "📁 Components:"
check "Icon.tsx"                    test -f "$ROOT/src/frontend/src/components/Icon.tsx"
check "Button.tsx"                  test -f "$ROOT/src/frontend/src/components/Button.tsx"
check "Input.tsx"                   test -f "$ROOT/src/frontend/src/components/Input.tsx"
check "Modal.tsx"                   test -f "$ROOT/src/frontend/src/components/Modal.tsx"
check "Tooltip.tsx"                 test -f "$ROOT/src/frontend/src/components/Tooltip.tsx"
check "Switch.tsx"                  test -f "$ROOT/src/frontend/src/components/Switch.tsx"
check "NodeCard.tsx"                test -f "$ROOT/src/frontend/src/components/NodeCard.tsx"
check "SearchBar.tsx"               test -f "$ROOT/src/frontend/src/components/SearchBar.tsx"
check "components/index.ts"         test -f "$ROOT/src/frontend/src/components/index.ts"

echo ""
echo "📁 Modules:"
check "GraphCanvas.tsx"             test -f "$ROOT/src/frontend/src/graph/GraphCanvas.tsx"
check "CRDTDocument.ts"             test -f "$ROOT/src/frontend/src/crdt/CRDTDocument.ts"
check "P2PManager.ts"               test -f "$ROOT/src/frontend/src/p2p/P2PManager.ts"
check "LocalLLMAdapter.ts"          test -f "$ROOT/src/frontend/src/ai/LocalLLMAdapter.ts"

echo ""
echo "📁 Tests:"
check "test_chunking.py"            test -f "$ROOT/tests/backend/test_chunking.py"
check "test_models.py"              test -f "$ROOT/tests/backend/test_models.py"
check "test_schemas.py"             test -f "$ROOT/tests/backend/test_schemas.py"
check "test_services.py"            test -f "$ROOT/tests/backend/test_services.py"
check "test_config.py"              test -f "$ROOT/tests/backend/test_config.py"
check "crdt.test.ts"                test -f "$ROOT/tests/frontend/crdt.test.ts"
check "ai.test.ts"                  test -f "$ROOT/tests/frontend/ai.test.ts"
check "p2p.test.ts"                 test -f "$ROOT/tests/frontend/p2p.test.ts"
check "demoData.test.ts"            test -f "$ROOT/tests/frontend/demoData.test.ts"

echo ""
echo "📁 CI/CD:"
check "ci/ci.yml"                   test -f "$ROOT/ci/ci.yml"
check "ci/deploy-static.yml"        test -f "$ROOT/ci/deploy-static.yml"
check ".github/workflows/ci.yml"    test -f "$ROOT/.github/workflows/ci.yml"
check ".github/workflows/deploy-static.yml" test -f "$ROOT/.github/workflows/deploy-static.yml"
check ".github/PULL_REQUEST_TEMPLATE.md"    test -f "$ROOT/.github/PULL_REQUEST_TEMPLATE.md"
check ".github/ISSUE_TEMPLATE/bug_report.md"     test -f "$ROOT/.github/ISSUE_TEMPLATE/bug_report.md"
check ".github/ISSUE_TEMPLATE/feature_request.md" test -f "$ROOT/.github/ISSUE_TEMPLATE/feature_request.md"
check ".github/ISSUE_TEMPLATE/question.md"       test -f "$ROOT/.github/ISSUE_TEMPLATE/question.md"

echo ""
echo "📁 Scripts:"
check "export_demo.py"              test -f "$ROOT/scripts/export_demo.py"
check "seed_demo_data.py"           test -f "$ROOT/scripts/seed_demo_data.py"
check "verify_demo.sh"              test -f "$ROOT/scripts/verify_demo.sh"

echo ""
echo "📁 Deploy:"
check "deploy/netlify.toml"         test -f "$ROOT/deploy/netlify.toml"
check "deploy/vercel.json"          test -f "$ROOT/deploy/vercel.json"

echo ""
echo "📁 Examples:"
check "examples/cids.json"          test -f "$ROOT/examples/cids.json"

# ---- Content checks ----
echo ""
echo "📝 Content checks:"
check "LICENSE mentions ZPL"        grep -q "Zorvia Public License" "$ROOT/LICENSE.md"
check "README has TL;DR"            grep -q "TL;DR" "$ROOT/README.md"
check "Backend has __version__"     grep -q "__version__" "$ROOT/src/backend/mycelium/__init__.py"

# ---- Summary ----
TOTAL=$((PASS + FAIL))
echo ""
echo "=========================================="
echo "  Results: ${PASS}/${TOTAL} passed, ${FAIL} failed"
echo "=========================================="
echo ""

if [ "$FAIL" -gt 0 ]; then
  echo -e "${RED}Some checks failed.${NC}"
  exit 1
else
  echo -e "${GREEN}All checks passed! ✓${NC}"
  exit 0
fi
