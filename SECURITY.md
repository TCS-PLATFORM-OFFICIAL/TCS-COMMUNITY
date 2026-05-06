# Security Policy

## 🔒 Reporting a Vulnerability

If you discover a security vulnerability in `tcs-macro-pulse`, please report it
**privately** so we can fix it before disclosure.

### How to report

- **Preferred**: Open a [private security advisory](https://github.com/TCS-PLATFORM-OFFICIAL/TCS-COMMUNITY/security/advisories/new) on GitHub.
- **Alternative**: Email `security@tcs-platform.com` (PGP key on request).

Please include:
1. A description of the vulnerability and its potential impact.
2. Steps to reproduce (proof of concept appreciated).
3. Affected version (`tcs-macro-pulse` version + Python version + OS).
4. Any suggested mitigation.

### What to expect

- **Acknowledgement** within 72 hours.
- **Triage + initial assessment** within 7 days.
- **Patch + coordinated disclosure** within 30 days for critical issues.
- Credit (if you wish) in the release notes and `SECURITY.md` Hall of Fame.

## 🛡️ Scope

In scope:
- All code under `tcs_macro_pulse/`
- `examples/` (informational, but reproducible exploits welcome)
- Build artifacts on PyPI (when published)

Out of scope:
- The proprietary TCS-PLATFORM SaaS (separate disclosure channel: `security@tcs-platform.com`)
- Third-party data sources (FRED, GDACS, ACLED) — please report directly to them
- Vulnerabilities in dependencies — please report upstream first; we'll coordinate

## 🚫 Please do NOT

- Publicly disclose the vulnerability before we've had a chance to patch.
- Test against production TCS-PLATFORM systems without prior written authorization.
- Use any vulnerability you find to access data you do not own.

## 📜 Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | ✅ Yes              |
| < 0.1   | ❌ No (pre-release) |

Thank you for helping keep `tcs-macro-pulse` and its users safe.
