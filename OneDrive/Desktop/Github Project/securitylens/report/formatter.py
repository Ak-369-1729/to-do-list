"""Generate a human-readable Markdown report from check results."""
from datetime import datetime
from typing import List, Dict, Any


def _risk_label(risk: str) -> str:
    return risk.upper() if risk else 'LOW'


def _format_finding(f: Dict[str, Any]) -> str:
    risk = _risk_label(f.get('risk', 'LOW'))
    desc = f.get('description', 'No description')
    rec = f.get('recommendation', '')
    return f"- **Finding:** {desc}\n  - **Risk:** {risk}\n  - **Recommendation:** {rec}\n"


def generate_report(results: List[Dict[str, Any]], generated_at: datetime = None) -> str:
    gen = generated_at or datetime.utcnow()
    lines = []
    lines.append('# SecurityLens System Audit')
    lines.append(f'*Generated (UTC): {gen.isoformat()}*')
    lines.append('')
    lines.append('## Summary')
    lines.append('This report summarizes local, non-invasive system checks. It explains potential security concerns in plain English and gives actionable recommendations. No raw logs are shown in this report.')
    lines.append('')

    for res in results:
        name = res.get('name', 'unknown')
        lines.append(f'---')
        lines.append(f'### {name.replace("_", " ").title()}')
        if not res.get('supported', True):
            lines.append(f'*Status:* Not supported on this system. {res.get("explanation", "")}')
            lines.append('')
            continue

        if 'error' in res:
            lines.append(f'*Status:* Error - {res.get("error")}')
            lines.append('')
            continue

        findings = res.get('findings', [])
        lines.append(f'*Findings:* {len(findings)}')
        lines.append('')
        for f in findings:
            lines.append(_format_finding(f))

    lines.append('---')
    lines.append('## Final Notes')
    lines.append('- **Privacy:** All checks run locally; the tool does not transmit data off this machine.')
    lines.append('- **Non-destructive:** SecurityLens does not perform exploitation or automated remediation.')
    lines.append('- **Next steps:** Investigate HIGH or unexpected findings, and consult a professional if unsure.')

    return '\n'.join(lines)
