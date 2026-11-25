#!/usr/bin/env bash
# Copies the deployable site (generated HTML, assets, data) into dist/ for Cloudflare, leaving out sources and repo files.
set -euo pipefail
cd "$(dirname "$0")/../.."
rm -rf dist && mkdir dist
tar -cf - --exclude=./.git --exclude=./.github --exclude=./tools --exclude=./dist --exclude=./node_modules --exclude=./.wrangler \
  --exclude=./README.md --exclude=./LICENSE --exclude=./CNAME --exclude=./.nojekyll --exclude=./.gitignore \
  --exclude=./wrangler.jsonc --exclude=./worker --exclude='.*.sha' --exclude='*.py' --exclude=__pycache__ . | tar -xf - -C dist
cp tools/cf/_headers dist/_headers
echo "dist: $(find dist -type f | wc -l) files, $(du -sh dist | cut -f1)"
