#!/usr/bin/env python3
"""Wrap vendored brand SVGs in small, readable cards for the profile README."""
from copy import deepcopy
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SVG = 'http://www.w3.org/2000/svg'
ET.register_namespace('', SVG)
ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')

def element(tag, attributes=None, text=None):
    node = ET.Element(f'{{{SVG}}}{tag}', attributes or {})
    node.text = text
    return node

DEVICON = {
    'go': 'Go', 'java': 'Java', 'spring': 'Spring', 'nodejs': 'Node.js',
    'php': 'PHP', 'laravel': 'Laravel', 'nextjs': 'Next.js', 'react': 'React',
    'javascript': 'JavaScript', 'tailwindcss': 'Tailwind CSS', 'html5': 'HTML',
    'css3': 'CSS', 'docker': 'Docker', 'amazonwebservices': 'AWS', 'git': 'Git',
    'linux': 'Linux', 'jenkins': 'Jenkins', 'bash': 'Bash',
    'postgresql': 'PostgreSQL', 'mysql': 'MySQL', 'mongodb': 'MongoDB',
    'oracle': 'Oracle',
}
LOBE = {
    'claude': ('claude-color', 'Claude'), 'codex': ('codex', 'Codex'),
    'opencode': ('opencode', 'OpenCode'), 'gemini': ('gemini-color', 'Gemini'),
    'cursor': ('cursor', 'Cursor'),
}

sources = [(key, 'devicon', key, label) for key, label in DEVICON.items()]
sources += [(key, 'lobe-icons', source, label) for key, (source, label) in LOBE.items()]

for key, library, source, label in sources:
    icon = ET.parse(ROOT / 'assets/vendor' / library / f'{source}.svg').getroot()
    for node in icon.iter():
        assert node.tag.rsplit('}', 1)[-1] not in {'script', 'foreignObject'}
        for attr, value in node.attrib.items():
            assert not attr.lower().startswith('on')
            if attr.endswith('href'):
                assert value.startswith('#'), (key, attr, value)
    card = element('svg', {'width': '104', 'height': '60', 'viewBox': '0 0 104 60', 'role': 'img', 'aria-label': label})
    card.append(element('title', text=label))
    card.append(element('rect', {'x': '0', 'y': '0', 'width': '104', 'height': '60', 'rx': '3', 'fill': '#f3eedf'}))
    artwork = deepcopy(icon)
    artwork.set('x', '38')
    artwork.set('y', '7')
    artwork.set('width', '28')
    artwork.set('height', '28')
    artwork.set('color', '#181916')
    card.append(artwork)
    card.append(element('text', {'x': '52', 'y': '51', 'text-anchor': 'middle', 'fill': '#181916', 'font-family': 'Arial,Helvetica,sans-serif', 'font-size': '12', 'font-weight': '600'}, label))
    ET.ElementTree(card).write(ROOT / 'assets/tools' / f'{key}.svg', encoding='unicode')

print(f'Built {len(sources)} self-contained logo cards.')
