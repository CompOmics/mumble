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
  Also available as `--include-mumble-decoys` on the command line.
- `isotope_errors` option (default `[0]`, CLI `--isotope-errors`): mass shifts are also matched
  after subtracting k 13C spacings for each listed isotope error k, so a modification is found
  when a 13C peak was selected as the monoisotopic precursor. Shifted lookups are skipped when the
  unmodified peptide already fits at one of the isotope errors. Every PSM gets
  `metadata["isotope_error"]`: the k of its candidate, or for the original PSM the k at which the
  unmodified peptide fits (`0` if it does not fit).

### Fixed
- Amino-acid combinations (`aa_combinations`) were never merged into the sorted mass lookup and
  could not be matched to any mass shift.
- An amino-acid combination named like a Unimod modification (`GG`) overwrote that modification.

## [0.3.0] - 2026-07-15

### Changed
- Cache directory now uses `platformdirs` (user cache location).
- `localize_mass_shift` caches per-modification results and shares them across combinations. Removed an unused recursive check.
- Bumped minimum `rustyms` version to 0.10.0.
- Marked the project as beta software in the README and package classifiers.
- Various small packaging and bug fixes (argument handling in `PSMHandler`, `.gitignore`, README clarifications).

[0.3.0]: https://github.com/CompOmics/mumble/releases/tag/0.3.0
