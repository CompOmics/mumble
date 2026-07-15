# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-07-15

### Changed
- Cache directory now uses `platformdirs` for a proper user cache location instead of a hardcoded path.
- Simplified and optimized the `localize_mass_shift` caching logic: per-modification results are now cached and shared across combinations instead of being recomputed for every combination, and a stale recursive check that never actually recursed was removed.
- Bumped minimum `rustyms` version to 0.10.0.
- Marked the project as beta software in the README and package classifiers.
- Various small packaging and bug fixes (argument handling in `PSMHandler`, `.gitignore`, README clarifications).

[0.3.0]: https://github.com/CompOmics/mumble/releases/tag/0.3.0
