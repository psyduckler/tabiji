#!/bin/bash
# Build the Scam Atlas into ePub and PDF.
#
# Requirements:
#   pip install pyyaml weasyprint
#   brew install pandoc
#
# Usage:
#   bash scripts/build.sh           # build everything
#   bash scripts/build.sh epub      # only ePub
#   bash scripts/build.sh pdf       # only PDF
#   bash scripts/build.sh kdp       # PDF sized for KDP paperback (6x9, 0.875 trim)

set -euo pipefail

cd "$(dirname "$0")/.."

INPUT="the-big-book-of-travel-scams-FULL.md"
TARGET="${1:-all}"

# Make sure the assembled manuscript exists
if [ ! -f "$INPUT" ]; then
  echo "Assembling manuscript first..."
  python3 scripts/assemble.py
fi

mkdir -p build

build_epub() {
  echo "Building ePub..."
  pandoc "$INPUT" \
    --from markdown \
    --to epub3 \
    --toc \
    --toc-depth=2 \
    --metadata title="The Big Book of Travel Scams" \
    --metadata subtitle="Thirty Scripts, Seven Patterns, and the Defense for Each (2026 Edition)" \
    --metadata author="Bernard Huang, Editor · Tabiji" \
    --metadata date="2026" \
    --metadata publisher="Tabiji" \
    --metadata language="en-US" \
    --metadata rights="© 2026 Tabiji Inc. All rights reserved." \
    -o build/the-big-book-of-travel-scams.epub
  echo "  → build/the-big-book-of-travel-scams.epub"
}

build_pdf() {
  echo "Building PDF (web/screen format)..."
  # Use weasyprint via pandoc; produces a screen-readable PDF.
  pandoc "$INPUT" \
    --from markdown \
    --to html \
    --toc \
    --toc-depth=2 \
    --standalone \
    -o build/the-big-book-of-travel-scams.html
  weasyprint build/the-big-book-of-travel-scams.html build/the-big-book-of-travel-scams.pdf
  echo "  → build/the-big-book-of-travel-scams.pdf"
}

build_kdp() {
  echo "Building KDP-paperback PDF (6x9 trim)..."
  # Uses LaTeX engine for paperback-grade interior PDF.
  pandoc "$INPUT" \
    --from markdown \
    --to pdf \
    --toc \
    --toc-depth=2 \
    --pdf-engine=xelatex \
    --variable=geometry:paperwidth=6in \
    --variable=geometry:paperheight=9in \
    --variable=geometry:inner=0.875in \
    --variable=geometry:outer=0.5in \
    --variable=geometry:top=0.75in \
    --variable=geometry:bottom=0.75in \
    --variable=fontsize=10pt \
    --variable=mainfont="Charter" \
    -o build/the-big-book-of-travel-scams-kdp.pdf
  echo "  → build/the-big-book-of-travel-scams-kdp.pdf"
}

case "$TARGET" in
  epub)  build_epub ;;
  pdf)   build_pdf ;;
  kdp)   build_kdp ;;
  all)   build_epub; build_pdf; build_kdp ;;
  *)     echo "Unknown target: $TARGET (use: epub | pdf | kdp | all)"; exit 1 ;;
esac

echo ""
echo "Done. Outputs in build/."
ls -lh build/
