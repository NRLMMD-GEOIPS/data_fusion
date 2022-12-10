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


<!---
@ Please update CHANGELOG with your desired initial version number (should match what is found in VERSION file),
@ and with todays date and any other updates related to your initial commit.

@ Update all portions of CHANGELOG identified with "@"
--->


# @v0.1.0: @YYYY-MM-DD, Initial commit of @new functionality@

### Major New Functionality
* **Top Level Administrivia**
    * **README.md**: standard README with repo cloning, optionall geoips installation, and testing
    * **CHANGELOG.md**: Initial CHANGELOG contents.
    * **VERSION**: Required VERSION file
    * **setup.py**: pip setup.py with package dependencies and entry points.
* **Testing**
    * **tests/test_all.sh**: Complete test script for full package integration tests
    * **@tests/scripts/@mydatatype@.tc.@product@.imagery_clean.sh@**: @Direct single source test call.@
    * **tests/scripts/test_config.sh**: Complete functionality integration test.
    * **tests/scripts/test_config.yaml**: YAML output config to product all available products and sectors
        * @product1 description@
        * @product2 description@
* **Package modules**
    * **@package@/interface_modules/readers/@my_reader@**: @Info on reader
    * **@package@/interface_modules/@module_type@/@my_module@**: @Info on module
    * **@include all new modules, with descriptions@**
