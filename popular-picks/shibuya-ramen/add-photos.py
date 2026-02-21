#!/usr/bin/env python3
"""Add img tags to shibuya-ramen article and prepare for photo search."""
import re

with open('index.html', 'r') as f:
    html = f.read()

# Restaurant data: (id, name, filename)
restaurants = [
    ('kamo-to-negi', 'Kamo to Negi', 'kamo-to-negi.jpg'),
    ('fuunji', 'Fuunji', 'fuunji.jpg'),
    ('oreryu', 'Oreryu Shio Ramen', 'oreryu-shio-ramen.jpg'),
    ('tatsunoya', 'Ramen Tatsunoya', 'ramen-tatsunoya.jpg'),
    ('afuri', 'AFURI Shibuya', 'afuri-shibuya.jpg'),
    ('menya-musashi', 'Menya Musashi', 'menya-musashi.jpg'),
    ('tsuta', 'Japanese Soba Noodles Tsuta', 'tsuta.jpg'),
    ('mammoth', 'Mammoth', 'mammoth.jpg'),
    ('hayashi', 'Hayashi', 'hayashi.jpg'),
    ('tonari', 'Tonari', 'tonari.jpg'),
    ('nagi', 'Ramen Nagi', 'ramen-nagi.jpg'),
    ('sakurazaka', 'Sakurazaka', 'sakurazaka.jpg'),
    ('jikasei-mensho', 'Jikasei Mensho', 'jikasei-mensho.jpg'),
    ('ichiran', 'Ichiran Shibuya', 'ichiran-shibuya.jpg'),
    ('soranoiro', 'Soranoiro', 'soranoiro.jpg'),
    ('kiraku', 'Kiraku', 'kiraku.jpg'),
    ('ippudo', 'Ippudo Shibuya', 'ippudo-shibuya.jpg'),
    ('junteuchi', 'Junteuchi Men to Mirai', 'junteuchi-men-to-mirai.jpg'),
]

# Add CSS for restaurant photos
img_css = """        .restaurant-photo {
            width: 100%; max-width: 800px;
            border-radius: 10px;
            margin-bottom: 1rem;
            aspect-ratio: 4/3;
            object-fit: cover;
        }"""

html = html.replace('        .restaurant-details {', img_css + '\n        .restaurant-details {')

# Add img tags after each what-to-order div
for rid, name, filename in restaurants:
    # Find the what-to-order closing div for this section
    section_start = html.find(f'id="{rid}"')
    if section_start == -1:
        print(f"WARNING: section {rid} not found")
        continue
    
    # Find the what-to-order div end after section start
    wo_start = html.find('<div class="what-to-order">', section_start)
    if wo_start == -1:
        print(f"WARNING: what-to-order not found for {rid}")
        continue
    wo_end = html.find('</div>', wo_start) + len('</div>')
    
    img_tag = f'\n    <img src="{filename}" alt="{name} ramen in Shibuya, Tokyo" class="restaurant-photo" width="800" height="600" loading="lazy">'
    html = html[:wo_end] + img_tag + html[wo_end:]

with open('index.html', 'w') as f:
    f.write(html)

print("Done — added img tags for all 18 restaurants")
for _, name, filename in restaurants:
    print(f"  {filename} — {name}")
