#!/bin/bash

REACT_SRC_DIR="data/14"
FLASK_STATIC="static/14"
FLASK_TEMPLATES="templates/14"

echo "DEBUG (React) -> Compiling/Deploying ...."
# echo "1. Cleaning previous NODE/NPM ...."
# rm -rf node_modules package-lock.json

# echo "2. Installing npm dependencies ..."
# npm install --no-fund --silent

# echo "3. Cleaning and creating PATHS ..."
mkdir -p "$FLASK_STATIC/assets"

# echo "4. REACT TSX esbuild COMPILING ..."
npx esbuild "$REACT_SRC_DIR/src/bootstrap.tsx" \
  --bundle \
  --minify \
  --sourcemap \
  --outfile="$FLASK_STATIC/14.js" \
  --loader:.tsx=tsx \
  --loader:.png=file \
  --jsx=automatic \
  --target=es2020 \
  --public-path=/static/14

# echo "5. REACT SCSS sass COMPILING ..."
npx sass "$REACT_SRC_DIR/src/style/main.scss" "$FLASK_STATIC/14.css" \
  --no-source-map \
  --style=compressed

# echo "6. Moving HTML to templates"
cp "$REACT_SRC_DIR/static/index.html" "$FLASK_TEMPLATES/index_14.html"

# echo "6. Copying assets, index and cleaning node_modules"
# cp "$REACT_SRC_DIR/static/index.html" "$FLASK_TEMPLATES/index_14.html"
# rm -rf node_modules package-lock.json

echo "DEBUG (React) REACT TSX/SCSS COMPILED AND DEPLOYED! :-)"

