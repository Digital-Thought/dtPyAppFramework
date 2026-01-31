# Security Policy

## Supported Versions

The following table outlines which versions of dtPyAppFramework currently receive security updates.

| Version | Status |
| ------- | ------ |
| 4.0.x   | Fully supported — receives all security patches and updates |
| 3.x     | Security fixes only — critical and high-severity vulnerabilities are patched |
| 2.x and below | End of life — no longer supported or maintained |

We strongly recommend upgrading to the latest 4.0.x release to benefit from all security improvements and new features.

## Reporting a Vulnerability

If you discover a security vulnerability in dtPyAppFramework, please report it responsibly. **Do NOT create a public GitHub issue for security vulnerabilities.** Public disclosure before a fix is available puts all users at risk.

Instead, please send your report via email to:

**dev@digital-thought.org**

### What to Include in Your Report

To help us investigate and resolve the issue efficiently, please provide as much of the following information as possible:

- **Description** — A clear and concise explanation of the vulnerability, including the affected component(s).
- **Reproduction Steps** — Detailed, step-by-step instructions to reproduce the behaviour, including any relevant configuration, code snippets, or environment details.
- **Impact Assessment** — Your assessment of the potential impact, including severity (e.g. information disclosure, privilege escalation, denial of service) and any conditions required for exploitation.
- **Suggested Fix** — If you have a proposed remediation or patch, please include it. This is optional but greatly appreciated.

### Response Timeline

We are committed to addressing security reports promptly:

- **Acknowledgement** — You will receive an acknowledgement of your report within **48 hours**.
- **Status Update** — We will provide an initial assessment and status update within **5 business days** of acknowledgement.
- **Ongoing Communication** — We will keep you informed of progress throughout the remediation process.

## Disclosure Policy

We follow a **coordinated disclosure** approach:

1. The reporter submits the vulnerability privately via email.
2. Our team investigates, confirms, and develops a fix.
3. A patched version is released and documented.
4. The vulnerability is publicly disclosed after the fix is available, with credit given to the reporter (unless anonymity is requested).

We believe in recognising the contributions of security researchers. Unless you request otherwise, we will credit you by name in the release notes and CHANGELOG for any confirmed vulnerability you report.

## Security Update Process

Security fixes are released as **patch versions** (e.g. 4.0.x) and follow this process:

1. The vulnerability is triaged and prioritised based on severity.
2. A fix is developed and tested on the relevant supported branches.
3. The patched version is published to [PyPI](https://pypi.org/project/dtPyAppFramework/).
4. All security-related changes are documented in [CHANGELOG.md](https://github.com/Digital-Thought/dtPyAppFramework/blob/main/CHANGELOG.md).
5. Users are encouraged to update promptly. Where appropriate, an advisory may be published via GitHub.

## Security-Related Configuration

dtPyAppFramework includes several built-in security features that should be configured appropriately for your deployment:

- **Encrypted Keystore** — Secrets are stored in a locally encrypted keystore, protected by a derived encryption key. In container deployments, the `KEYSTORE_PASSWORD` environment variable ensures consistent encryption across shared volumes.
- **HMAC Verification** — The framework supports HMAC-based integrity verification to detect tampering of sensitive data and configuration.
- **Multi-Cloud Secrets Management** — Sensitive values can be stored and retrieved from Azure Key Vault, AWS Secrets Manager, or the local encrypted keystore, configured via `SEC/` references in `config.yaml`. This ensures secrets are never stored in plain text within configuration files.

For detailed guidance on configuring these features, refer to the [project documentation](https://github.com/Digital-Thought/dtPyAppFramework).
