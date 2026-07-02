import click
import logging
import sys
import importlib
from rich.logging import RichHandler

from mumble import PSMHandler, remove_modification_cache

# setup logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format="%(message)s",  # Simple format for logging
    datefmt="[%X]",  # Time format
    handlers=[RichHandler(rich_tracebacks=True, show_path=False)],
)

# Define CLI options as a dictionary
CLI_OPTIONS = {
    "psm_list": {
        "type": click.Path(exists=True),
        "help": "Path to the input file.",
    },
    "modification_file": {
        "type": click.Path(exists=True),
        "help": "Restriction list of modifications to use from Unimod.",
        "default": str(importlib.resources.files("mumble.package_data") / "default_ptm_list.tsv"),
        "show_default": True,
    },
    "psm_file_type": {
        "type": click.STRING,
        "help": "Type of the input file to read with PSM_utlis.io.read_file",
        "default": "infer",
    },
    "aa_combinations": {
        "type": click.INT,
        "help": "Number of amino acid combinations to add as modification REQUIRES fasta_file",
        "default": 0,
        "show_default": True,
    },
    "fasta_file": {
        "type": click.Path(exists=True),
        "help": "Path to a fasta file",
        "default": None,
    },
    "mass_error": {
        "type": click.FLOAT,
        "help": "Mass error for the mass shift",
        "default": 0.02,
        "show_default": True,
    },
    "output_file": {
        "type": click.STRING,
        "help": "Path to the output file",
        "default": None,
    },
    "write_filetype": {
        "type": click.STRING,
        "help": "Type of the output file to write with PSM_utlis.io.write_file",
        "default": "tsv",
        "show_default": True,
    },
    "include_decoy_psm": {
        "is_flag": True,
        "help": "Parse modifications for decoys in modified PSMlist",
        "default": False,
        "show_default": True,
    },
    "include_original_psm": {
        "is_flag": True,
        "help": "Keep the original PSMs in the modified PSMlist",
        "default": False,
        "show_default": True,
    },
    "combination_length": {
        "type": click.INT,
        "help": "Maximum number of modifications per combination. All lower numbers will be included as well.",
        "default": 1,
        "show_default": True,
    },
    "exclude_mutations": {
        "is_flag": True,
        "help": "If set, modifications with the classification 'AA substitution' will be excluded.",
        "default": False,
        "show_default": True,
    },
    "config_file": {
        "type": click.Path(exists=True),
        "help": "Path to a config file",
        "default": None,
    },
    "log_level": {
        "type": click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
        "default": "INFO",
        "help": "Set the logging level",
        "show_default": True,
    },
    "all_unimod_modifications": {
        "is_flag": True,
        "default": False,
        "help": "Instead of using a subset of modifications from Unimod, use all available modifications.",
        "show_default": True,
    },
}


@click.command("cli", context_settings={"show_default": True})
@click.argument("input_file", type=click.Path(exists=True), default=None, required=False)
@click.option(
    "--clear-cache/--no-clear-cache",
    is_flag=True,
    default=False,
    help="Remove the modification cache file and exit early.",
)
def main(clear_cache, **kwargs):
    """
    Finding the perfect match for your mass shift.
    """
    # if the user just wants to clear the cache, do it and quit
    if clear_cache:
        remove_modification_cache()
        logging.info("Exiting Mumble. You will find your match another time.")
        sys.exit(0)

    # Set the logging level based on the CLI option
    log_level = kwargs.get("log_level", "INFO").upper()
    logging.getLogger().setLevel(log_level)

    ctx = click.get_current_context()

    # Extract CLI-provided parameters
    cli_params = {
        key: value
        for key, value in kwargs.items()
        if ctx.get_parameter_source(key) == click.core.ParameterSource.COMMANDLINE
    }

    # Initialize PSMHandler with priority for CLI params
    psm_handler = PSMHandler(
        config_file=kwargs.get("config_file"),
        **cli_params,
    )
    modified_psm_list = psm_handler.add_modified_psms(kwargs["input_file"])

    psm_handler.write_modified_psm_list(modified_psm_list)


# Dynamically add CLI options
for option, params in CLI_OPTIONS.items():
    main = click.option(f"--{option.replace('_', '-')}", **params)(main)

if __name__ == "__main__":
    main()
