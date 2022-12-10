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

# Please identify all instances of "@" within this file, and update appropriately.

'''Installation instructions for @package@ package'''

from os.path import realpath, join, dirname

import setuptools

# NOTE: VERSION file must contain ONLY the version number, no comments, etc.
# You may set the initial version to any value you desire, just update VERSION appropriately.
with open(join(dirname(realpath(__file__)), 'VERSION'), encoding='utf-8') as version_file:
    version = version_file.read().strip()

# Info on Python package_data: https://setuptools.pypa.io/en/latest/userguide/datafiles.html
# Info on Python entry points: https://setuptools.pypa.io/en/latest/userguide/entry_point.html
setuptools.setup(
    name='@package@',
    version=version,
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={"@package@": [
                                "yaml_configs/*",
                                "yaml_configs/*/*",
                                "yaml_configs/*/*/*",
                                ],
                  },
    install_requires=[
                      # Include required external Python packages (ie, packages that are installable via pip)
                      ],
    entry_points={

        # Add entry points as needed for your particular @package
        # Uncomment and update appropriately for each module you will be implementing.
        # You can have more than one module per module type (ie, arbirary numbers of readers, algorithms, etc)

        # 'geoips.readers': [
        #     '@my_reader@=@package@.interface_modules.readers.@myreader@:@myreader@',
        # ],
        # 'geoips.output_formats': [
        #     '@my_output_format_1@=@package@.interface_modules.output_formats.@my_output_format_1@:@my_output_format_1@',
        #     '@my_output_format_2@=@package@.interface_modules.output_formats.@my_output_format_2@:@my_output_format_2@',
        # ],
        # 'geoips.algorithms': [
        #     '@my_alg@=@package@.interface_modules.algorithms.@my_alg@:@my_alg@',
        # ],
        # 'geoips.trackfile_parsers': [
        #     '@my_parser@=@package@.interface_modules.trackfile_parsers.@my_parser@:@my_parser@'
        # ],
        # 'geoips.interpolation': [
        #     '@my_interp@=@package@.interface_modules.interpolation.@my_interp@:@my_interp@'
        # ],
        # 'geoips.user_colormaps': [
        #     '@my_cmap@=@package@.interface_modules.user_colormaps.@my_cmap@:@my_cmap@',
        # ],
        # 'geoips.filename_formats': [
        #     '@my_fname@=@package@.interface_modules.filename_formats.@my_fname@:@my_fname@',
        # ],
        # 'geoips.title_formats': [
        #     '@my_title@=@package@.interface_modules.title_formats.@my_title@:@my_title@',
        # ],
        # 'geoips.coverage_checks': [
        #     '@my_covg@=@package@.interface_modules.coverage_checks.@my_covg@:@my_covg@',
        # ],
    }
)
