import json, subprocess, os, sys

SAFETY_DIR = "api/v1/safety"
conflicts = []
for f in sorted(os.listdir(SAFETY_DIR)):
    if not f.endswith('.json'): continue
    cc = f.replace('.json','')
    
    # Get all versions
    pr_data = json.load(open(f'{SAFETY_DIR}/{f}'))
    
    try:
        enriched = json.loads(subprocess.check_output(
            ['git', 'show', f'ba69110ce:{SAFETY_DIR}/{f}'], stderr=subprocess.DEVNULL))
    except:
        enriched = None
    
    try:
        main_data = json.loads(subprocess.check_output(
            ['git', 'show', f'origin/main:{SAFETY_DIR}/{f}'], stderr=subprocess.DEVNULL))
    except:
        main_data = None
    
    if enriched is None:
        print(f'{cc}: no enriched version, keeping PR version')
        continue
    
    # Start with enriched (most complete) as base
    merged = dict(enriched)
    
    # Overlay unique PR additions:
    # 1. Scams from PR that enriched doesn't have
    pr_scams = pr_data.get('scams', [])
    enriched_scams = enriched.get('scams', [])
    enriched_scam_names = {s.get('name','').lower() for s in enriched_scams}
    new_scams = [s for s in pr_scams if s.get('name','').lower() not in enriched_scam_names]
    if new_scams:
        merged['scams'] = enriched_scams + new_scams
        print(f'{cc}: added {len(new_scams)} unique scams from PR')
    
    # 2. emergencyWorkflows from PR if enriched doesn't have it
    if not enriched.get('emergencyWorkflows') and pr_data.get('emergencyWorkflows'):
        merged['emergencyWorkflows'] = pr_data['emergencyWorkflows']
        print(f'{cc}: added emergencyWorkflows from PR')
    
    # 3. sectionFreshness from PR if enriched doesn't have it
    if not enriched.get('sectionFreshness') and pr_data.get('sectionFreshness'):
        merged['sectionFreshness'] = pr_data['sectionFreshness']
        print(f'{cc}: added sectionFreshness from PR')
    
    # Write merged version
    with open(f'{SAFETY_DIR}/{f}', 'w') as fh:
        json.dump(merged, fh, indent=2, ensure_ascii=False)
        fh.write('\n')
    
    # Count changes
    if merged != pr_data:
        conflicts.append(cc)

print(f'\nTotal files updated: {len(conflicts)}')
