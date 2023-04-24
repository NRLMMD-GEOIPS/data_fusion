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

"""Setup for data_fusion package."""

import setuptools

package_name = "data_fusion"

setuptools.setup(
    name=package_name,
    use_scm_version={
        "write_to": f"{package_name}/version.py",  # Writes hard coded version to file
        "version_scheme": "post-release",  # Use current version .postN vs incrementing
        "local_scheme": "no-local-version",
    },  # Does not include extra hash info
    setup_requires=["setuptools_scm"],
    packages=setuptools.find_packages(),
    install_requires=[
        "geoips>=1.5.3",
    ],
    entry_points={
        "console_scripts": [
            "data_fusion_procflow=data_fusion.commandline.data_fusion_procflow:main",
        ],
        "geoips.procflows": [
            "data_fusion=data_fusion.plugins.modules.procflows.data_fusion:data_fusion"
        ],
        "geoips.algorithms": [
            "stitched=data_fusion.plugins.modules.algorithms.stitched:stitched"
        ],
        "geoips.output_formatters": [
            "layered_imagery=data_fusion.plugins.modules.output_formatters.layered_imagery:layered_imagery"
        ],
    },
)
