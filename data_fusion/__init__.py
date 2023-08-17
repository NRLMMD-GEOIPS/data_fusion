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

"""
The GeoIPS |unireg| data_fusion Package provides a Python 3 plugin to GeoIPS.

The data_fusion plugin provides the capability for including an arbitrary number
of data types within a single product or algorithm.

.. |unireg|    unicode:: U+000AE .. REGISTERED SIGN

"""

from ._version import __version__, __version_tuple__

__all__ = ["__version__", "__version_tuple__"]
