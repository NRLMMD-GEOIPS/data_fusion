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

"""Data manipulation steps for "stitched" algorithm."""

# Installed Libraries
import logging
import numpy as np
import xarray

LOG = logging.getLogger(__name__)

interface = "algorithms"
family = "xarray_dict_to_xarray"
name = "stitched"


def call(xarray_dict, parallax_correction=True, satzen_correction=True):
    """
    Algorithm for stitching multiple datasets into a single combined product.

    Parameters
    ----------
    xobj : dict of xarray.Dataset
        Dictionary of xarray datasets, one dataset for each satellite/sensor
        that will be stitched into the final image.
    parallax_correction : bool, default=True
        Not currently implemented, will provide mechanism for reducing blurriness
        between satellites.  Currently just turns off MSG-1 in favor of Himawari-8.
    satzen_correction : bool, default=True
        If True, implement satellite zenith correction between satellites, giving
        precedence to the satellite that is closer to center of scan.  Without
        parallax correction, this causes some blurriness in the overlap region
        between satellites where there are high clouds.

    Returns
    -------
    xarray.Dataset
        xarray Dataset containing the final stitched dataset.
    """
    # This will change when blending polar!!
    metadata_xobj = xarray_dict.pop("METADATA")
    primary_area_definition = metadata_xobj.attrs["area_definition"]
    primary_sector_shape = primary_area_definition.shape
    merged_data_array = np.ma.masked_all(primary_sector_shape)
    partial_data_array = np.ma.masked_all(primary_sector_shape)
    # satzen_array = np.ma.masked_all(primary_sector_shape)
    start_datetime = metadata_xobj.attrs["start_datetime"]
    end_datetime = metadata_xobj.attrs["end_datetime"]
    final_product_name = metadata_xobj.attrs["product_name"]
    final_source_name = metadata_xobj.attrs["source_name"]
    final_platform_name = metadata_xobj.attrs["platform_name"]
    final_data_provider = metadata_xobj.attrs["data_provider"]
    final_prod_plugin = metadata_xobj.attrs["product_plugin"]

    source_names = []
    platform_names = []

    for curr_xarray in sorted(xarray_dict.values(), key=lambda xobj: (xobj.fuse_order)):
        source_names += [curr_xarray.source_name]
        platform_names += [curr_xarray.platform_name]
        if curr_xarray.start_datetime < start_datetime:
            start_datetime = curr_xarray.start_datetime
        if curr_xarray.end_datetime > end_datetime:
            end_datetime = curr_xarray.end_datetime
        currdata = np.ma.masked_all(primary_sector_shape)
        # Pull the min/max lines/samples out of the config file for the
        # current subsector.
        # This determines where the current data will go in the primary sector.
        curr_sector_shape = curr_xarray.area_definition.shape
        varname = curr_xarray.product_name

        # Pull the min/max lines/samples out of the config file for the
        # current subsector.
        # This determines where the current data will go in the primary sector.
        min_sample = 0
        min_line = 0
        max_sample = curr_sector_shape[1]
        max_line = curr_sector_shape[0]
        # Put the subsector data in the appropriate location in the primary sector
        currdata[min_line:max_line, min_sample:max_sample] = np.ma.masked_invalid(
            curr_xarray[varname]
        )
        # Major parallax issues between msg-1 and himawari-8, but this needs a
        # more intelligent fix than this.
        # Maybe blend into this box using logic similar to below ?
        if curr_xarray.platform_name == "msg-1" and parallax_correction:
            currdata = np.ma.masked_where(
                (
                    (curr_xarray["longitude"] > 70)
                    & (curr_xarray["latitude"] < 30)
                    & (curr_xarray["latitude"] > -30)
                ),
                currdata,
            )

        # Once we have an existing merged data array for the current channel,
        # merge the current subsector data into the existing final data array.
        # Note this puts the first image we find on top, and it stays there.
        # MLS3 Note this where we would blend the arrays together to make a
        # prettier picture without sharp transitions.  There would be an extra
        # line creating a "blended_data_array" which smooths the transitions
        # between currdata and merged_data_array, then merged_data_array[channame]
        # would be replaced with "blended_data_array" in the np.ma.where call
        # below. Or, use the same line below, and update merged_data_array[channame]
        # with the blended values prior to calling np.ma.where.

        LOG.info(
            " Adding %s %s %s %s %s data, %0.2f coverage ... ",
            curr_xarray.source_name,
            curr_xarray.platform_name,
            curr_xarray.product_name,
            curr_xarray.start_datetime,
            varname,
            np.ma.count(currdata) * 1.0 / currdata.size,
        )

        if curr_xarray[varname].to_masked_array().shape != currdata.shape:
            LOG.info("     Merging partial array, no satzen correction")
            partial_data_array = np.ma.where(
                currdata.mask == False, currdata, partial_data_array
            )
        elif satzen_correction and "satellite_zenith_angle" in curr_xarray.variables:
            overlap_inds = np.ma.where(~currdata.mask & ~merged_data_array.mask)
            currdata_inds = np.ma.where(~currdata.mask & merged_data_array.mask)
            merged_data_array[currdata_inds] = currdata[currdata_inds]
            if overlap_inds[0].size > 0:
                LOG.info(
                    "     Applying satellite_zenith_angle correction to "
                    "overlapping data"
                )
                satzen_overlap = np.radians(
                    curr_xarray["satellite_zenith_angle"].to_masked_array()[
                        overlap_inds
                    ]
                )
                merged_data_array[overlap_inds] = (
                    np.cos(satzen_overlap) * currdata[overlap_inds]
                    + (1 - np.cos(satzen_overlap)) * merged_data_array[overlap_inds]
                )
                LOG.info("        Num overlap points: %s", len(overlap_inds[0]))
            else:
                LOG.info(
                    "     No overlapping data, "
                    "not applying satellite_zenith_angle correction"
                )
            LOG.info("        Num points: %s", len(currdata_inds[0]))
            # satzen_array[currdata_inds] = np.radians(
            #     curr_xarray['satellite_zenith_angle'
            #     ].to_masked_array()[currdata_inds])
            # satzen_array[overlap_inds] = np.radians(
            #     curr_xarray['satellite_zenith_angle'
            #     ].to_masked_array()[overlap_inds])

        else:
            LOG.info(
                "     satellite_zenith_angle array not defined "
                "or satzen_correction %s not requested",
                satzen_correction,
            )
            merged_data_array = np.ma.where(
                currdata.mask == False, currdata, merged_data_array
            )

        # Tell the user what source, platform, time, channel was just merged.
        # Include the current subsector's percent coverage, as well as the
        # new fully merged array percent coverage.
        LOG.info(
            "     Added %s %s %s %s %s data, %0.2f coverage, "
            "partial coverage now %0.2f, total coverage %0.2f",
            curr_xarray.source_name,
            curr_xarray.platform_name,
            curr_xarray.product_name,
            curr_xarray.start_datetime,
            varname,
            np.ma.count(currdata) * 1.0 / currdata.size,
            np.ma.count(partial_data_array) * 1.0 / partial_data_array.size,
            np.ma.count(merged_data_array) * 1.0 / merged_data_array.size,
        )

    LOG.info("Merging partial array with full array")
    # overlap_inds = np.ma.where(~satzen_array.mask & ~partial_data_array.mask)
    # if overlap_inds[0].size > 0:
    #     satzen_overlap = np.radians(
    #         curr_xarray['satellite_zenith_angle'
    #         ].to_masked_array()[overlap_inds])
    #     merged_data_array[overlap_inds] = np.cos(satzen_overlap) * \
    #                                       merged_data_array[overlap_inds] \
    #                                       + (1 - np.cos(satzen_overlap)) * \
    #                                         partial_data_array[overlap_inds]
    merged_data_array = np.ma.where(
        merged_data_array.mask == False, merged_data_array, partial_data_array
    )

    LOG.info(
        "     Final coverage %0.2f",
        np.ma.count(merged_data_array) * 1.0 / merged_data_array.size,
    )

    final_xarray = xarray.Dataset()
    final_xarray[final_product_name] = xarray.DataArray(merged_data_array)
    final_xarray.attrs["product_name"] = final_product_name
    final_xarray.attrs["area_definition"] = primary_area_definition
    final_xarray.attrs["source_names"] = source_names
    final_xarray.attrs["platform_names"] = platform_names
    final_xarray.attrs["source_name"] = final_source_name
    final_xarray.attrs["platform_name"] = final_platform_name
    final_xarray.attrs["start_datetime"] = start_datetime
    final_xarray.attrs["end_datetime"] = end_datetime
    final_xarray.attrs["data_provider"] = final_data_provider
    final_xarray.attrs["product_plugin"] = final_prod_plugin
    lons, lats = final_xarray.area_definition.get_lonlats()
    final_xarray["latitude"] = xarray.DataArray(lats)
    final_xarray["longitude"] = xarray.DataArray(lons)

    # Put xarray_dict back the way we found it.  We popped it off earlier in
    # order to ensure we had just the data xarray objects when looping through.
    xarray_dict["METADATA"] = metadata_xobj

    return final_xarray
