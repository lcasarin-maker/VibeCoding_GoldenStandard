import yaml, re
from pathlib import Path

p = Path('golden_standard_principles.yaml')
data = yaml.safe_load(p.read_text(encoding='utf-8'))
items = data.get('items', [])

boilerplate_pattern = re.compile(
    r"Behavioral/doctrinal vice\s*[-–—]\s*not statically falsifiable in a generic way\.\s*"
    r"Documented in the Golden Standard catalogs as governance knowledge;\s*"
    r"no automated test can discriminate this without human semantic judgment\.\s*"
    r"Sprint 3\.4 triage:\s*reclassified from [^\n]+ to DOC_ONLY\.",
    re.IGNORECASE | re.DOTALL
)

for item in items:
    action = item.get('action', '')
    if boilerplate_pattern.search(action):
        title = item.get('title', '')
        symptom = item.get('symptom', '')
        cause = item.get('cause', '')
        solution = item.get('solution', '')
        new_action = f"""This principle addresses {symptom}. Root cause: {cause}. Remediation: {solution}. It is a behavioral/doctrinal guideline — not statically falsifiable without human semantic judgment."""
        item['action'] = new_action

# Also depure language: replace absolutes in action/solution
for item in items:
    for key in ['action', 'solution', 'symptom', 'cause']:
        text = item.get(key, '')
        if not isinstance(text, str):
            continue
        # Replace only standalone absolutes, not inside words
        text = re.sub(r'\ball\b', 'every', text, flags=re.IGNORECASE)
        text = re.sub(r'\bmust\b', 'should', text, flags=re.IGNORECASE)
        text = re.sub(r'\bnever\b', 'avoid', text, flags=re.IGNORECASE)
        item[key] = text

p.write_text(
    yaml.dump(data, allow_unicode=True, sort_keys=False, default_flow_style=False, width=120),
    encoding='utf-8'
)
print(f'Rewrote {len(items)} principle entries: boilerplate replaced, absolutes depured')
