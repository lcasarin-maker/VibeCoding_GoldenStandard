import yaml
from pathlib import Path

# Load catalogs
vc_data = yaml.safe_load(Path('golden_standard_coding_vices.yaml').read_text(encoding='utf-8'))
vc_items = vc_data.get('items', [])

tk_data = yaml.safe_load(Path('golden_standard_tokenomics.yaml').read_text(encoding='utf-8'))
tk_items = tk_data.get('items', [])

pi_data = yaml.safe_load(Path('golden_standard_project_insights.yaml').read_text(encoding='utf-8'))
pi_items = pi_data.get('items', [])

# Separate doctrinal vs actionable
doctrinal_vc = [i for i in vc_items if i.get('doctrinal')]
accionable_vc = [i for i in vc_items if not i.get('doctrinal')]

doctrinal_tk = [i for i in tk_items if i.get('validating_mechanism') == 'DOC_ONLY']
accionable_tk = [i for i in tk_items if i.get('validating_mechanism') != 'DOC_ONLY']

# Build principles catalog
principles = []
for item in doctrinal_vc:
    p = dict(item)
    p['catalog_source'] = 'coding_vices'
    principles.append(p)
for item in doctrinal_tk:
    p = dict(item)
    p['catalog_source'] = 'tokenomics'
    principles.append(p)
for item in pi_items:
    p = dict(item)
    p['catalog_source'] = 'project_insights'
    p['doctrinal'] = True
    principles.append(p)

principles_data = {
    'format_version': '3.0',
    'catalog_name': 'principles',
    'items': principles,
}

# Write principles catalog
Path('golden_standard_principles.yaml').write_text(
    yaml.dump(principles_data, allow_unicode=True, sort_keys=False, default_flow_style=False, width=120),
    encoding='utf-8'
)

# Update VC catalog (remove doctrinal)
vc_data['items'] = accionable_vc
Path('golden_standard_coding_vices.yaml').write_text(
    yaml.dump(vc_data, allow_unicode=True, sort_keys=False, default_flow_style=False, width=120),
    encoding='utf-8'
)

# Update TK catalog (remove doc_only)
tk_data['items'] = accionable_tk
Path('golden_standard_tokenomics.yaml').write_text(
    yaml.dump(tk_data, allow_unicode=True, sort_keys=False, default_flow_style=False, width=120),
    encoding='utf-8'
)

print(f'Created golden_standard_principles.yaml with {len(principles)} principles')
print(f'  from VC doctrinal: {len(doctrinal_vc)}')
print(f'  from TK doc_only: {len(doctrinal_tk)}')
print(f'  from PI: {len(pi_items)}')
print(f'Updated VC: {len(accionable_vc)} accionables remaining')
print(f'Updated TK: {len(accionable_tk)} accionables remaining')
