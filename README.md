# Mumble

**Finding the perfect unimod match for your mass shifted PSM**

> [!IMPORTANT]
> Mumble is under active development and should be considered **beta** software. It is usable
> and already improves identification rates on open-modification-search-style data, but
> occasional errors can still occur, especially on unusual input files or uncommon
> modifications. Results should be reviewed before downstream use, and issues can be reported on
> the [issue tracker](https://github.com/compomics/mumble/issues).

## Overview

The PSM Modification Handler is a Python-based tool designed to find candidate unimod modifications for mass shifts. The tool allows users to apply modifications to PSMs, localize mass shifts, and generate lists of modified PSMs.

## Features

- **PSM Modification**: Apply specific modifications to PSMs and generate modified PSM lists.
- **Mass Shift Localization**: Identify potential modifications in peptides by localizing mass shifts.
- **Flexible Input/Output**: Read PSMs from various file formats, modify them, and write the results to different output formats.
- **Customizable Modifications**: Supports the addition of amino acid combinations and handles custom modifications through the Unimod database.

## Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package installer)

### Required Libraries

Install the required Python library using the following command:

```bash
pip install mumble
```


## Usage

### Command-Line Interface (CLI) Usage

Mumble provides a command-line interface to modify PSMs based on mass shifts, as well as several parameters for customization. You can use the `mumble` command to interact with the tool.

#### Basic Command Syntax

To run the CLI, use the following command:

```bash
mumble [OPTIONS] INPUT_FILE
```

Where `INPUT_FILE` is the path to the input file containing the PSM data.

#### Parameters:

Here are the available options you can pass when running the command:

- **`--psm-list`**: (required) Path to the input file containing the PSM data. Must be provided if not already set via arguments.
- **`--modification-file`**: Path to a restriction list of modifications to use from Unimod. Defaults to `default_ptm_list.tsv` included with the package.
- **`--psm-file-type`**: Type of the input file to read with PSM_utils (e.g., `mzid`, `tsv`). Default is "infer".
- **`--aa-combinations`**: Number of amino acid combinations to add as modification. Requires a `fasta_file`. Default is `0`.
- **`--fasta-file`**: Path to a fasta file (for use with `aa_combinations`).
- **`--mass-error`**: Mass error for the mass shift, default is `0.02`.
- **`--output-file`**: Path to the output file to write modified PSMs.
- **`--write-filetype`**: Type of the output file to write with PSM_utils (e.g., `tsv`, `csv`). Default is `tsv`.
- **`--include-decoy-psm`**: Flag to parse modifications for decoys in the modified PSM list.
- **`--include-original-psm`**: Flag to keep the original PSMs in the modified PSM list.
- **`--combination-length`**: Maximum number of modifications per combination. All lower numbers will be included as well. Default is `1`.
- **`--exclude-mutations`**: If set, modifications with the classification 'AA substitution' will be excluded.
- **`--config-file`**: Path to a config file for additional configuration parameters (e.g., custom modification sets, advanced settings).
- **`--log-level`**: Set the logging level. Options: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`. Default is `INFO`.
- **`--clear-cache`**: Remove the modification cache file and exit early.
- **`--all-unimod-modifications`**: Use all available modifications from Unimod instead of a subset.

#### Examples:

1. **Modify a single PSM**:
```bash
mumble --psm-list "path/to/psm_file.mzid" --mass-error 0.02 --output-file "modified_psms.tsv"
```

2. **Modify a list of PSMs with custom configurations**:
```bash
mumble --psm-list "path/to/psm_file.mzid" --fasta-file "path/to/proteins.fasta" --aa-combinations 5 --config-file "path/to/config_file.json"
```

3. **Clear the cache and exit**:
```bash
mumble --clear-cache
```

4. **Using a custom modification file**:
```bash
mumble --psm-list "path/to/psm_file.mzid" --modification-file "path/to/custom_ptm_list.tsv"
```

#### Config file usage

You can also use a configuration file to specify options that will be loaded automatically when running the command. This allows you to store commonly used parameters without needing to pass them every time.

Example configuration file (`config_file.json`):

```json
{
    "mass_error": 0.05,
    "aa_combinations": 2,
    "psm_file_type": "mzid",
    "output_file": "output.tsv"
}
```

You can then specify the path to this file using the `--config-file` option:

```bash
mumble --config-file "path/to/config_file.json"
```

### Python API 
Here's a quick example of how to use the PSM Modification Handler through the python API for single PSMs:

```python
>>> from mumble import PSMHandler
>>> from psm_utils import PSM

>>> # Initialize the PSMHandler
>>> psm_handler = PSMHandler(aa_combinations=0, fasta_file=None, mass_error=0.02)

>>> # Create a minimal PSM to generate modified version from
>>> psm = PSM(
...     peptidoform="ARTHR/3",
...     precursor_mz=228.129628 # Required information
... )
>>> # Generate proteoforms for given PSM with a certain MZ
>>> modified_proteoforms = psm_handler.get_modified_peptidoforms_list(psm, include_original_psm=False)


>>> # Write the modified PSM list to a file
>>> psm_handler.write_modified_psm_list(modified_proteoforms, output_file="modified_proteoforms.tsv", psm_file_type="tsv")

>>> print(modified_proteoforms)
# [
#     PSM(
#         peptidoform="[Acetyl]-ARTHR/3"
#         precursor_mz=228.129628
#     )
# ]
```
Here's a quick example of how to use the PSM Modification Handler through the python API for PSM lists:
```python
>>> # Add modified PSMs, reading directly from a PSM file
>>> # (add_modified_psms also accepts a list of PSM objects or a PSMList)
>>> modified_psm_list = psm_handler.add_modified_psms(
...     "path/to/psm_file.mzid",
...     psm_file_type="mzid",
...     include_decoy_psm=False,
...     include_original_psm=True,
... )

>>> # Write the modified PSM list to a file
>>> psm_handler.write_modified_psm_list(modified_psm_list, output_file="modified_psms.tsv", psm_file_type="tsv")
```
For more information on PSM objects and PSM lists visit [psm_utils](https://github.com/compomics/psm_utils)

## Testing

The project includes unit tests using `pytest` to ensure code reliability.

### Running Tests

To run the tests, simply use the following command:

```bash
pytest
```

### Contributing


Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature-name`).
5. Open a pull request.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **PSMUtils**: For providing core utilities for PSM handling. ([psm_utils](https://github.com/compomics/psm_utils))
- **Pyteomics**: For offering tools to handle mass spectrometry data. ([pyteomics](https://github.com/levitsky/pyteomics))

