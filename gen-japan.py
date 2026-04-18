#!/usr/bin/env python3
"""Generate the Japan itinerary fulfillment script."""

def build_day(num, date, title, desc, neighborhoods, blocks, pins):
    pins_str = ",\n        ".join(
        f"{{ lat: {p['lat']}, lng: {p['lng']}, label: '{p['label']}', num: {p['num']}, cat: '{p['cat']}', desc: '{p['desc']}' }}"
        for p in pins
    )
    blocks_str = []
    for b in blocks:
        acts = b.get('activities', [])
        meals = b.get('meals', [])
        tips = b.get('tips', [])
        
        act_strs = []
        for a in acts:
            dets = ",\n              ".join(f"'{d}'" for d in a.get('details', []))
            act_strs.append(f"""            {{
              title: '{a['title']}',
              description: '{a['description']}',
              details: [{dets}]
            }}""")
        act_block = ",\n".join(act_strs)
        
        meal_strs = []
        for m in meals:
            meal_strs.append(f"""          {{
              type: '{m['type']}',
              name: '{m['name']}',
              description: '{m['description']}',
              meta: '{m.get('meta', '')}'
            }}""")
        meal_block = ",\n".join(meal_strs)
        
        tip_strs = []
        for t in tips:
            tip_strs.append(f"{{ type: '{t.get('type', 'tip')}', text: '{t['text']}' }}")
        tip_block = ",\n            ".join(tip_strs)
        
        blocks_str.append(f"""        {{
          label: '{b['label']}',
          activities: [
{act_block}
          ],
          meals: [
{male_block}
          ],
          tips: [
            {tip_block}
          ]
        }}""")
    
    blocks_final = ",\n".join(blocks_str)
    
    return f"""    {{
      num: {num},
      date: '{date}',
      title: '{title}',
      description: '{desc}',
      neighborhoods: '{neighborhoods}',
      timeBlocks: [
{blocks_final}
      ],
      mapPins: [
        {pins_str}
      ]
    }}"""

# Simplified approach: just write the JS file directly
js = open('/Users/psy/.openclaw/workspace/tabiji/scripts/fulfill-order_1776178142375_dvmst2.js', 'r').read()
print(f"Current file length: {len(js)}")
print(f"Days covered so far: {js.count('num: ')}")
