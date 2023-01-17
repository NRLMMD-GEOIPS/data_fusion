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

Data Fusion GeoIPS Plugin
==========================

The data_fusion package is a GeoIPS-compatible plugin, intended to be used within the GeoIPS ecosystem.
Please see the 
[GeoIPS Documentation](https://github.com/NRLMMD-GEOIPS/geoips/blob/main/README.md)
for more information on the GeoIPS plugin architecture and base infrastructure.

Package Overview
-----------------

The Data Fusion plugin provides the capability for including an arbitrary number of data types within
a single product or algorithm - an alternative processing workflow developed within this package
handles passing different combinations of datasets to each module appropriately - the main geoips
package only provides support for including a single dataset per product.

Currently, the test scripts can be used as templates for setting up additional data fusion products and
algorithms.  Additional documentation will be added in time.  If you have questions, please
contact geoips@nrlmry.navy.mil.

System Requirements
---------------------

* geoips >= 1.5.3
* Test data repos contained in $GEOIPS_TESTDATA_DIR for tests to pass.
  * NOTE: Must obtain appropriate ABI, AHI test datasets via NOAA AWS
  * NOTE: Must obtain appropriate SEVIRI test datasets via EUMETSAT

IF REQUIRED: Install base geoips package
------------------------------------------------------------
SKIP IF YOU HAVE ALREADY INSTALLED BASE GEOIPS ENVIRONMENT 

If GeoIPS Base is not yet installed, follow the
[installation instructions](https://github.com/NRLMMD-GEOIPS/geoips/blob/main/docs/installation.rst)
within the geoips source repo documentation:

Install data_fusion package
----------------------------
```bash
    # Assuming you followed the fully supported installation,
    # using $GEOIPS_PACKAGES_DIR and $GEOIPS_CONFIG_FILE:
    source $GEOIPS_CONFIG_FILE
    git clone -b $GEOIPS_ACTIVE_BRANCH $GEOIPS_REPO_URL/data_fusion $GEOIPS_PACKAGES_DIR/data_fusion
    pip install -e $GEOIPS_PACKAGES_DIR/data_fusion
```

Test data_fusion installation
-----------------------------
```bash
    # Assuming you followed the fully supported installation,
    # using $GEOIPS_PACKAGES_DIR and $GEOIPS_CONFIG_FILE:
    source $GEOIPS_CONFIG_FILE
    $GEOIPS_PACKAGES_DIR/data_fusion/tests/test_all.sh
```
