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

## NRLMMD-GEOIPS/geoips#69: 2023-02-06, update for interface class module plugins
### Refactor
* Replace reader and algorithm functions with geoips.interfaces calls
* Remove unused imports
```
modified: data_fusion/interface_modules/procflows/data_fusion.py
```
* Replace colormap functions with geoips.interfaces calls
```
modified: data_fusion/interface_modules/output_formats/layered_imagery.py
```


# v1.6.3: 2023-02-02, marker overlay, bug fixes
## GEOIPS#170: 2023-02-02, update during release
### Release Updates
* Update VERSION to 1.6.3, add CHANGELOG 1.6.3 line
## GEOIPS#2: 2022-12-06, overlay marker on image
### Testing
* Add layered.sh call to test_all.sh
### Major New Functionality
#### data_fusion/yaml_configs/product_inputs/layered.yaml
* Add Layered product template (does nothing)
#### data_fusion/interface_modules/output_formats/layered_imagery.py
* title construction
    * include_end_datetime option for title output specification
    * Support dictionary of dictionary of xarray objects for metadata
* get_final_mpl_colors_info
    * Allow no colormap specification!
    * Handle looping through xarrays, or dictionaries of xarrays (find order appropriately for sorting)
    * Pass fused_xarray_dict to plot_data
#### data_fusion/interface_modules/procflows/data_fusion.py
* Explicitly list "unsectored" product types
    * unsectored_xarray_dict_to_output_format
    * unsectored_xarray_dict_area_to_output_format
    * unmodified
* Do not pad or sector unsectored product types
* Additional noalg_product_types
    * sectored_xarray_dict_area_to_output_format
    * unsectored_xarray_dict_area_to_output_format
    * unmodified
* Rename "order" attribute on xarray to "fuse_order"
### Bug fixes
#### Ensure appending list of curr_products to final_products
* If curr_products is dict, append curr_products.keys() vs curr_products
```
data_fusion/interface_modules/procflows/data_fusion.py
```
## GEOIPS#4: 2022-12-09, Procflow resource usage statistics
### Major New Functionality
#### Add procflow overall resource usage statistics
* Add check for product_db, which controls if procflow writes to database
* Add call to write_stats_to_database function that adds resource usage stats to databse
    * Only called when product_db is True
```
modified: data_fusion/interface_modules/procflows/data_fusion.py
```

# v1.6.0: 2022-11-28, open source release updates
## GEOIPS#119: 2022-11-17, standardize README
### Documentation
#### Standardize README
* Remove references to package name in comments
* Replace environment variables and base installation with links to geoips repo
* Remove calls to setup.sh, just pip install data_fusion
### Installation
#### Simplify installation process
* Remove setup.sh script
* Add geoips>=1.5.3 to setup.py


# v1.5.3: 2022-11-04, initial layered product functionality, compatibility updates for pyrocb and stitched processing
## GEOIPS#8: 2022-10-24, updates to re-enable pyrocb processing
### Refactor
#### Rename from dataset_id to dataset_name
* Standardize to use "name" vs "id" internal to code.
* Also more consistent with product_name, source_name, etc
```
modified: tests/scripts/geo.sh
modified: tests/scripts/layered.sh
modified: data_fusion/commandline/args.py
modified: data_fusion/interface_modules/procflows/data_fusion.py
modified: data_fusion/interface_modules/output_formats/layered_imagery.py
```
#### Remove "primary_dataset_id" command line option
* Remove "primary" dataset, since that is a very vague term
* If we need to specify datasets to use for determining area_defs with coverage, actual %covg, etc, be explicit
    * Include in product_inputs or product_params directly
    * Use explicit terminology for what each dataset would accomplish.
