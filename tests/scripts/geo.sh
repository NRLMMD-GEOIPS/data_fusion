# # # This source code is subject to the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

if [[ "$1" == "" ]]; then
    curr_product='Infrared-Gray'
else
    curr_product=$1
fi

geoips run data_fusion \
      --compare_path $GEOIPS_PACKAGES_DIR/data_fusion/tests/outputs/${curr_product}_image \
      --filename_formatter geoips_fname \
      --sector_list global \
      --fusion_final_output_formatter imagery_annotated \
      --fusion_final_product_name Blended-Infrared-Gray \
      --fusion_final_source_name stitched \
      --fusion_final_platform_name geo \
      --fuse_files $GEOIPS_TESTDATA_DIR/test_data_fusion/data/goes16_20210929.0000/* \
          --fuse_reader_name abi_netcdf \
          --fuse_product_name ${curr_product} \
          --fuse_dataset_name goes16 \
          --fuse_order 0 \
      --fuse_files $GEOIPS_TESTDATA_DIR/test_data_fusion/data/goes17_20210929.0000/* \
          --fuse_reader_name abi_netcdf \
          --fuse_product_name ${curr_product} \
          --fuse_dataset_name goes17 \
          --fuse_order 1 \
      --fuse_files $GEOIPS_TESTDATA_DIR/test_data_fusion/data/himawari8_20210929.0000/* \
          --fuse_reader_name ahi_hsd \
          --fuse_product_name ${curr_product} \
          --fuse_dataset_name ahi \
          --fuse_order 2
retval=$?

exit $retval
