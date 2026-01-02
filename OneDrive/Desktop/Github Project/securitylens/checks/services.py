"""Running services check using systemctl, with graceful fallback."""
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


def _parse_systemctl(output: str) -> List[Dict[str, str]]:
    lines = [l for l in output.splitlines() if l.strip()]
    services = []
    for line in lines[1:]:
        parts = line.split()
        if parts:
            services.append({'raw': line})
    return services


def run() -> Dict[str, Any]:
    if not shutil.which('systemctl'):
        return {
            'name': 'services',
            'supported': False,
            'explanation': 'systemctl not available on this system (non-systemd).',
            'findings': [],
        }

    cmd = ['systemctl', 'list-units', '--type=service', '--state=running', '--no-pager', '--no-legend']
    raw, code, err = _run_command(cmd)
    if code != 0:
        return {
            'name': 'services',
            'supported': True,
            'error': err or 'Unknown error running systemctl',
            'findings': [],
        }

    parsed = _parse_systemctl(raw)
    findings = []
    for s in parsed:
        findings.append({
            'description': f"Running service: {s['raw']}",
            'risk': 'LOW',
            'recommendation': 'Confirm the service is expected; disable if unnecessary.'
        })

    if not findings:
        findings.append({
            'description': 'No running systemd services detected.',
            'risk': 'LOW',
            'recommendation': 'No action needed.'
        })

    return {
        'name': 'services',
        'supported': True,
        'summary_count': len(parsed),
        'findings': findings,
    }
