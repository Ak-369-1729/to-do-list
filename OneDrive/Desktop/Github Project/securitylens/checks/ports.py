"""Open ports check using system utilities.

This module runs `ss -tuln` or `netstat -tuln` to detect listening TCP/UDP ports.
It returns structured data but never exposes raw logs directly in reports.
"""
import shutil
import subprocess
from typing import Dict, Any


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


def _parse_ss_output(output: str):
    lines = [l for l in output.splitlines() if l.strip()]
    ports = []
    for line in lines[1:]:
        parts = line.split()
        if len(parts) >= 5:
            proto = parts[0]
            local = parts[4]
            ports.append({'proto': proto, 'local': local})
    return ports


def run() -> Dict[str, Any]:
    # Prefer ss, fallback to netstat
    if shutil.which('ss'):
        cmd = ['ss', '-tuln']
        tool = 'ss'
    elif shutil.which('netstat'):
        cmd = ['netstat', '-tuln']
        tool = 'netstat'
    else:
        return {
            'name': 'open_ports',
            'supported': False,
            'explanation': 'No ss or netstat command found on system.',
            'findings': [],
        }

    raw, code, err = _run_command(cmd)

    if code != 0:
        return {
            'name': 'open_ports',
            'supported': True,
            'tool': tool,
            'error': err or 'Unknown error while running command',
            'findings': [],
        }

    parsed = _parse_ss_output(raw)

    # Summarize findings without raw logs
    findings = []
    for p in parsed:
        findings.append({
            'description': f"Listening {p['proto']} on {p['local']}",
            'risk': 'LOW',
            'recommendation': 'If this service is unexpected, investigate the owning process and consider firewalling or stopping it.'
        })

    if not findings:
        findings.append({
            'description': 'No listening TCP/UDP ports detected by the available tool.',
            'risk': 'LOW',
            'recommendation': 'No action needed unless you expect services to be running.'
        })

    return {
        'name': 'open_ports',
        'supported': True,
        'tool': tool,
        'summary_count': len(parsed),
        'findings': findings,
    }
