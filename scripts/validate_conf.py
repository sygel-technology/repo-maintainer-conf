#!/usr/bin/env python3
"""Protección preventiva del piloto. Validación básica; no es un dry-run del CLI."""
from pathlib import Path
import sys
import yaml

base = Path(__file__).resolve().parents[1] / 'conf'
configs = sorted(base.rglob('*.yml'))
for f in configs:
    text = f.read_text(encoding='utf-8')
    if 'PENDIENTE_' in text:
        sys.exit(f'ERROR: marcadores sin completar en {f}')
    if not isinstance(yaml.safe_load(text), dict):
        sys.exit(f'ERROR: YAML vacío o inválido {f}')

repos = {}
for f in sorted((base / 'repo').glob('*.yml')):
    repos.update(yaml.safe_load(f.read_text(encoding='utf-8')))
if set(repos) != {'sy-mass-mailing'}:
    sys.exit(f'ERROR: este piloto solo permite sy-mass-mailing, encontrados: {list(repos)}')

teams = {}
for f in sorted((base / 'psc').glob('*.yml')):
    teams.update(yaml.safe_load(f.read_text(encoding='utf-8')))

for name, repo in repos.items():
    if repo['psc'] not in teams:
        sys.exit(f'ERROR: PSC {repo["psc"]} de {name} no configurado')
    if repo.get('branches') != ['18.0']:
        sys.exit('ERROR: cambiar ramas solo después de revisar y adaptar validador del piloto')

for name, team in teams.items():
    if not team.get('members') or not team.get('representatives'):
        sys.exit(f'ERROR: miembros reales y representantes deben validarse para {name}')

global_cfg = yaml.safe_load((base / 'global.yml').read_text(encoding='utf-8'))
if not global_cfg.get('owner'):
    sys.exit('ERROR: owner sin configurar')

print('VALIDACIÓN BÁSICA CORRECTA (no garantiza ausencia de cambios de permisos).')
