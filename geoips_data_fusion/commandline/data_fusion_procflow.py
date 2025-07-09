# # # This source code is subject to the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

"""
Command line script for kicking off geoips based procflows.

MUST call with --procflow
"""

from geoips.commandline.run_procflow import main as geoips_main
from geoips_data_fusion.commandline.args import get_command_line_args


def main():
    """Script to kick off processing based on command line args."""
    geoips_main(get_command_line_args)


if __name__ == "__main__":
    main()
