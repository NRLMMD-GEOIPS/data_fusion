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

import logging

import matplotlib.pyplot as plt
import matplotlib
rc_params = matplotlib.rcParams

from geoips.image_utils.mpl_utils import create_figure_and_main_ax_and_mapobj
from geoips.image_utils.mpl_utils import save_image, plot_overlays
from geoips.image_utils.mpl_utils import set_title, create_colorbar
from geoips.plugins.modules.procflows.single_source import plot_data

# New geoips interface classes
from geoips.interfaces import colormaps

# Old geoips YAML based plugins not yet implemented as class-based plugins
from geoips.dev.product import get_cmap_name, get_cmap_args
from geoips.sector_utils.utils import is_sector_type

LOG = logging.getLogger(__name__)

output_type = 'xrdict_area_product_outfnames_to_outlist'


def layered_title(area_def, xrdict):
    LOG.info('Setting dynamic title')

    title_lines = []

    if is_sector_type(area_def, 'tc'):

        # Make sure we reflect the actual start_datetime in the filename
        # geoimg_obj.set_geoimg_attrs(start_dt=xarray_obj.start_datetime)
        if 'interpolated_time' in area_def.sector_info:
            sector_time = area_def.sector_info['interpolated_time']
        else:
            sector_time = area_def.sector_info['synoptic_time']

        title_lines += ['{0}{1:02d} {2} at {3}'.format(area_def.sector_info['storm_basin'],
                                                       int(area_def.sector_info['storm_num']),
                                                       area_def.sector_info['storm_name'],
                                                       sector_time.strftime('%Y-%m-%d %H:%M:%S'))]
     
    for dataset_name in xrdict.keys():
        if dataset_name == 'METADATA':
            continue
        xarray_obj = xrdict[dataset_name]
        # data_time = xarray_obj.start_datetime + (xarray_obj.end_datetime - xarray_obj.start_datetime)/2
        data_time = xarray_obj.start_datetime
        # pandas dataframes seem to handle time objects much better than xarray.
        title_lines += ['{0} {1} {2} at {3}'.format(xarray_obj.platform_name.upper(),
                                                    xarray_obj.source_name.upper(),
                                                    xarray_obj.product_name.upper(),
                                                    data_time.strftime('%Y-%m-%d %H:%M:%S'))]

    title_string = '\n'.join(title_lines)
    LOG.info('title_string: %s', title_string)

    return title_string


def get_arg(xobj, arg_type, dataset_name, arg_name):
    # Like: xarray_dict['METADATA'].product_definition['mpl_colors_info'][xobj.dataset_name]['width']
    arg_val = None
    if hasattr(xobj, 'product_definition') \
       and arg_type in xobj.attrs['product_definition'] \
       and dataset_name in xobj.attrs['product_definition'][arg_type] \
       and arg_name in xobj.attrs['product_definition'][arg_type][dataset_name]:
        arg_val = xobj.attrs['product_definition'][arg_type][dataset_name][arg_name]
    return arg_val


def get_final_mpl_colors_info(xobj, dataset_name, product_name, source_name):

    cmap_func_name = get_cmap_name(product_name, source_name)
    cmap_func = colormaps.get_plugin(cmap_func_name)
    cmap_args = get_cmap_args(product_name, source_name)
    mpl_colors_info = cmap_func(**cmap_args)

    # New options for data_fusion / multi colorbars
    mpl_colors_info['colorbar_kwargs'] = {'orientation': 'horizontal',
                                          'extend': 'both'}
    mpl_colors_info['colorbar_positioning'] = None
    mpl_colors_info['set_ticks_kwargs'] = {'size': rc_params['font.size'] * 0.5}
    mpl_colors_info['set_label_kwargs'] = {'size': rc_params['font.size'] * 0.5}

    # Replace mpl_colors_info parameters with final product specified.
    for key in mpl_colors_info:
        curr_arg = get_arg(xobj, 'mpl_colors_info', dataset_name, key)
        if curr_arg is not None:
            if isinstance(curr_arg, dict) and isinstance(mpl_colors_info[key], dict):
                for subkey in curr_arg:
                    mpl_colors_info[key][subkey] = curr_arg[subkey]
            else:
                mpl_colors_info[key] = curr_arg

    return mpl_colors_info


