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

'''Read @my_data@ data products'''

# Please identify instances of @ within this reader file, and update appropriately.

import logging
from os.path import basename
from datetime import datetime
import xarray
LOG = logging.getLogger(__name__)

reader_type = 'standard'


def @my_reader@(fnames, metadata_only=False, chans=None, area_def=None, self_register=False):
    ''' Read @my_data@ data products.

    All GeoIPS 'standard' type readers read data into xarray Datasets - a separate
    dataset for each shape/resolution of data - and contain standard metadata information.

    Args:
        fnames (list): List of strings, full paths to files
        metadata_only (Optional[bool]):
            * DEFAULT False
            * return before actually reading data if True
        chans (Optional[list of str]):
            * DEFAULT None (include all channels)
            * List of desired channels (skip unneeded variables as needed)
        area_def (Optional[pyresample.AreaDefinition]):
            * NOT YET IMPLEMENTED
                * DEFAULT None (read all data)
                * Specify region to read
        self_register (Optional[str]):
            * NOT YET IMPLEMENTED
                * DEFAULT False (read multiple resolutions of data)
                * register all data to the specified resolution.

    Returns:
        dict of xarray.Datasets: dict of xarray.Dataset objects with required
            Variables and Attributes: (See geoips/docs :doc:`xarray_standards`),
            dict key can be any descriptive dataset id
   '''

    # Populate dictionary of xarray Datasets - one xarray object for each resolution of data, and the special
    # METADATA dictionary key with only metadata.
    xarrays = {}

    # Create an xarray dataset to contain metadata
    meta_xarray = xarray.Dataset()
    meta_xarray.attrs['original_source_filenames'] = []

    for fname in fnames:
        # populate metadata appropriately as needed
        LOG.info('Read data from %s', fname)
        meta_xarray = xarray.open_dataset(str(fname))
        meta_xarray.attrs['original_source_filenames'] += [basename(fname)]

    # Required metadata
    meta_xarray.attrs['data_provider'] = '@data_provider@'
    meta_xarray.attrs['source_name'] = '@source_name@'
    meta_xarray.attrs['platform_name'] = '@platform_name@'
    meta_xarray.attrs['interpolation_radius_of_influence'] = @ROI_int@  # Around the size of the sensor footprint
    meta_xarray.attrs['minimum_coverage'] = 20

    # Pull start and end datetime from data appropriately
    meta_xarray.attrs['start_datetime'] = @datetime.strptime(meta_xarray.attrs['time_coverage_start'][0:19],
                                                            '%Y-%m-%dT%H:%M:%S')@
    meta_xarray.attrs['end_datetime'] = @datetime.strptime(meta_xarray.attrs['time_coverage_end'][0:19],
                                                          '%Y-%m-%dT%H:%M:%S')@

    # Return metadata without reading data yet.
    if metadata_only is True:
        LOG.info('metadata_only requested, returning without readind data')
        return {'METADATA': meta_xarray}

    # Now actually populate the data

    # Variable names will be used in product parameter YAML files to specify which variables should be used
    # for which products.
    xarrays['@DS1@'] = xarray.Dataset()
    xarrays['@DS1@'].attrs = meta_xarray.attrs.copy()  # Populate @attributes appropriately
    xarrays['@DS1@']['latitude'] = @must have 2d array of latitudes for each dataset@
    xarrays['@DS1@']['longitude'] = @must have 2d array of longitudes for each dataset@
    xarrays['@DS1@']['ds1_var1'] = @must have 2d array of data for each variable that matches shape of lat/lon arrays@
    xarrays['@DS1@']['ds1_var2'] = @must have 2d array of data for each variable that matches shape of lat/lon arrays@

    xarrays['@DS2@'] = xarray.Dataset()
    xarrays['@DS2@'].attrs = meta_xarray.attrs.copy()  # Populate @attributes appropriately
    xarrays['@DS2@']['latitude'] = @must have 2d array of latitudes for each dataset@
    xarrays['@DS2@']['longitude'] = @must have 2d array of longitudes for each dataset@
    xarrays['@DS2@']['ds2_var1'] = @must have 2d array of data for each variable that matches shape of lat/lon arrays@
    xarrays['@DS2@']['ds2_var2'] = @must have 2d array of data for each variable that matches shape of lat/lon arrays@

    xarrays['METADATA'] = list(xarrays.values())[0][[]]

    return xarrays
