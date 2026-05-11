#!/usr/bin/env bash
# ==============================================================================
# build.sh — Rebuild all KDP-ready artifacts for The Dental Tourism Field Guide
#
# Outputs (written to book-dental/build/):
#   - the-dental-tourism-field-guide.epub  (Kindle ebook)
#   - kindle-cover.jpg                      (1600×2400 sRGB JPEG)
#   - paperback-interior.pdf                (6×9", KDP-valid)
#   - paperback-wrap-cover.pdf              (full wrap with bleed)
#
# Run from repo root:
#   bash book-dental/scripts/build.sh
#
# Requires: pandoc, weasyprint, rsvg-convert, sips (macOS), python3
# ==============================================================================

set -euo pipefail

# Resolve directories relative to the script location (repo-relative)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BOOK_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$BOOK_DIR/build"
SRC_MS="$BOOK_DIR/manuscript/00-the-dental-tourism-field-guide.md"
COVER_SVG="$BOOK_DIR/assets/svg/cover-front.svg"
WRAP_SVG="$BOOK_DIR/assets/svg/cover-wrap.svg"
PRINT_CSS="$BOOK_DIR/assets/css/print-style.css"
EPUB_CSS="$BOOK_DIR/assets/css/epub-style.css"
PREPROCESS="$SCRIPT_DIR/preprocess.py"

mkdir -p "$BUILD_DIR"

echo "==> Stripping HTML designer comments from manuscript"
perl -0777 -pe 's/<!--[\s\S]*?-->\n*//g' "$SRC_MS" > "$BUILD_DIR/manuscript-source.md"

echo "==> Adding pandoc semantic divs (preprocess.py)"
# preprocess.py reads/writes from its own working directory, so cd into build
( cd "$BUILD_DIR" && cp manuscript-source.md "$BUILD_DIR/manuscript-source.md" 2>/dev/null || true )
SRC_FOR_PREPROCESS="$BUILD_DIR/manuscript-source.md" \
DST_FOR_PREPROCESS="$BUILD_DIR/manuscript-processed.md" \
python3 - <<PYEOF
import sys
sys.path.insert(0, "$SCRIPT_DIR")
from pathlib import Path
import preprocess as p
p.SRC = Path("$BUILD_DIR/manuscript-source.md")
p.DST = Path("$BUILD_DIR/manuscript-processed.md")
p.main()
PYEOF

echo "==> Building Kindle cover (PNG → JPG, sRGB, 1600×2400)"
rsvg-convert -w 1600 -h 2400 -f png -o "$BUILD_DIR/cover-1600x2400.png" "$COVER_SVG"
sips -s format jpeg -s formatOptions 95 \
     "$BUILD_DIR/cover-1600x2400.png" \
     --out "$BUILD_DIR/kindle-cover.jpg" >/dev/null 2>&1

echo "==> Building EPUB"
pandoc "$BUILD_DIR/manuscript-processed.md" \
  -o "$BUILD_DIR/the-dental-tourism-field-guide.epub" \
  --epub-cover-image="$BUILD_DIR/kindle-cover.jpg" \
  --css="$EPUB_CSS" \
  --metadata title="The Dental Tourism Field Guide" \
  --metadata subtitle="A Buyer-Protection Guide to Dental Care Abroad" \
  --metadata author="Bernard Huang" \
  --metadata date="$(date +%Y-%m-%d)" \
  --metadata publisher="Tabiji" \
  --metadata lang="en" \
  --metadata rights="© $(date +%Y) Tabiji. All rights reserved." \
  --toc --toc-depth=2 --split-level=1

echo "==> Building paperback interior PDF (HTML → weasyprint)"
pandoc "$BUILD_DIR/manuscript-processed.md" \
  -o "$BUILD_DIR/manuscript.html" \
  --standalone \
  --metadata title="The Dental Tourism Field Guide" \
  --metadata subtitle="A Buyer-Protection Guide to Dental Care Abroad" \
  --metadata author="Bernard Huang" \
  --metadata date="" \
  --css="$PRINT_CSS"
weasyprint "$BUILD_DIR/manuscript.html" "$BUILD_DIR/paperback-interior.pdf"

echo "==> Building paperback wrap cover PDF"
# Read width/height from the SVG viewBox (assumes "viewBox=\"0 0 W H\"")
SVG_W=$(grep -oE 'viewBox="0 0 [0-9.]+' "$WRAP_SVG" | awk '{print $3}')
SVG_H=$(grep -oE 'viewBox="0 0 [0-9.]+ [0-9.]+' "$WRAP_SVG" | awk '{print $4}')
WIDTH_IN=$(python3 -c "print($SVG_W / 100)")
HEIGHT_IN=$(python3 -c "print($SVG_H / 100)")
rsvg-convert \
  --page-width "${WIDTH_IN}in" --page-height "${HEIGHT_IN}in" \
  --width "${WIDTH_IN}in" --height "${HEIGHT_IN}in" \
  -f pdf1.7 -o "$BUILD_DIR/paperback-wrap-cover.pdf" "$WRAP_SVG"

echo ""
echo "==> Build complete. Files in $BUILD_DIR:"
ls -lh "$BUILD_DIR" | grep -E "(epub|jpg|pdf)$"

echo ""
echo "==> Verification:"
PAGES=$(pdfinfo "$BUILD_DIR/paperback-interior.pdf" | awk '/^Pages:/{print $2}')
SPINE=$(python3 -c "print(f'{$PAGES * 0.002252:.4f}')")
EXPECTED_W=$(python3 -c "print(f'{0.125 + 6 + $PAGES * 0.002252 + 6 + 0.125:.4f}')")
echo "  Interior page count: $PAGES"
echo "  Required spine width: ${SPINE}\""
echo "  Required wrap cover width: ${EXPECTED_W}\""
echo ""
echo "  Verify wrap cover dimensions match:"
pdfinfo "$BUILD_DIR/paperback-wrap-cover.pdf" | grep -E "Page size"
echo ""
echo "  If the wrap cover width does not match the required width above,"
echo "  edit assets/svg/cover-wrap.svg to update the spine width to ${SPINE}\""
echo "  and re-run this script."