def create_all_colorbars(fig, main_ax, mapobj, xarray_dict):

    horizontal_mpl_colors_info = []
    vertical_mpl_colors_info = []

    main_ax_min_x_pix = main_ax.bbox.bounds[0]
    main_ax_width_pix = main_ax.bbox.bounds[2]

    main_ax_min_y_pix = main_ax.bbox.bounds[1]
    main_ax_height_pix = main_ax.bbox.bounds[3]

    fig_min_x_pix = fig.bbox.bounds[0]
    fig_width_pix = fig.bbox.bounds[2]

    fig_min_y_pix = fig.bbox.bounds[1]
    fig_height_pix = fig.bbox.bounds[3]

    main_ax_width_percent = main_ax_width_pix / fig_width_pix
    main_ax_min_x_percent = main_ax_min_x_pix / fig_width_pix

    main_ax_height_percent = main_ax_height_pix / fig_height_pix
    main_ax_min_y_percent = main_ax_min_y_pix / fig_height_pix

    # Remove 'METADATA' from the list
    xarray_datasets = {}
    for dataset_name in xarray_dict.keys():
        if dataset_name != 'METADATA':
            xarray_datasets[dataset_name] = xarray_dict[dataset_name]

    for xobj in sorted(xarray_datasets.values(), key=lambda xobj: (xobj.order)):
        mpl_colors_info = get_final_mpl_colors_info(xarray_dict['METADATA'],
                                                    xobj.dataset_name,
                                                    xobj.attrs['product_name'],
                                                    xobj.attrs['source_name'])
        if mpl_colors_info['colorbar'] is True:
            if mpl_colors_info['colorbar_kwargs']['orientation'] == 'horizontal':
                horizontal_mpl_colors_info += [mpl_colors_info]
            elif mpl_colors_info['colorbar_kwargs']['orientation'] == 'vertical':
                vertical_mpl_colors_info += [mpl_colors_info]


    ##########################################################################################################
    ###
    ### We are separating horizontal and vertical colorbars here only for generating reasonable defaults
    ###
    ### By default, vertical will be placed on the right, and horizontal along the bottom.
    ### Separating vertical and horizontal allows calculating the exact locations based on the number of each
    ###
    ### If full "colorbar_positioning" is specified, they will be placed as requested, regardless of the
    ### number of horizontal vs vertical colorbars
    ###
    ##########################################################################################################

    num_cmaps = {}
    gap = {}
    full_width = {}
    cbar_fraction = {}
    start_pos = {}

    num_cmaps['horizontal'] = len(horizontal_mpl_colors_info)
    num_cmaps['vertical'] = len(vertical_mpl_colors_info)

    # Set values used for calculating horizontal and vertical defaults, in case needed
    if num_cmaps['horizontal']:
        gap['horizontal'] = (main_ax_width_percent) / (num_cmaps['horizontal']*10)
        full_width['horizontal'] = main_ax_width_percent - (num_cmaps['horizontal']-1)*gap['horizontal']
        cbar_fraction['horizontal'] = 1.0 / num_cmaps['horizontal']
        start_pos['horizontal'] = main_ax_min_x_percent

    if num_cmaps['vertical']:
        gap['vertical'] = main_ax_height_percent / (num_cmaps['vertical']*10)
        full_width['vertical']  = main_ax_height_percent - (num_cmaps['vertical']-1)*gap['vertical']
        cbar_fraction['vertical'] = 1.0 / num_cmaps['vertical']
        start_pos['vertical'] = main_ax_min_y_percent

    # Now start creating each colorbar, based on information in mpl_colors_info dictionaries
    for mpl_colors_info in horizontal_mpl_colors_info+vertical_mpl_colors_info:

        orientation = mpl_colors_info['colorbar_kwargs']['orientation']

        # Provide defaults if "colorbar_positioning" is None
        if mpl_colors_info['colorbar_positioning'] is None:

            # Provide the defaults for vertical colorbars, if colorbar_positioning is not set
            if mpl_colors_info['colorbar_kwargs']['orientation'] == 'vertical':

                # This is to match the "old" start position of 0.005 cbar_top_offset relative to fig
                # start_x_pos = 1.0064516129032257
                start_x_pos = (main_ax_width_percent + 0.005) / main_ax_width_percent

                # This is to match the "old" cbar_height of 0.02, relative to fig
                # end_x_pos = 1.032258064516129
                end_x_pos = (0.02 / main_ax_width_percent) + start_x_pos

                start_y_pos = (start_pos['vertical'] - main_ax_min_y_percent) / main_ax_height_percent
                end_y_pos = (full_width['vertical']*cbar_fraction['vertical']/main_ax_height_percent) + start_y_pos

            # Provide the defaults for horizontal colorbars if "colorbar_positioning" is not specified
            if mpl_colors_info['colorbar_kwargs']['orientation'] == 'horizontal':
                start_x_pos = (start_pos['horizontal'] - main_ax_min_x_percent) / main_ax_width_percent
                end_x_pos = (full_width['horizontal']*cbar_fraction['horizontal']) / main_ax_width_percent + start_x_pos

                # This is to match the "old" start position of 0.05 cbar_bottom_offset relative to fig
                # start_y_pos = -0.07792207792207793
                start_y_pos = (0.05 - main_ax_min_y_percent) / main_ax_height_percent

                # This is to match the "old" cbar_height of 0.02, relative to fig
                # end_y_pos = -0.05194805194805195
                end_y_pos = (0.02 / main_ax_height_percent) + start_y_pos

            mpl_colors_info['colorbar_positioning'] = {}
            mpl_colors_info['colorbar_positioning']['start_y_pos'] = start_y_pos
            mpl_colors_info['colorbar_positioning']['end_y_pos'] = end_y_pos
            mpl_colors_info['colorbar_positioning']['start_x_pos'] = start_x_pos
            mpl_colors_info['colorbar_positioning']['end_x_pos'] = end_x_pos

            # Start the next one + gap
            start_pos[orientation] = start_pos[orientation] \
                                     + full_width[orientation]*cbar_fraction[orientation] \
                                     + gap[orientation]

        # These are relative to main_ax
        cbar_ax_min_x_percent = mpl_colors_info['colorbar_positioning']['start_x_pos']
        cbar_ax_min_y_percent = mpl_colors_info['colorbar_positioning']['start_y_pos']
        cbar_ax_max_x_percent = mpl_colors_info['colorbar_positioning']['end_x_pos']
        cbar_ax_max_y_percent = mpl_colors_info['colorbar_positioning']['end_y_pos']

        # These are relative to fig
        cbar_ax_left_start_pos = main_ax_min_x_percent + (cbar_ax_min_x_percent * main_ax_width_percent)
        cbar_ax_width = (cbar_ax_max_x_percent - cbar_ax_min_x_percent) * main_ax_width_percent

        cbar_ax_bottom_start_pos = main_ax_min_y_percent + (cbar_ax_min_y_percent * main_ax_height_percent)
        cbar_ax_height = (cbar_ax_max_y_percent - cbar_ax_min_y_percent) * main_ax_height_percent

        # These fields are what are actually used within "create_colorbar" for placing the colorbar
        # Explicit "axes" locations for the new colorbar axis, relative to the overall FIGURE, not the MAIN AX
        # 
        # We are using x/y start/end positions relative to the MAIN AXIS in order to calculate the final
        # colorbar axis positions relative to the FIGURE.
        mpl_colors_info['cbar_ax_left_start_pos'] = cbar_ax_left_start_pos
        mpl_colors_info['cbar_ax_bottom_start_pos'] = cbar_ax_bottom_start_pos
        mpl_colors_info['cbar_ax_width'] = cbar_ax_width
        mpl_colors_info['cbar_ax_height'] = cbar_ax_height

        create_colorbar(fig, mpl_colors_info)

    return


