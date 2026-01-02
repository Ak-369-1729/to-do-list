"""System update status check using apt (non-invasive)."""
import shutil
import subprocess
from typing import Dict, Any, List


def _run_command(cmd):
    try:
        completed = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=False,
            check=False,
        )
        return completed.stdout.strip(), completed.returncode, completed.stderr.strip()
    except Exception as e:
        return '', 1, str(e)


def _parse_apt(output: str) -> List[str]:
    lines = [l for l in output.splitlines() if l.strip()]
    pkgs = []
    for line in lines:
        if '/' in line:
            pkgs.append(line)
    return pkgs


def run() -> Dict[str, Any]:
    if not shutil.which('apt'):
        return {
            'name': 'updates',
            'supported': False,
            'explanation': 'apt not found on system; cannot check package updates.',
            'findings': [],
        }

    cmd = ['apt', 'list', '--upgradable']
    raw, code, err = _run_command(cmd)
    if code != 0:
        return {
            'name': 'updates',
            'supported': True,
            'error': err or 'Error running apt list --upgradable',
            'findings': [],
        }

    parsed = _parse_apt(raw)
    findings = []
    if parsed:
        for p in parsed:
            findings.append({
                'description': f'Upgradable package: {p}',
                'risk': 'LOW',
                'recommendation': 'Review package change and apply updates via your package manager.'
            })
    else:
        findings.append({
            'description': 'No upgradable packages reported by apt.',
            'risk': 'LOW',
            'recommendation': 'System packages appear up-to-date according to apt.'
        })

    return {
        'name': 'updates',
        'supported': True,
        'summary_count': len(parsed),
        'findings': findings,
    }
