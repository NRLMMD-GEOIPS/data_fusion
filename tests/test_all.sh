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

# Please identify and update all instances of "@" found in this script appropriately.
# You will need to generate one or more test scripts that test your complete functionality,
# (these scripts provide example geoips calls and sample output, as well as providing a full integration test),
# and call each script within the test_all.sh script.  Do not rename this script or test directory - automated
# integrations tests look for the tests/test_all.sh script for complete testing.

#!/bin/bash

# This should contain test calls to cover ALL required functionality tests for the @package@ repo.

# The $GEOIPS tests modules sourced within this script handle:
   # setting up the appropriate associative arrays for tracking the overall return value,
   # calling the test scripts appropriately, and 
   # setting the final return value.

# Note you must use the variable "call" in the for the loop

. $GEOIPS/tests/utils/test_all_pre.sh @package@

echo ""
# "call" used in test_all_run.sh
for call in \
\
            "$GEOIPS_PACKAGES_DIR/@package@/tests/scripts/test_config.sh" \
            "$GEOIPS_PACKAGES_DIR/@package@/tests/scripts/@mydatatype@.tc.@product@.imagery_clean.sh"
do
    . $GEOIPS/tests/utils/test_all_run.sh
done

. $GEOIPS/tests/utils/test_all_post.sh
