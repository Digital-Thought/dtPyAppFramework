# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [4.1.1] - 2026-01-31

### Added

- Add multi-process file locking and atomic writes to local keystore (v4.0.1)
  Implemented thread-safe access to the local secrets store for containerised
- Add container-specific paths for temp and logging in CONTAINER_MODE
  Implemented container-aware path management to support multiple containers
- Add --password command-line argument to set KEYSTORE_PASSWORD
  Added a new --password / -p command-line argument that sets the
- Add sample applications for keystore features
  - password_keystore: Demonstrates --password argument and portable keystores
- Add separate process workers to concurrent_keystore sample
  Restructured concurrent_keystore sample to run each worker as a
- Address all SonarQube issues across source, tests, and samples
  Fix 2 blockers: remove extra self argument in _add_secret_file call,
- Add sample data and logs directories to .gitignore
  Ignore runtime-generated data/ and logs/ directories under samples/
- Add CHANGELOG.md for version 4.1.1

### Changed

- Initial commit
- Bumped to 4.0.0
- Bumped to 4.0.0
- Bumped to 4.0.0
- Bump to v4.0.1
- Merge pull request #1 from Digital-Thought/local-secrets-multiprocess
  Local secrets multiprocess
- Improve application shutdown handling with auto-exit and wait_for_shutdown
  Redesigned the application lifecycle to support two patterns:
- Bump to v4.0.2
- Bump to v4.0.2
- Merge pull request #2 from Digital-Thought/container-changes
  Container changes
- Use KEYSTORE_PASSWORD directly in container mode without system fingerprint
  In CONTAINER_MODE, the keystore password is now used directly from the
- Bump to v4.0.3 with changelog update
  - Move keystore password changes to new 4.0.3 section
- Merge pull request #3 from Digital-Thought/HMAC-Container-Change
  Hmac container change
- Use matching short_name for password_keystore samples
  Both create_keystore.py and access_keystore.py now use
- [RELEASE] Bump version to 4.1.0
  Add AppContext singleton facade, metadata auto-discovery from text files,
- Merge pull request #4 from Digital-Thought/HMAC-Container-Change
  Hmac container change
- Bump azure-core and filelock to address security vulnerabilities
  - azure-core: 1.32.0 → 1.38.0 (fixes deserialization of untrusted data, HIGH)
- [RELEASE] Bump version to 4.1.1
  Security and code quality release addressing all SonarQube findings:
- Clean artifacts from sample runs.

### Removed

- Removed deprecated versions of the artifact actions

### Fixed

- Fix keystore path references in sample applications
  Changed ApplicationPaths().keystore_root_path to
- Fix empty secret key validation errors (v4.0.4)
  Added defensive checks to prevent SecurityValidationError when empty
- Fix test failures, source bugs, and update documentation
  Fix 38 failing CI tests across 6 test files: correct singleton
- fix: Correct test failures and InputValidator import path
  Fix relative import in secret_store.py from `..security.validation` to
- Fix remaining SonarQube issues across source, tests, and samples
  Source fixes:
- fix: Remove redundant exception handling and resolve SonarQube false positive
  - Remove redundant try/except block in keystore.py that caught exceptions
- fix: Increase PBKDF2 iteration count to 100,000 for password strengthening
  Increase iterations in _strengthen_user_password from 50,000 to 100,000


