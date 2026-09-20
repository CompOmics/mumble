# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `include_mumble_decoys` option (default `false`): for every single-modification candidate,
  also generate the same modification on residues it cannot occupy (one decoy site per real
  site, evenly spread over the peptide). Candidates are flagged in `metadata["mumble_decoy_site"]`
  (`True` for decoy sites, `False` for real candidates and, when kept, the original PSM). Intended
  as within-spectrum negatives for site-localisation models and false-localisation-rate estimates.

## [0.3.0] - 2026-07-15

### Changed
- Cache directory now uses `platformdirs` for a proper user cache location instead of a hardcoded path.
- Simplified and optimized the `localize_mass_shift` caching logic: per-modification results are now cached and shared across combinations instead of being recomputed for every combination, and a stale recursive check that never actually recursed was removed.
- Bumped minimum `rustyms` version to 0.10.0.
- Marked the project as beta software in the README and package classifiers.
- Various small packaging and bug fixes (argument handling in `PSMHandler`, `.gitignore`, README clarifications).

[0.3.0]: https://github.com/CompOmics/mumble/releases/tag/0.3.0
