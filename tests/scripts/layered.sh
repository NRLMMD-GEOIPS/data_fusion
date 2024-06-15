# # # Distribution Statement A. Approved for public release. Distribution is unlimited.
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

# Note that all --fuse_* arguments are ordered - there can be any number included in the command line
# call, and they will be appended in the order they are received. Ensure the --fuse_* arguments are
# grouped together appropriately for each data type.

# Identify and update all instances of @ found within this script appropriately.

#   @package@ should be the name of this repository
#   @my_layered_test_script@ indicates that the test output directory name should match
#                            the test script name by convention

# Fusion Final arguments: These are the arguments to specify the final output product, after layering
#                         each individual "fuse" product specification below. The "fusion_final" arguments
#                         indicate how to bring all the individual products together into a single "final" product.
#   @My-Layered-Product@: This is the name of your final product.  This MUST match @My-Layered-Product@ specified
#                         within product_inputs/layered.yaml
#   --fusion_final_source_name layered: The source name "layered" must match both:
#                         * the name of the file product_inputs/layered.yaml and
#                         * the key at the top level of product_inputs/layered.yaml
#                         This is an arbitrarily defined "source" name, but it must be consistent.
#   --fusion_final_platform_name multi: This is an entirely arbitrarily defined platform name.
#                         It is only used for filename and title generation
#                         (sets "platform_name" on the final xarray object)
#   --fusion_final_output_format layered_imagery: Do not change this argument - the "layered_imagery"
#                         output_format in the data_fusion repository is the magic that plots the
#                         separate products together.

# Individual fuse arguments: Each set of arguments fully defines a product for a single layer of the final
# image.  Ensure the fuse arguments are grouped together appropriately for each layer:
#   @datatype_N@ should reference the Nth datatype you are interested in processing
#       (and will reference test data
#       repositories set up through
#       https://github.com/NRLMMD-GEOIPS/template_test_data)
#   @datafiles_N@ is the appropriate path to the data files of @datatype_N@ within the test data repo.
#   @fuse_reader_name_N@ is the appropriate reader associated with your @datatype_N@
#   @fuse_product_name_N@ is the product you would like to create from @datafile_N@
#   @fuse_output_format_N@ is the output format you would like to use for plotting the current layer.
#              Note this is most likely going to be a "clean" output format (no gridlines, coastlines,
#              titles, etc), since we want to simply layer the different images, and the annotations
#              will be applied via the "fusion_final_output_format".
#              Valid image formats for layering must include fig, main_ax, mapobj inputs
#                (If passed, use the existing fig, main_ax, and mapobj rather than recreating)
#              Valid image formats for layering must support not producing output if
#                output_fnames is None (so we can avoid producing images for each layer individually)
#              See geoips imagery_clean.py and imagery_windbarbs_clean.py for examples of valid output formats.
#   @fuse_dataset_name_N@: arbitrary string that defines the name of the current dataset.
#              Any instance of @fuse_dataset_name_N@ in the template script must match those in the
#              template product/layered.yaml file
#   --fuse_order: Integer specifying the order of the layers.
#              Lower numbers are on the bottom, higher numbers on the top

# Note you may update other arguments within this test call, or add additional arguments.

# Also - the first time you run your test script, it will prompt you to update your test outputs - at that point
# you can populate the "tests/outputs" directory, and your next run will result in a 0 return value.


# Please create a separate test script for each piece of functionality you would like to test.

for product_name in Layered-Winds-Default \
                    Layered-Winds-Two-Colorbars \
                    Layered-Winds-Horizontal-Adjust \
                    Layered-Winds-Vertical-Default \
                    Layered-Winds-Vertical-Adjust \
                    Layered-Winds-Horizontal-and-Vertical; do

geoips run data_fusion \
      --compare_path $GEOIPS_PACKAGES_DIR/data_fusion/tests/outputs/${product_name}_image \
      --filename_formatter geoips_fname \
      --trackfile_parser bdeck_parser \
      --trackfiles $GEOIPS_PACKAGES_DIR/geoips/tests/sectors/tc_bdecks/bwp142022.dat \
      --fusion_final_product_name $product_name \
      --fusion_final_source_name layered \
      --fusion_final_platform_name multi \
      --fusion_final_output_formatter layered_imagery \
      --fuse_files $GEOIPS_TESTDATA_DIR/test_data_scat/bg_data/ahi_20220911_1330_tc2022wp14muifa/* \
          --fuse_reader_name ahi_hsd \
          --fuse_product_name Infrared-Gray \
          --fuse_output_format imagery_clean \
          --fuse_dataset_name ir \
          --fuse_order 0 \
      --fuse_files $GEOIPS_TESTDATA_DIR/test_data_scat/data/20220911_metopb_byu_uhr_tc2022wp14muifa/MUIFA_20220911_51797_B_A-product.nc \
          --fuse_reader_name ascat_uhr_netcdf \
          --fuse_product_name windspeed \
          --fuse_output_format imagery_clean \
          --fuse_dataset_name windspeed \
          --fuse_order 1 \
      --fuse_files $GEOIPS_TESTDATA_DIR/test_data_scat/data/20220911_metopb_knmi_tc2022wp14muifa/ascat_20220911_132700_metopb_51797_eps_o_250_3202_ovw.l2.nc \
          --fuse_reader_name scat_knmi_winds_netcdf \
          --fuse_product_name Windbarbs-Gray \
          --fuse_output_format imagery_windbarbs_clean \
          --fuse_dataset_name windbarbs \
          --fuse_order 2
curr_retval=$?
# Sum up all the retvals
retval=$((curr_retval+retval))
done

exit $retval
