"""File permissions check: scan a safe directory for world-writable files."""
import os
from typing import Dict, Any, List


def _scan_dir(path: str) -> List[Dict[str, str]]:
    results = []
    for root, dirs, files in os.walk(path, onerror=lambda e: None):
        for name in files:
            full = os.path.join(root, name)
            try:
                mode = os.stat(full).st_mode
            except Exception:
                continue
            # world-writable check
            if mode & 0o002:
                results.append({'path': full})
    return results


def run(scan_path: str = None) -> Dict[str, Any]:
    if not scan_path:
        return {
            'name': 'permissions',
            'supported': True,
            'explanation': 'Default /tmp not available on this system; no scan performed.',
            'findings': [],
        }

    if not os.path.isdir(scan_path):
        return {
            'name': 'permissions',
            'supported': True,
            'explanation': f"Scan path {scan_path} is not a directory.",
            'findings': [],
        }

    try:
        world_writable = _scan_dir(scan_path)
    except Exception as e:
        return {
            'name': 'permissions',
            'supported': True,
            'error': str(e),
            'findings': [],
        }

    findings = []
    for item in world_writable:
        findings.append({
            'description': f"World-writable file: {item['path']}",
            'risk': 'MEDIUM',
            'recommendation': 'Restrict permissions with `chmod o-w <file>` or move sensitive files to a safer location.'
        })

    if not findings:
        findings.append({
            'description': f'No world-writable files found under {scan_path}.',
            'risk': 'LOW',
            'recommendation': 'No action needed.'
        })

    return {
        'name': 'permissions',
        'supported': True,
        'scanned_path': scan_path,
        'summary_count': len(world_writable),
        'findings': findings,
    }
