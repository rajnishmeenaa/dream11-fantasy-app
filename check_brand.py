import urllib.request
import json

base = 'http://localhost:8000'

# Test manifest
manifest = json.loads(urllib.request.urlopen(f'{base}/manifest.json').read().decode('utf-8'))
print('Manifest Name:', manifest['name'], '| Short Name:', manifest['short_name'])

# Test index.html title
html = urllib.request.urlopen(f'{base}/index.html').read().decode('utf-8')
for line in html.splitlines():
    if '<title>' in line or 'brand-text' in line or 'brand-d' in line:
        print('Branding:', line.strip())
