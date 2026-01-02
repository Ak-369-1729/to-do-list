# SecurityLens

SecurityLens is a local, privacy-first system security audit tool aimed at helping beginners understand OS-level security posture in plain English.

**Problem solved**: Many users aren't sure how to interpret system state (open ports, permissions, running services, available updates). SecurityLens runs safe, read-only checks and explains what those findings mean and how to act.

**Why SecurityLens exists**: To provide an accessible way to learn about basic system security without performing intrusive or destructive actions.

**Who it's for**: Beginners, system administrators who want quick local checks, and educators teaching security basics.

**What it is NOT**: SecurityLens is not a penetration testing tool, does not exploit vulnerabilities, and does not collect or transmit any data.

## Privacy guarantees
- Runs entirely locally.
- No network requests or telemetry.
- Writes only a Markdown report to the local filesystem.

## How to run

From the project root run:

```bash
python securitylens/securitylens.py
```

The tool will write `sample-report.md` in the `securitylens` directory.

## Design notes
- Modular checks in `checks/`.
- Human-friendly report generation in `report/`.
- No external Python packages required.
