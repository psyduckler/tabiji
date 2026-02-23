#!/usr/bin/env python3
"""
Optimize winning images to 800px JPEG and update HTML files with img tags.
"""
import os, re, shutil
from pathlib import Path
from PIL import Image

BASE = Path('/Users/psy/.openclaw/workspace/tabiji/popular-picks')

# All winners: (page_slug, rest_slug, candidate_num, alt_text)
WINNERS = {
    'oaxaca-mole': [
        ('los-pacos', 1, 'Los Pacos mole degustation Oaxaca Mexico'),
        ('mo-kalli', 4, 'Mo-Kalli mole restaurant Tlacolula Oaxaca'),
        ('el-sabor-antequera', 3, 'El Sabor de Antequera mole buffet Oaxaca'),
        ('casa-oaxaca', 2, 'Casa Oaxaca restaurant courtyard Oaxaca'),
        ('el-naranjo', 3, 'El Naranjo mole enchiladas Oaxaca'),
        ('mercado-20', 1, 'Mercado 20 de Noviembre Oaxaca market'),
        ('la-olla', 1, 'La Olla mole negro Oaxaca'),
        ('pitiona', 5, 'Pitiona fine dining Oaxaca'),
        ('casa-crespo', 4, 'Casa Crespo cooking school mole Oaxaca'),
        ('la-biznaga', 5, 'La Biznaga mezcal and mole Oaxaca'),
        ('el-topil', 2, 'El Topil memelas mole negro Oaxaca street food'),
        ('zandunga', 1, 'Zandunga courtyard restaurant Oaxaca'),
        ('itanoni', 3, 'Itanoni tortilleria heirloom corn Oaxaca'),
        ('el-jardin', 3, 'El Jardin del Zocalo tamales Oaxaca'),
        ('casa-mook', 3, 'Casa Mook modern indigenous restaurant Oaxaca'),
    ],
    'bangkok-mango-sticky-rice': [
        ('mae-varee', 5, 'Mae Varee mango sticky rice Bangkok Thong Lo'),
        ('or-tor-kor', 5, 'Or Tor Kor Market Bangkok Thai produce'),
        ('after-you', 5, 'After You dessert cafe mango sticky rice Bangkok'),
        ('nang-loeng', 2, 'Nang Loeng Market Bangkok historic'),
        ('chatuchak', 1, 'Chatuchak Weekend Market Bangkok street food'),
        ('jay-dee', 4, 'Jay Dee mango sticky rice vendor Bangkok Silom'),
        ('krua-apsorn', 1, 'Krua Apsorn restaurant Bangkok'),
        ('baan-ying', 3, 'Baan Ying restaurant Bangkok Thai home cooking'),
        ('yaowarat', 2, 'Yaowarat Chinatown Bangkok night market'),
        ('the-local', 4, 'The Local Restaurant Bangkok heritage Thai house'),
        ('mango-tango', 1, 'Mango Tango dessert cafe Bangkok mango'),
        ('wanlop', 2, 'Wanlop mango stall Sukhumvit Soi 38 Bangkok night'),
        ('pak-khlong', 4, 'Pak Khlong Talat flower market Bangkok'),
        ('nahm', 1, 'Nahm restaurant Bangkok Michelin Thai cuisine'),
        ('khao-san', 1, 'Khao San Road Bangkok backpacker night market'),
    ],
    'bangkok-rooftop-pools': [
        ('so-bangkok', 4, 'SO Bangkok hotel rooftop infinity pool Lumphini Park'),
        ('137-pillars', 1, '137 Pillars Bangkok rooftop infinity pool skyline'),
        ('park-hyatt', 1, 'Park Hyatt Bangkok rooftop pool skyline'),
        ('avani-riverside', 1, 'AVANI Riverside Bangkok rooftop pool Chao Phraya'),
        ('sindhorn-midtown', 1, 'Sindhorn Midtown Bangkok rooftop infinity pool'),
        ('eastin-grand', 1, 'Eastin Grand Sathorn Bangkok infinity pool twilight'),
        ('okura-prestige', 5, 'Okura Prestige Bangkok cantilevered rooftop pool'),
        ('novotel-sukhumvit', 5, 'Novotel Sukhumvit Bangkok rooftop infinity pool'),
        ('hotel-muse', 2, 'Hotel Muse Bangkok Speakeasy rooftop bar blue hour'),
        ('kimpton-maalai', 1, 'Kimpton Maa-Lai Bangkok tropical garden pool'),
        ('hilton-sukhumvit', 2, 'Hilton Sukhumvit Bangkok rooftop pool twilight'),
        ('dusit-thani', 2, 'Dusit Thani Bangkok infinity pool Lumphini'),
        ('grand-mercure', 1, 'Grand Mercure Bangkok Atrium rooftop pool'),
        ('innside-melia', 2, 'INNSiDE Melia Bangkok rooftop pool twilight'),
        ('siam-at-siam', 4, 'Siam at Siam Bangkok design hotel pool BTS'),
        ('mode-sathorn', 3, 'Mode Sathorn Hotel Bangkok rooftop pool Sathorn'),
    ],
}

