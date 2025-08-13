# Security Policy

## Supported Versions
Active work occurs on `main`. Security fixes will be released as patch versions.

## Reporting a Vulnerability
Please email **security@circlegroup.au** (or your preferred security inbox). Include:
- A description of the issue and where it was found
- Steps to reproduce / PoC
- Impact assessment (what could an attacker do)
- Any logs or screenshots

We will acknowledge receipt within **48 hours**, provide a timeline, and keep you updated until resolution. Please **do not** create public issues for security reports.

## Disclosure
We request **90-day coordinated disclosure** by default. If exploitation is observed in the wild, we may accelerate the timeline.

## Secrets & Keys
Never commit secrets (API keys, tokens, `.env`, database files, encryption keys). Use environment variables or secret managers. The repository is configured to ignore common secret files; CI will block new leaks where possible.

## Transport & Storage
- Prefer HTTPS for all external APIs.
- Encrypt sensitive at-rest configuration with Fernet or use cloud secret managers.
- Practice least-privilege for tokens/scopes.
