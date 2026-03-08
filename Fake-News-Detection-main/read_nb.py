import json
nb = json.load(open('Fake News Detection.ipynb', 'r', encoding='utf-8'))
cells = [c for c in nb['cells'] if c['cell_type'] == 'code']
for i, c in enumerate(cells[:10]):
    print(f"--- CELL {i} ---")
    print(''.join(c['source']))
    print()
