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

for product_name in Layered-Winds-Default \
                    Layered-Winds-Two-Colorbars \
                    Layered-Winds-Horizontal-Adjust \
                    Layered-Winds-Vertical-Default \
                    Layered-Winds-Vertical-Adjust \
                    Layered-Winds-Horizontal-and-Vertical; do

data_fusion_procflow \
      --compare_path $GEOIPS_PACKAGES_DIR/data_fusion/tests/outputs/${product_name}_image \
      --filename_formatter geoips_fname \
      --procflow data_fusion \
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