# Section IDs in HTML files (for finding insertion points)
SECTION_IDS = {
    'oaxaca-mole': {
        'los-pacos': 'los-pacos', 'mo-kalli': 'mo-kalli', 
        'el-sabor-antequera': 'el-sabor-antequera', 'casa-oaxaca': 'casa-oaxaca',
        'el-naranjo': 'el-naranjo', 'mercado-20': 'mercado-20',
        'la-olla': 'la-olla', 'pitiona': 'pitiona',
        'casa-crespo': 'casa-crespo', 'la-biznaga': 'la-biznaga',
        'el-topil': 'el-topil', 'zandunga': 'zandunga',
        'itanoni': 'itanoni', 'el-jardin': 'el-jardin',
        'casa-mook': 'casa-mook',
    },
    'bangkok-mango-sticky-rice': {
        'mae-varee': 'mae-varee', 'or-tor-kor': 'or-tor-kor',
        'after-you': 'after-you', 'nang-loeng': 'nang-loeng',
        'chatuchak': 'chatuchak', 'jay-dee': 'jay-dee',
        'krua-apsorn': 'krua-apsorn', 'baan-ying': 'baan-ying',
        'yaowarat': 'yaowarat', 'the-local': 'the-local',
        'mango-tango': 'mango-tango', 'wanlop': 'wanlop',
        'pak-khlong': 'pak-khlong', 'nahm': 'nahm',
        'khao-san': 'khao-san',
    },
    'bangkok-rooftop-pools': {
        'so-bangkok': 'so-bangkok', '137-pillars': '137-pillars',
        'park-hyatt': 'park-hyatt', 'avani-riverside': 'avani-riverside',
        'sindhorn-midtown': 'sindhorn-midtown', 'eastin-grand': 'eastin-grand',
        'okura-prestige': 'okura-prestige', 'novotel-sukhumvit': 'novotel-sukhumvit',
        'hotel-muse': 'hotel-muse', 'kimpton-maalai': 'kimpton-maalai',
        'hilton-sukhumvit': 'hilton-sukhumvit', 'dusit-thani': 'dusit-thani',
        'grand-mercure': 'grand-mercure', 'innside-melia': 'innside-melia',
        'siam-at-siam': 'siam-at-siam', 'mode-sathorn': 'mode-sathorn',
    },
}