```
modified: tests/scripts/geo.sh
modified: tests/scripts/layered.sh
modified: data_fusion/commandline/args.py
modified: data_fusion/interface_modules/procflows/data_fusion.py
```
#### Add "coverage_dataset" to Layered product_params files
* Rather than specifying command line, indicated within YAML product files if there is a specific coverage dataset
* Initial implementation may be less than optimal but if this layout seems appropriate we can update the backend later.
    * Pass "METADATA" dataset to plot_data as alg_xarray. Used for:
        * start/end datetime, source, platform for filenames/titles
        * variables for coverage checks
    * Update METADATA with appropriate attributes from coverage_dataset
        * start/end datetime
        * add all variables (used in conjunction of alt_varname_for_covg to ensure proper variable used for covg
```
modified: data_fusion/yaml_configs/product_inputs/layered.yaml
modified: data_fusion/yaml_configs/product_params/Layered-Winds-Horizontal-Adjust.yaml
modified: data_fusion/yaml_configs/product_params/Layered-Winds-Horizontal-and-Vertical.yaml
modified: data_fusion/yaml_configs/product_params/Layered-Winds-Vertical-Adjust.yaml
modified: data_fusion/yaml_configs/product_params/Layered-Winds-Vertical-Default.yaml
modified: data_fusion/interface_modules/procflows/data_fusion.py
```
#### Add "covg_func" and "covg_args alt_varname" to Layered product_params files
* To ensure coverage is calculated appropriately for specify the variable name to use for coverage for each
  individual dataset
* By default, looks for "final_product_name" variable, so ensure the correct variable for each dataset is used.
```
modified: data_fusion/yaml_configs/product_inputs/layered.yaml
modified: data_fusion/yaml_configs/product_params/Layered-Winds-Horizontal-Adjust.yaml
modified: data_fusion/yaml_configs/product_params/Layered-Winds-Horizontal-and-Vertical.yaml
modified: data_fusion/yaml_configs/product_params/Layered-Winds-Vertical-Adjust.yaml
modified: data_fusion/yaml_configs/product_params/Layered-Winds-Vertical-Default.yaml
```
#### Use overall start/end datetime for "METADATA"
* Previously used "primary_dataset_id" to determine METADATA attributes.
* Update to automatically determin appropriate metadata based on ALL the datasets.
* This is currently ONLY used within get_area_defs_from_command_line_args routine
```
modified: data_fusion/interface_modules/procflows/data_fusion.py
```
#### Update test output filenames
* Update multi -> layered platform name (as specified in command line call)
* Update 132801 start time to 132830 (since now using sectored coverage_dataset start time vs unsectored)
```
renamed: tests/outputs/Layered-Winds-Default_image/20220911.132801.multi.multi.Layered-Winds-Default.tc2022wp14muifa.41p03.multi.1p0.png -> tests/outputs/Layered-Winds-Default_image/20220911.132830.multi.layered.Layered-Winds-Default.tc2022wp14muifa.41p03.multi.1p0.png
renamed: tests/outputs/Layered-Winds-Horizontal-Adjust_image/20220911.132801.multi.multi.Layered-Winds-Horizontal-Adjust.tc2022wp14muifa.41p03.multi.1p0.png -> tests/outputs/Layered-Winds-Horizontal-Adjust_image/20220911.132830.multi.layered.Layered-Winds-Horizontal-Adjust.tc2022wp14muifa.41p03.multi.1p0.png
renamed: tests/outputs/Layered-Winds-Horizontal-and-Vertical_image/20220911.132801.multi.multi.Layered-Winds-Horizontal-and-Vertical.tc2022wp14muifa.41p03.multi.1p0.png -> tests/outputs/Layered-Winds-Horizontal-and-Vertical_image/20220911.132830.multi.layered.Layered-Winds-Horizontal-and-Vertical.tc2022wp14muifa.41p03.multi.1p0.png
renamed: tests/outputs/Layered-Winds-Two-Colorbars_image/20220911.132801.multi.multi.Layered-Winds-Two-Colorbars.tc2022wp14muifa.41p03.multi.1p0.png -> tests/outputs/Layered-Winds-Two-Colorbars_image/20220911.132830.multi.layered.Layered-Winds-Two-Colorbars.tc2022wp14muifa.41p03.multi.1p0.png
renamed: tests/outputs/Layered-Winds-Vertical-Adjust_image/20220911.132801.multi.multi.Layered-Winds-Vertical-Adjust.tc2022wp14muifa.41p03.multi.1p0.png -> tests/outputs/Layered-Winds-Vertical-Adjust_image/20220911.132830.multi.layered.Layered-Winds-Vertical-Adjust.tc2022wp14muifa.41p03.multi.1p0.png
renamed: tests/outputs/Layered-Winds-Vertical-Default_image/20220911.132801.multi.multi.Layered-Winds-Vertical-Default.tc2022wp14muifa.41p03.multi.1p0.png -> tests/outputs/Layered-Winds-Vertical-Default_image/20220911.132830.multi.layered.Layered-Winds-Vertical-Default.tc2022wp14muifa.41p03.multi.1p0.png
```

## GEOIPS#8: 2022-10-21, updates to allow stitched data_fusion processing
Accidentally forgot to get the original stitched processing working with the layered imagery updates.
### Bug fixes
#### new file: data_fusion/yaml_configs/product_inputs/stitched.yaml
* Make explicit "stitched" product input for stitched type outputs
* Ie, use separate "layered" and "stitched" product inputs for layered and stitched type imagery
#### renamed: data_fusion/interface_modules/output_formats/layered.py -> layered_imagery.py
* Disambiguate the output format from source name, etc
#### modified: tests/scripts/layered.sh
* Renamed layered output format to layered_imagery
#### modified: setup.py
* Renamed layered output format to layered_imagery
#### new file: tests/outputs/Infrared-Gray_image/20210929.000000.geo.stitched.Blended-Infrared-Gray.global.74p05.multi.20p0.png
* Renamed source/platform/product name
#### deleted: tests/outputs/Infrared-Gray_image/20210929.000000.multi.multi.Infrared-Gray.global.74p05.multi.20p0.png
* Renamed source/platform/product name
#### modified: data_fusion/interface_modules/procflows/data_fusion.py
* Ensure "area_definition" is attached to interp_xarrays['METADATA']
    * Used within stitched algorithm (and should be accessible to all fusion algorithms)
* Ensure we only retain unique variables through get_required_variables
* Remove unused read_all_files
#### modified: data_fusion/yaml_configs/product_inputs/multi.yaml
* Add Stitched product to multi product input
#### modified: tests/scripts/geo.sh
* Update from run_procflow to data_fusion_procflow
* Update to use standard fusion command line arguments
* Add fuse order (not really necessary, but toying with making it required)
* Update source_name from multi to stitched
* Update product_name from Stitched to Blended-Infrared-Gray
* Update platform name from multi to geo
#### modified: data_fusion/interface_modules/algorithms/stitched.py
* Remove METADATA xarray dataset before merging (was removing all blending)
* Add METADATA xarray dataset back into xarray_dict before returning! (passed by reference)
* Use METADATA for setting attributes (previously hard coded)
    * source_name
    * platform_name
    * data_provider
    * product_definition
    * area_definition
#### renamed: data_fusion/yaml_configs/product_inputs/multi.yaml -> layered.yaml
* Remove Stitched, Infrared-Gray, and WV-Lower from multi.yaml->layered.yaml
    * multi.yaml->layered.yaml used specifically for "layered" products
#### deleted: data_fusion/yaml_configs/product_params/Stitched.yaml
* Removed - product specified directly in product_inputs
#### modified: data_fusion/yaml_configs/product_inputs/abi.yaml
* Replace Stitched product name with Blended-Infrared-Gray
    * Unique fusion product names for each "final" product
    * This is currently exclusively used for identifying additional variables required 
* Use Infrared-Gray as product template
#### modified: data_fusion/yaml_configs/product_inputs/ahi.yaml
* Replace Stitched product name with Blended-Infrared-Gray
    * Unique fusion product names for each "final" product
    * This is currently exclusively used for identifying additional variables required 
* Use Infrared-Gray as product template
#### modified: data_fusion/yaml_configs/product_inputs/seviri.yaml
* Replace Stitched product name with Blended-Infrared-Gray
    * Unique fusion product names for each "final" product
    * This is currently exclusively used for identifying additional variables required 
* Use Infrared-Gray as product template
    

## GEOIPS#8: 2022-09-29, initial layered product functionality
### Major New Functionality
#### .gitignore
* Add diff_test outputs to .gitignore
#### setup.py
* Add data_fusion_procflow console_script
* Add layered output_format
#### data_fusion/commandline/data_fusion_procflow.py
This is a passthrough script to call geoips run_procflow main with data_fusion specific "get_command_line_args"
#### data_fusion/commandline/args.py
passthrough functions to use geoips args funcs, with data_fusion additions
* check_command_line_args: Pass through to geoips version, plus data_fusion specific checks
    * DO NOT allow args:
        * reader_name
        * product_name
        * output_format
    * REQUIRE args:
        * fusion_final_product_name
        * fusion_final_output_format
        * fusion_final_source_name
        * fusion_final_platform name
    * REQUIRE for each "fuse_files" set:
        * fuse_reader_name
        * fuse_product_name
        * fuse_dataset_id
    * ALLOW for each "fuse_files" set and if included for one set REQUIRE for all sets:
        * fuse_output_format
        * fuse_order
        * fuse_self_register_source
        * fuse_self_register_platform
        * fuse_self_register_dataset
        * fuse_sectored_read
        * fuse_resampled_read
* get_command_line_args: Pass through to geoips version, with alternate add_args and check_args funcs specified
* add_args: Calls geoips version (to get all standard command line args), then adds data_fusion specific args
    * fuse_output_format: must be same length as "fuse_files" - specifies output format for each set
    * fuse_order: must be same length as "fuse_files" - specifies ordering for layers.
    * fuse_dataset_id: unique string or integer identifying the current dataset
    * fuse_product_name: product name for current fuse dataset (override fuse_product in geoips args)
    * fuse_reader_name: reader name for current fuse dataset (override fuse_reader in geoips args)
    * fusion_primary_dataset_id: single argument, specifies which "fuse_files" dataset should be primary
    * fusion_final_platform_name: id for what should be considered the "platform_name" for the final product
        * ie, things like "multi" or "geo_polar" or "merged_geo", etc
    * fusion_final_source_name: id for what should be considered the "source_name" for the final product
        * ie, things like "multi" or "visir_winds" or "visir", etc
    * fusion_final_output_format: output_format module to be used for the final product
    * fusion_final_product_name: product name to be used for the final product
#### data_fusion/interface_modules/output_formats/layered.py
* Output format that plots various products in specified order
* Heavily rely on geoips/image_utils/mpl_utils.py functions, with additional code to handle multiple datasets
##### def layered (top level)
1. Loop through all datasets, sorted by xobj.order (smallest value on the bottom, largest on the top)
    * Plot dataset using geoips.interface_modules.procflows.single_source.plot_data directly 
2. Set title based on all datasets (using .layered_title / geoips.image_utils.mpl_utils.set_title)
3. Plot overlays (gridlines, boundaries, etc, using geoips.image_utils.mpl_utils.plot_overlays)
4. Create all colorbars (using .create_all_colorbars)
5. Write out output_fnames (using geoips.image_utils.mpl_utils.save_image)
##### def layered_title
* Sets up title based on metadata from each dataset
* Eventually will support additional arguments in product YAML - for now just default formatting
    * one line for each dataset
    * Same formatting as default title format
##### def get_arg(xobj, arg_type, dataset_id, arg_name)
* Allow pulling a single argument out of the product definition, which is attached to the xarray dataset
* Found in: xobj.attrs['product_definition'][arg_type][dataset_id][arg_name]
##### def get_final_mpl_colors_info
* Pull mpl_colors_info from the specified product/source (once for each dataset)
* Override entries within mpl_colors_info with values found in product definition
##### def create_all_colorbars
* Calculate sizes of each colorbar based on specifications in product definition
    * If colorbar_positioning unspecfieid, defaults are based on orientation and number of colorbars - equal sizes.
    * start_x_pos - relative to main_ax (0 to 1.0 within bounds, <0 left of main_ax, >1.0 right of main_ax)
    * end_x_pos - relative to main_ax (0 to 1.0 within bounds, <0 left of main_ax, >1.0 right of main_ax)
    * start_y_pos - relative to main_ax (0 to 1.0 within bounds, <0 below main_ax, >1.0 above main_ax)
    * end_y_pos - relative to main_ax (0 to 1.0 within bounds, <0 below main_ax, >1.0 above main_ax)
* Call geoips.image_utils.mpl_utils.create_colorbar with specified mpl_colors_info parameters to create each cbar
#### data_fusion/interface_modules/procflows/data_fusion.py
Updates for layered imagery
##### Command line updates
* Add support for fusion output_formats and fusion order to command line args
* Pull full set of fusion datasets from unpack_fusion_arguments, working from full command_line_args dict
    * Include "final" and "primary" datasets (as specified command line)
    * Include ALL possible information for each individual dataset, as specified command line
* Move error checking into commandline/args.py script
##### Top level updates (final vs primary vs METADATA)
* Replace inaccurate "primary_product_name" variable name with "final_product_name"
* Use same plot_data for all product types
    * If fused_xarray is dict, use alg_xarray = fused_xarray['METADATA']
    * Else if fused_xarray is an xarray.Dataset, use alg_xarray = fused_xarray
* Use {dataset_id} as dataset name for all dictionaries (processed and non-processed)
* Add "find_fuse_dataset" function that takes the full dict,
  and currently just "dataset_id" to pull the appropriate dataset
* Use "primary" fusion dataset for identifying area_defs if available
    * dataset METADATA (start/end datetime) required to obtain area_defs for time-based sectors
    * Remove "variables" argument from get_area_defs_from_command_line_args call - unused
    * Remove "get_required_fusion_variables" function - unneeded
* Include metadata_xobj for "final" fusion dataset
    * Include all standard metadata (data_provider, source_name, platform_name, etc)
* Include all attrs from fuse_data dictionary on final xarrays that are passed to output format module
##### Updates to get_fused_xarray
* Explicity require product family to be one "alg_product_families" or "noalg_product_families" - no default
    * alg_product_types = ['alg', 'interp', 'interp_alg', 'interp_alg_cmap', 'alg_interp_cmap', 'alg_cmap', 'cmap']
    * noalg_product_types = ['sectored_xarray_dict_to_output_format',
                             'unsectored_xarray_dict_to_output_format',
                             'xarray_dict_to_output_format']
* For noalg_product_types, add METADATA from individual fuse datasets to interp_xarrays[dataset_name]['METADATA']
* Create interp_xarrays['METADATA'] = fuse_data['final']['metadata_xobj']
* Create interp_xarrays['METADATA'][final_product_name] = interp_xarrays[primary_dataset_id][primary_product_name]
   * Used for checking coverage
* Update to allow fusion products that apply an algorithm or not (support overlays)
   * Only add required variables for "final_product" for current fuse_source_name if final product
     specified in product_inputs/<source>.yaml
   * Allow skipping alg application for "no_alg_product_types" in get_fuse_xarray
       * sectored_xarray_dict_to_output_format
       * unsectored_xarray_dict_to_output_format
       * xarray_dict_to_output_format
   * Allow calling output format that takes a dictionary of xarrays rather than single xarray Dataset
### Test Repo Updates
#### tests/scripts/layered.sh
Updated command line arguments
* Use data_fusion_procflow vs run_procflow
* Specify "fuse_order" - for assembling final imagery appropriately
* Specify "fuse_dataset_id" - unique identifier for each set of files
* Specify "fuse_reader_name" vs "fuse_reader" for consistency
* Specify "fuse_product_name" vs "fuse_product" for consistency
* Specify "fusion_primary_dataset_id" - for identifying dataset that should be considered "primary"
    * for determining product datetime, etc
    * Use "fuse_dataset_id" unique string/int as "fusion_primary_dataset_id" identifier
* --fusion_final_<arg> in place of --output_format, --product_name
    * --fusion_final_product_name Layered-Winds \
    * --fusion_final_source_name multi \
    * --fusion_final_platform_name Geo-Polar \
    * --fusion_final_output_format Layered \
    * --fusion_primary_dataset_id windspeed \
* Initial test will include TC test case with Infrared-Gray, windspeed, and Windbarb-Gray.
* Call all test products, and return sum of all return values:
    * Layered-Winds-Default
    * Layered-Winds-Two-Colorbars
    * Layered-Winds-Horizontal-Adjust
    * Layered-Winds-Vertical-Default
    * Layered-Winds-Vertical-Adjust
    * Layered-Winds-Horizontal-and-Vertical
#### data_fusion/yaml_configs/product_inputs/multi.yaml
* Add "Layered-Winds" products to multi product_inputs:
   * Layered-Winds-Default
   * Layered-Winds-Two-Colorbars
   * Layered-Winds-Horizontal-Adjust
   * Layered-Winds-Vertical-Default
   * Layered-Winds-Vertical-Adjust
   * Layered-Winds-Horizontal-and-Vertical
#### data_fusion/yaml_configs/product_params/Layered.yaml
* Template "xarray_dict_to_output_format" product type
#### tests/outputs/Layered-Winds-Default_image/20220911.132801.multi.multi.Layered-Winds-Default.tc2022wp14muifa.41p03.multi.1p0.png
* Default image output for "layered" functionality
#### tests/outputs/Layered-Winds-Horizontal-Adjust_image/20220911.132801.multi.multi.Layered-Winds-Horizontal-Adjust.tc2022wp14muifa.41p03.multi.1p0.png
* Image output for layered functinality with adjustments to horizontal colorbars
#### tests/outputs/Layered-Winds-Horizontal-and-Vertical_image/20220911.132801.multi.multi.Layered-Winds-Horizontal-and-Vertical.tc2022wp14muifa.41p03.multi.1p0.png
* Image output for layered functinality with adjustments to both horizontal and vertical colorbars
#### tests/outputs/Layered-Winds-Two-Colorbars_image/20220911.132801.multi.multi.Layered-Winds-Two-Colorbars.tc2022wp14muifa.41p03.multi.1p0.png
* Image output for layered functinality with default options with only 2 colorbars specified
#### tests/outputs/Layered-Winds-Vertical-Adjust_image/20220911.132801.multi.multi.Layered-Winds-Vertical-Adjust.tc2022wp14muifa.41p03.multi.1p0.png
* Image output for layered functinality with adjustments to vertical colorbars
#### tests/outputs/Layered-Winds-Vertical-Default_image/20220911.132801.multi.multi.Layered-Winds-Vertical-Default.tc2022wp14muifa.41p03.multi.1p0.png
* Image output for layered functinality with default vertical colorbars
#### data_fusion/yaml_configs/product_params/Layered-Winds-Horizontal-Adjust.yaml
* Test adjustements to multiple horizontal colorbars
#### data_fusion/yaml_configs/product_params/Layered-Winds-Horizontal-and-Vertical.yaml
* Test adjustements to multiple horizontal and vertical colorbars
#### data_fusion/yaml_configs/product_params/Layered-Winds-Vertical-Adjust.yaml
* Test adjustements to multiple vertical colorbars
#### data_fusion/yaml_configs/product_params/Layered-Winds-Vertical-Default.yaml
* Test default multiple vertical colorbars


# v1.5.2: 2022-09-16, finalize procflow, and use single_source utils

## GEOIPS#7: 2022-08-31, full data_fusion capability

### Refactor
* **data_fusion/interface_modules/procflows/data_fusion.py**
    * Removed the bulk of data_fusion "get_alg_xarray" (renamed remaining pieces "get_fused_xarray"), and
      use shared single_source get_alg_xarray routine
    * Removed "pad_area_definition" function, updated single_source pad_area_definition to support variable
      scale factors, and to allow padding for non-TC sectors.

### Improvements
* **data_fusion/interface_modules/procflows/data_fusion.py**
    * Use single_source procflow get_alg_xarray, rather than copying here and slightly modifying.
    * get_fused_xarray loops over all datasets and calls get_alg_xarray on each, then applies final algorithm
      to ALL preprocessed datasets.
    * Support "pad_area_definition" specification in product YAML configs, specifying datasets must be
      padded before reprojecting (to avoid missing data)
    * Support "dataset_name" specification in product YAML configs, else defaults to {fuse_data_name}_{product_name}
    * Support xarray.Dataset or dict of xarray.Dataset returns from final get_fused_xarray
        * xarray_dict[final_product_name] is used as single "alg_xarray" to plot_data, for setting up filenames, etc
        * xarray_dict is used for actual plotting, if defined
    * Support 'unmodified' product types within get_fused_xarray


# v1.5.1: 2022-07-13, update test outputs, geoips2->geoips

### Test Repo Updates
* **Test image outputs**
    * Updated cartopy to 0.20.2, matplotlib to v3.5.2, and natural-earth-vector to 5.2.0
    * test repo outputs incompatible with matplotlib < 3.5.2, cartopy < 0.20.2, and natural-earth-vector < 5.2.0
    * Older versions have gridlines that slighter differ around coastlines from later versions
    * Exclusively a qualitative difference, but it *does* cause the test comparisons to fail
* **Consolidate test outputs**
    * Move test output from test\_data\_fusion to data\_fusion/tests/outputs/Infrared-Gray\_image

### Refactor
* **File modifications**
    * Update all instances of 'geoips2' with 'geoips'
    * Update all instances of 'GEOIPS2' with 'GEOIPS'
* **Setup standardization**
    * Replace 'setup\_data\_fusion.sh install\_data\_fusion' with 'setup.sh install'

### Documentation Updates
* Update \*.md Distro statement headers to use 4 spaces prefix rather than ### (formatting improvement)


# v1.4.5: 2022-03-19, compare_paths->compare_path

### Refactor
* Update data_fusion procflow to use compare_path rather than compare_paths for consistency/accuracy
    (never use more than one compare_path via command line)


# v1.4.0: 2022-01-11, function updates to support modular metadata requests

### Refactor
    * Function updates to support modular metadata requests
        * Update remove_duplicates call signature
        * Update plot_data call signature


# v1.3.0: 2021-11-24, sector_type 'atcf'->'tc', --atcfdb->tcdb, --atcfdb_sectorlist->tcdb_sectorlist

### Refactor
    * Update naming from atcf to tc
        * sector_type atcf -> tc
        * --atcfdb -> tcdb
        * --atcfdb_sectorlist -> tcdb_sectorlist


# v1.2.5: 2021-11-18, updated to standard interfaces

### Improvements
    * Updated all modules to comply with standard interfaces, to pass test_interfaces.py
        * alg.py - stitched.py
        * procflow.py - data_fusion.py


# v1.2.3: 2021-11-05, update to use dictionaries of xarrays internally, simplify test scripts

### Improvements
    * Replace lists of xarrays with dictionaries of xarrays within data_fusion procflow
    * Replace "old" testing construct with simplified test scripts containing explicit command line calls


# v1.2.2: 2021-10-25, geostationary stitching using modular data fusion capability

### Major New Functionality
    * Data fusion capability - initial implementation of geostationary satellite stitching
        * data_fusion procflow
        * Stitched product for blending between satellites
            * Pass "fuse_product" associated with each "fuse_files" argument to determine which products to blend
        * data_fusion exhaustive test script