def layered_imagery(xarray_dict,
                    area_def,
                    product_name,
                    output_fnames,
                    boundaries_info=None,
                    gridlines_info=None,
                    title_format=None,
                    title_copyright=None):

    # Create matplotlib figure and main axis, where the main image will be plotted
    fig, main_ax, mapobj = create_figure_and_main_ax_and_mapobj(area_def.x_size,
                                                                area_def.y_size,
                                                                area_def,
                                                                noborder=False)

    # Remove 'METADATA' from the list
    xarray_datasets = {}
    for dataset_name in xarray_dict.keys():
        if dataset_name != 'METADATA':
            xarray_datasets[dataset_name] = xarray_dict[dataset_name]
        
    for xobj in sorted(xarray_datasets.values(), key=lambda xobj: (xobj.order)):
        output_kwargs = {'fig': fig, 'main_ax': main_ax, 'mapobj': mapobj}
        if isinstance(xobj, dict):
            curr_product_name = xobj['METADATA'].attrs['product_name']
            curr_output_dict = xobj['METADATA'].attrs
        else:
            curr_product_name = xobj.attrs['product_name']
            curr_output_dict = xobj.attrs
        plot_data(curr_output_dict,
                  xobj,
                  area_def,
                  curr_product_name,
                  output_kwargs,
                  no_output=True)

    # Use METADATA xobj for title
    title_string = layered_title(area_def, xarray_dict)
    set_title(main_ax, title_string, area_def.y_size)

    # Plot gridlines and boundaries overlays
    plot_overlays(mapobj, main_ax, area_def, 
                  boundaries_info=boundaries_info, 
                  gridlines_info=gridlines_info,
                  boundaries_zorder=3, gridlines_zorder=3)

    create_all_colorbars(fig, main_ax, mapobj, xarray_dict)

    success_outputs = []
    if output_fnames is not None:
        for annotated_fname in output_fnames:
            # Save the final image
            # Use METADATA xobj for datetime
            success_outputs += save_image(fig, annotated_fname, is_final=True,
                                          image_datetime=xarray_dict['METADATA'].start_datetime)

    return success_outputs

