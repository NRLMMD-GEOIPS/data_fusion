# # # Distribution Statement A. Approved for public release. Distribution unlimited.
# # #
# # # Author:
# # # Naval Research Laboratory, Marine Meteorology Division
# # #
# # # This program is free software: you can redistribute it and/or modify it under
# # # the terms of the NRLMMD License included with this program. This program is
# # # distributed WITHOUT ANY WARRANTY; without even the implied warranty of
# # # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the included license
# # # for more details. If you did not receive the license, for more information see:
# # # https://github.com/U-S-NRL-Marine-Meteorology-Division/

''' Command line script for kicking off geoips based procflows. MUST call with --procflow'''

from geoips.commandline.run_procflow import main as geoips_main
from data_fusion.commandline.args import get_command_line_args


def main():
    ''' Script to kick off processing based on command line args '''
    geoips_main(get_command_line_args)


if __name__ == '__main__':
    main()
