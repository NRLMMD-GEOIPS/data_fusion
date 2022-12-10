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

#!/bin/bash

# Identify and update all instances of @ found within this script appropriately.
#   @package@ should be the name of this repository
#   @datatype@ should reference the datatype you are interested in processing (and will reference the test data
#              repository you set up through https://github.com/NRLMMD-GEOIPS/template_test_data
#   @datafile@ is the appropriate path to your data files within the test data repo.
#   @test_script_1@ indicates that the test output directory name should match the test script name by convention
#   @readername@ is the appropriate reader associated with your testdataset
#   @product@ is the product you would like to test.
#   NOTE: imagery_clean preferred to avoid dependencies on external plotting packages for image consistency,
#           though you may change the output format if required for your package testing.

# Note you may update other arguments within this test call, or add additional arguments.
# Also - the first time you run your test script, it will prompt you to update your test outputs - at that point
# you can populate the "tests/outputs" directory, and your next run will result in a 0 return value.

# Ensure each test script is called from the @package@/tests/test_all.sh script.

# Please create a separate test script for each piece of functionality you would like to test.

    # --resampled_read \  # @NOTE: --resampled_read argument required for ABI and AHI readers.
run_procflow \
    $GEOIPS_TESTDATA_DIR/test_data_@datatype@/data/@datafile@ \
    --procflow single_source \
    --reader_name @readername@ \
    --product_name @product@ \
    --compare_path "$GEOIPS_BASEDIR/geoips_packages/@package@/tests/outputs/@test_single_source@" \
    --output_format imagery_clean \
    --filename_format geoips_fname \
    --sector_list global \
    --sectorfiles $GEOIPS/tests/sectors/static/global.yaml
ss_retval=$?

exit $((ss_retval))