def optimize_image(src_path, dest_path, max_width=800, quality=82):
    """Optimize image: resize to max_width, save as JPEG at given quality."""
    try:
        with Image.open(src_path) as img:
            # Convert to RGB (handle RGBA, P, etc.)
            if img.mode in ('RGBA', 'P', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                if 'A' in img.mode:
                    background.paste(img, mask=img.split()[-1])
                else:
                    background.paste(img)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize if wider than max_width
            w, h = img.size
            if w > max_width:
                new_h = int(h * max_width / w)
                img = img.resize((max_width, new_h), Image.LANCZOS)
            
            # Save as JPEG
            img.save(dest_path, 'JPEG', quality=quality, optimize=True)
            return os.path.getsize(dest_path)
    except Exception as e:
        print(f"    ❌ Error optimizing {src_path}: {e}")
        return 0

def insert_img_tag(html_content, section_id, img_filename, alt_text):
    """Insert img tag in the restaurant section, after restaurant-details, before what-to-order."""
    # Find the section
    section_start = html_content.find(f'id="{section_id}"')
    if section_start == -1:
        print(f"    ❌ Section id={section_id} not found")
        return html_content
    
    # Check if img with this filename already exists in this section
    section_chunk_check = html_content[section_start:section_start + 4000]
    if f'src="{img_filename}"' in section_chunk_check:
        print(f"    ✅ Already has img tag for {img_filename}")
        return html_content
    
    # Find the what-to-order div within this section (first occurrence)
    wto_marker = '    <div class="what-to-order">'
    wto_pos = html_content.find(wto_marker, section_start)
    if wto_pos == -1:
        print(f"    ❌ Could not find what-to-order in section {section_id}")
        return html_content
    
    # Build img tag to insert
    img_tag = f'    <img src="{img_filename}" alt="{alt_text}" loading="lazy" style="width:100%;max-height:420px;object-fit:cover;border-radius:10px;margin-bottom:1rem;">\n'
    
    # Insert just before the what-to-order div
    new_html = html_content[:wto_pos] + img_tag + html_content[wto_pos:]
    print(f"    ✅ Inserted img tag for {section_id}")
    return new_html

def process_page(page_slug):
    """Process all restaurants for a page."""
    page_dir = BASE / page_slug
    html_path = page_dir / 'index.html'
    tmp_dir = BASE / f'tmp-{page_slug}'
    
    print(f"\n{'='*60}")
    print(f"Processing: {page_slug}")
    print(f"{'='*60}")
    
    # Read HTML
    html = html_path.read_text(encoding='utf-8')
    added_count = 0
    
    for rest_slug, candidate_num, alt_text in WINNERS[page_slug]:
        img_filename = f"{rest_slug}.jpg"
        dest_path = page_dir / img_filename
        
        # Skip if already exists > 1KB
        if dest_path.exists() and dest_path.stat().st_size > 1024:
            print(f"  ✅ SKIP {rest_slug} (exists: {dest_path.stat().st_size//1024}KB)")
            # Still update HTML if img tag missing
            section_id = SECTION_IDS[page_slug].get(rest_slug, rest_slug)
            html = insert_img_tag(html, section_id, img_filename, alt_text)
            continue
        
        # Find the source candidate
        src_path = tmp_dir / rest_slug / f"candidate_{candidate_num}.jpg"
        if not src_path.exists():
            # Try other numbers
            print(f"  ⚠️  {rest_slug}: candidate_{candidate_num}.jpg missing, trying others...")
            for n in range(1, 6):
                alt_src = tmp_dir / rest_slug / f"candidate_{n}.jpg"
                if alt_src.exists():
                    src_path = alt_src
                    print(f"     Using candidate_{n} instead")
                    break
        
        if not src_path.exists():
            print(f"  ❌ {rest_slug}: No candidates found!")
            continue
        
        # Optimize
        size = optimize_image(str(src_path), str(dest_path))
        if size > 0:
            print(f"  ✅ {rest_slug}: {src_path.name} → {img_filename} ({size//1024}KB)")
            added_count += 1
        else:
            print(f"  ❌ {rest_slug}: optimization failed")
            if dest_path.exists():
                dest_path.unlink()
            continue
        
        # Insert img tag in HTML
        section_id = SECTION_IDS[page_slug].get(rest_slug, rest_slug)
        html = insert_img_tag(html, section_id, img_filename, alt_text)
    
    # Write updated HTML
    html_path.write_text(html, encoding='utf-8')
    print(f"\n  📝 HTML updated for {page_slug}")
    print(f"  Photos added: {added_count}")
    return added_count

# Process all three pages
results = {}
for page_slug in ['oaxaca-mole', 'bangkok-mango-sticky-rice', 'bangkok-rooftop-pools']:
    results[page_slug] = process_page(page_slug)

print(f"\n{'='*60}")
print("SUMMARY")
print(f"{'='*60}")
for page, count in results.items():
    print(f"  {page}: {count} photos added/processed")
