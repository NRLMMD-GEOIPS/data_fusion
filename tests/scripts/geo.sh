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

if [[ "$1" == "" ]]; then
    curr_product='Infrared-Gray'
else
    curr_product=$1
fi

data_fusion_procflow \
      --procflow data_fusion \
      --compare_path $GEOIPS_BASEDIR/geoips_packages/data_fusion/tests/outputs/${curr_product}_image \
      --filename_formatter geoips_fname \
      --fusion_final_output_formatter imagery_annotated \
      --fusion_final_product_name Blended-Infrared-Gray \
      --fusion_final_source_name stitched \
      --fusion_final_platform_name geo \
      --sector_list global \
      --fuse_files $GEOIPS_BASEDIR/test_data/test_data_fusion/data/goes16_20210929.0000/* \
          --fuse_reader_name abi_netcdf \
          --fuse_product_name ${curr_product} \
          --fuse_dataset_name goes16 \
          --fuse_order 0 \
      --fuse_files $GEOIPS_BASEDIR/test_data/test_data_fusion/data/goes17_20210929.0000/* \
          --fuse_reader_name abi_netcdf \
          --fuse_product_name ${curr_product} \
          --fuse_dataset_name goes17 \
          --fuse_order 1 \
      --fuse_files $GEOIPS_BASEDIR/test_data/test_data_fusion/data/himawari8_20210929.0000/* \
          --fuse_reader_name ahi_hsd \
          --fuse_product_name ${curr_product} \
          --fuse_dataset_name ahi \
          --fuse_order 2 \
      --fuse_files $GEOIPS_BASEDIR/test_data/test_data_fusion/data/msg1_20210929.0000/* \
          --fuse_reader_name seviri_hrit \
          --fuse_product_name ${curr_product} \
          --fuse_dataset_name msg1 \
          --fuse_order 3 \
      --fuse_files $GEOIPS_BASEDIR/test_data/test_data_fusion/data/msg4_20210929.0000/* \
          --fuse_reader_name seviri_hrit \
          --fuse_product_name ${curr_product} \
          --fuse_dataset_name msg4 \
          --fuse_order 4
retval=$?

exit $retval