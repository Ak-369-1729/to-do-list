#!/usr/bin/env python3
"""SecurityLens - entry point for the local system security audit tool.

Run with:
    python securitylens.py

This script runs a set of local, non-invasive checks and writes a
human-readable report to `sample-report.md`.
"""
import os
from datetime import datetime

from checks import ports, permissions, services, updates
from report.formatter import generate_report


def main():
    scan_dir = '/tmp'
    if not os.path.exists(scan_dir):
        scan_dir = None

    results = []
    results.append(ports.run())
    results.append(permissions.run(scan_dir or None))
    results.append(services.run())
    results.append(updates.run())

    report_text = generate_report(results, generated_at=datetime.utcnow())

    out_path = os.path.join(os.path.dirname(__file__), 'sample-report.md')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(report_text)

    print('SecurityLens audit complete.')
    print(f'Report written to: {out_path}')


if __name__ == '__main__':
    main()
