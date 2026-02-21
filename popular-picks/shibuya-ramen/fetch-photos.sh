#!/bin/bash
# Fetch top 5 Google Images candidates for each restaurant
set -e
cd "$(dirname "$0")"
SERPAPI_KEY=$(security find-generic-password -s serpapi-key -w)
mkdir -p candidates

declare -A QUERIES
QUERIES=(
  ["kamo-to-negi"]="Kamo to Negi 鴨to葱 Shibuya ramen"
  ["fuunji"]="Fuunji 風雲児 tsukemen Tokyo"
  ["oreryu-shio-ramen"]="Oreryu Shio Ramen 俺流塩らーめん Shibuya"
  ["ramen-tatsunoya"]="Ramen Tatsunoya 龍の家 Shibuya"
  ["afuri-shibuya"]="AFURI ramen Shibuya yuzu shio"
  ["menya-musashi"]="Menya Musashi 麺屋武蔵 Shibuya ramen"
  ["tsuta"]="Tsuta 蔦 ramen Yoyogi-Uehara"
  ["mammoth"]="Mammoth マンモス tsukemen Shibuya"
  ["hayashi"]="Hayashi はやし ramen Shibuya"
  ["tonari"]="Tonari 東南 tanmen Shibuya"
  ["ramen-nagi"]="Ramen Nagi ラーメン凪 Shibuya niboshi"
  ["sakurazaka"]="Sakurazaka 桜坂 ramen Shibuya tonkotsu"
  ["jikasei-mensho"]="Jikasei Mensho 自家製麺 ramen Shibuya"
  ["ichiran-shibuya"]="Ichiran 一蘭 Shibuya ramen"
  ["soranoiro"]="Soranoiro ソラノイロ ramen vegan Tokyo"
  ["kiraku"]="Kiraku 喜楽 ramen Shibuya"
  ["ippudo-shibuya"]="Ippudo 一風堂 Shibuya ramen"
  ["junteuchi-men-to-mirai"]="Junteuchi Men to Mirai 純手打ち 麺と未来 Shimokitazawa"
)

for slug in "${!QUERIES[@]}"; do
  query="${QUERIES[$slug]}"
  dir="candidates/$slug"
  
  # Skip if already have the final photo
  if [ -f "${slug}.jpg" ] && [ $(stat -f%z "${slug}.jpg" 2>/dev/null || echo 0) -gt 1024 ]; then
    echo "SKIP $slug — already has photo"
    continue
  fi
  
  mkdir -p "$dir"
  echo "SEARCH: $slug — $query"
  
  # URL-encode query
  encoded=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$query'))")
  
  # Search Google Images via SerpAPI
  curl -s "https://serpapi.com/search.json?engine=google_images&q=${encoded}&api_key=${SERPAPI_KEY}&num=8" > "$dir/results.json"
  
  # Extract top 5 image URLs
  python3 -c "
import json, sys
with open('$dir/results.json') as f:
    data = json.load(f)
results = data.get('images_results', [])[:5]
for i, r in enumerate(results):
    print(r.get('original', ''))
" > "$dir/urls.txt"
  
  # Download each
  i=0
  while IFS= read -r url; do
    if [ -z "$url" ]; then continue; fi
    i=$((i+1))
    curl -sL --max-time 10 -o "$dir/photo_${i}.jpg" "$url" 2>/dev/null || true
    size=$(stat -f%z "$dir/photo_${i}.jpg" 2>/dev/null || echo 0)
    if [ "$size" -lt 10000 ]; then
      rm -f "$dir/photo_${i}.jpg"
      echo "  photo_${i}: too small ($size bytes), removed"
    else
      echo "  photo_${i}: ${size} bytes OK"
    fi
  done < "$dir/urls.txt"
  
  echo "---"
  sleep 1
done

echo "DONE fetching candidates"
