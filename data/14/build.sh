#!/bin/bash

REACT_SRC_DIR="./data/14/src"
FLASK_STATIC="./static/14"
FLASK_TEMPLATES="./templates/14"

echo "DEBUG 14 NODE:  Cleaning ..."
rm -rf node_modules package-lock.json

echo "DEBUG 14 NODE:  npm install ..."
npm install --no-fund --silent

echo "DEBUG 14 CMD: Creating static/assets PATHS ..."
mkdir -p "$FLASK_STATIC/assets"

# REACT TSX
echo "DEBUG 14 REACT -> TSX esbuild started"
npx esbuild "$REACT_SRC_DIR/bootstrap.tsx" \
  --bundle \
  --minify \
  --sourcemap \
  --outfile="$FLASK_STATIC/14.js" \
  --loader:.tsx=tsx \
  --loader:.png=file \
  --jsx=automatic \
  --target=es2020

# SCSS
echo "DEBUG 14 SCSS -> SCSS compiling ..."
npx sass "$REACT_SRC_DIR/style/main.scss" "$FLASK_STATIC/14.css" \
  --no-source-map \
  --style=compressed

# PATHS and assets
echo "DEBUG 14 CMD -> Copying HTML - ASSETS"
cp -rv "$REACT_SRC_DIR/static/assets/" "$FLASK_STATIC/assets/"
cp "$REACT_SRC_DIR/static/index.html" "$FLASK_TEMPLATES/index_14.html"

echo "DEBUG 14 NODE:  Removing node_modules ..."
rm -rf node_modules

echo "✅ DEBUG 14 REACT ALL DONE!"

