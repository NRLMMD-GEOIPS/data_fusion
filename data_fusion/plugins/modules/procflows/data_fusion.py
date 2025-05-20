# # # This source code is subject to the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

"""Driver for standard single channel products."""

import logging
from os import getenv

import xarray

# New class-based interfaces
from geoips.errors import PluginError
from geoips.interfaces import algorithms
from geoips.interfaces import readers
from geoips.interfaces import products
from geoips.interfaces import output_checkers

from geoips.filenames.duplicate_files import remove_duplicates


# Old interfaces (YAML, not updated to classes yet!)
from geoips.dev.product import (
    get_required_variables,
    get_covg_args_from_product,
)

# Direct imports from single_source
from geoips.plugins.modules.procflows.single_source import (
    pad_area_definition,
    get_alg_xarray,
    get_area_defs_from_command_line_args,
    plot_data,
    get_output_formatter_kwargs,
)

from data_fusion.commandline.args import check_command_line_args
from geoips.utils.context_managers import import_optional_dependencies

with import_optional_dependencies(loglevel="info"):
    """Attempt to import a package and print to LOG.info if the import fails."""
    from geoips_db.utils.database_writes import write_stats_to_database

from geoips.utils.memusg import print_mem_usage

PMW_NUM_PIXELS_X = 1400
PMW_NUM_PIXELS_Y = 1400
PMW_PIXEL_SIZE_X = 1000
PMW_PIXEL_SIZE_Y = 1000

LOG = logging.getLogger(__name__)

interface = "procflows"
family = "standard"
name = "data_fusion"


def get_overall_start_datetime(fuse_dict):
    """Get the starting datetime for all products."""
    min_start_datetime = None
    for fuse_name in fuse_dict:
        if (
            "metadata_xobj" in fuse_dict[fuse_name]
            and "start_datetime" in fuse_dict[fuse_name]["metadata_xobj"].attrs
            and (
                min_start_datetime is None
                or fuse_dict[fuse_name]["metadata_xobj"].attrs["start_datetime"]
                < min_start_datetime
            )
        ):
            min_start_datetime = fuse_dict[fuse_name]["metadata_xobj"].attrs[
                "start_datetime"
            ]
    return min_start_datetime


def get_overall_end_datetime(fuse_dict):
    """Get the ending datetime for all products."""
    max_end_datetime = None
    for fuse_name in fuse_dict:
        if (
            "metadata_xobj" in fuse_dict[fuse_name]
            and "end_datetime" in fuse_dict[fuse_name]["metadata_xobj"].attrs
            and (
                max_end_datetime is None
                or fuse_dict[fuse_name]["metadata_xobj"].attrs["end_datetime"]
                > max_end_datetime
            )
        ):
            max_end_datetime = fuse_dict[fuse_name]["metadata_xobj"].attrs[
                "end_datetime"
            ]
    return max_end_datetime


def unpack_fusion_arguments(argdict):
    """Unpack fusion arguments."""
    fusion_files = argdict["fuse_files"]
    fusion_readers = argdict["fuse_reader_name"]
    fusion_products = argdict["fuse_product_name"]
    fusion_outputs = argdict["fuse_output_format"]
    fusion_orders = argdict["fuse_order"]
    fusion_dataset_names = argdict["fuse_dataset_name"]
    fusion_self_register_sources = argdict["fuse_self_register_source"]
    fusion_self_register_platforms = argdict["fuse_self_register_platform"]
    fusion_self_register_datasets = argdict["fuse_self_register_dataset"]
    fusion_sectored_reads = argdict["fuse_sectored_read"]
    fusion_resampled_reads = argdict["fuse_resampled_read"]

    requested_fusion = {}

    curr_num = 0
    for fusion_file_list in fusion_files:
        # reader_name and product_name required - just pull those directly
        fusion_reader_name = fusion_readers[curr_num]
        fusion_product_name = fusion_products[curr_num]
        fusion_dataset_name = fusion_dataset_names[curr_num]
        reader_func = readers.get_plugin(fusion_reader_name)
        meta = reader_func(fusion_file_list, metadata_only=True)
        source_name = meta["METADATA"].attrs["source_name"]

        curr_fuse_dict = {
            "reader_name": fusion_reader_name,
            "reader_func": reader_func,
            "files": fusion_file_list,
            "product_name": fusion_product_name,
            "source_name": source_name,
            "dataset_name": fusion_dataset_name,
            "metadata_xobj": meta["METADATA"],
        }

        # All other "fuse_*" arguments are optional - but if included, must be
        # included for each dataset.
        # If number arguments equals number of fusion datasets, include in dictionary
        if fusion_outputs:
            curr_fuse_dict["output_formatter"] = fusion_outputs[curr_num]
        if fusion_orders:
            curr_fuse_dict["fuse_order"] = fusion_orders[curr_num]
        if fusion_self_register_sources:
            curr_fuse_dict["self_register_source"] = fusion_self_register_sources[
                curr_num
            ]
        if fusion_self_register_platforms:
            curr_fuse_dict["self_register_platform"] = fusion_self_register_platforms[
                curr_num
            ]
        if fusion_self_register_datasets:
            curr_fuse_dict["self_register_dataset"] = fusion_self_register_datasets[
                curr_num
            ]
        if fusion_sectored_reads:
            curr_fuse_dict["sectored_read"] = fusion_sectored_reads[curr_num]
        if fusion_resampled_reads:
            curr_fuse_dict["resampled_read"] = fusion_resampled_reads[curr_num]
        if "fuse_reader_kwargs" in argdict and argdict["fuse_reader_kwargs"]:
            curr_fuse_dict["reader_kwargs"] = argdict["fuse_reader_kwargs"][curr_num]
        # Populate each individual fused dataset
        requested_fusion[fusion_dataset_name] = curr_fuse_dict
        curr_num = curr_num + 1

    # This is the requested final product info
    overall_start_datetime = get_overall_start_datetime(requested_fusion)
    overall_end_datetime = get_overall_end_datetime(requested_fusion)
    requested_fusion["final"] = {
        "product_name": argdict["fusion_final_product_name"],
        "source_name": argdict["fusion_final_source_name"],
        "platform_name": argdict["fusion_final_platform_name"],
        "output_format": argdict["fusion_final_output_formatter"],
        "start_datetime": overall_start_datetime,
        "end_datetime": overall_end_datetime,
    }
    final_metadata_xobj = xarray.Dataset()
    final_metadata_xobj.attrs["source_name"] = requested_fusion["final"]["source_name"]
    final_metadata_xobj.attrs["product_name"] = requested_fusion["final"][
        "product_name"
    ]
    final_metadata_xobj.attrs["platform_name"] = requested_fusion["final"][
        "platform_name"
    ]
    final_metadata_xobj.attrs["output_format"] = requested_fusion["final"][
        "output_format"
    ]
    final_metadata_xobj.attrs["start_datetime"] = requested_fusion["final"][
        "start_datetime"
    ]
    final_metadata_xobj.attrs["end_datetime"] = requested_fusion["final"][
        "end_datetime"
    ]
    final_metadata_xobj.attrs["data_provider"] = "multi"
    requested_fusion["final"]["metadata_xobj"] = final_metadata_xobj

    return requested_fusion


def get_fused_xarray(area_def, fuse_data, command_line_args):
    """
    Get the fused xarray.

    This loops through each "fuse" dataset, and calls single_source.get_alg_xarray
    to pre-process each appropriately. After pre-processing each dataset to their
    individual "products", the final algorithm is applied to all datasets.
    """
    from geoips.xarray_utils.data import sector_xarrays

    final_product_name = fuse_data["final"]["product_name"]
    final_source_name = fuse_data["final"]["source_name"]
    final_prod_plugin = products.get_plugin(final_source_name, final_product_name)
    final_covg_args = get_covg_args_from_product(final_prod_plugin)

    metadata_xobj = fuse_data["final"]["metadata_xobj"]
    coverage_dataset = None

    interp_xarrays = {}
    # variables = get_required_variables(product_name, sect_xarrays[0].source_name)
    for fuse_data_name in fuse_data:
        # 'final' fusion dataset is included within this dictionary - skip those.
        # We only want to read the individual fusion datasets here.
        if fuse_data_name == "final":
            continue
        product_name = fuse_data[fuse_data_name]["product_name"]
        source_name = fuse_data[fuse_data_name]["source_name"]
        reader = fuse_data[fuse_data_name]["reader_func"]
        files = fuse_data[fuse_data_name]["files"]
        prod_plugin = products.get_plugin(source_name, product_name)
        required_variables = get_required_variables(prod_plugin)

        # We are checking to see if there are any additional variables required
        # for this particular combined final_product_name for the current
        # source.
        # This could be things like "satellite_zenith_angle" for blending between
        # satellites, etc.
        try:
            # Attempt to load a product plugin that may or may not exist. Use
            # call_number=-1, as this denotes that we should fail quickly and not
            # rebuild the plugin registry if this plugin cannot be found
            final_prod_plugin_for_curr_source = products.get_plugin(
                source_name, final_product_name, call_number=-1
            )
            # If variables are specified within the "final_product" definition
            # in product_inputs/<source_name>.yaml, Then append them to the
            # required_variables list here (if variables not specified, nothing
            # to add)
            additional_vars = get_required_variables(final_prod_plugin_for_curr_source)
            if additional_vars:
                required_variables += list(set(additional_vars))
            else:
                raise PluginError
        except PluginError:
            LOG.info(
                "No additional requirements for source %s / final product %s",
                source_name,
                final_product_name,
            )

        # If "pad_area_definition" was requested in the individual
        # "fuse_product" within product_inputs/<source_name>.yaml,
        # then pad appropriately here.  If a product is missing some
        # data after reprojecting, you may need to pad.
        prod_plugin = products.get_plugin(
            source_name, product_name, command_line_args["product_spec_override"]
        )

        unsectored_product_types = [
            "unsectored_xarray_dict_to_output_format",
            "unsectored_xarray_dict_area_to_output_format",
            "unmodified",
        ]

        if (
            prod_plugin.family not in unsectored_product_types
            and "pad_area_definition" in prod_plugin["spec"]
            and prod_plugin["spec"]["pad_area_definition"]
        ):
            xscale = prod_plugin["spec"].get("pad_x_scale_factor", 1.5)
            yscale = prod_plugin["spec"].get("pad_y_scale_factor", 1.5)
            pad_area_def = pad_area_definition(
                area_def, force_pad=True, x_scale_factor=xscale, y_scale_factor=yscale
            )
        else:
            pad_area_def = area_def

        if "reader_kwargs" in fuse_data[fuse_data_name]:
            reader_kwargs = fuse_data[fuse_data_name]["reader_kwargs"]
        else:
            reader_kwargs = {}
        # Read the padded area definition (ensure we have enough data to cover
        # the entire sector after reprojecting
        reader_out = reader(
            files,
            metadata_only=False,
            chans=required_variables,
            area_def=pad_area_def,
            **reader_kwargs,
        )

        if prod_plugin.family not in unsectored_product_types:
            pad_sect_xarrays = sector_xarrays(
                reader_out, pad_area_def, required_variables
            )
        else:
            pad_sect_xarrays = reader_out

        # Is this any different from the previous `prod_plugin?`
        prod_plugin = products.get_plugin(
            pad_sect_xarrays["METADATA"].source_name,
            product_name,
        )
        # dataset_name is {dataset_name} for uniqueness.
        dataset_name = fuse_data[fuse_data_name]["dataset_name"]

        alg_product_types = [
            "algorithm",
            "interpolator_algorithm",
            "interpolator_algorithm_colormapper",
            "algorithm_interpolator_colormapper",
            "algorithm_colormapper",
            "colormapper",
        ]
        interp_only_product_types = ["interpolator"]
        noalg_product_types = [
            "sectored_xarray_dict_to_output_format",
            "sectored_xarray_dict_area_to_output_format",
            "unsectored_xarray_dict_to_output_format",
            "xarray_dict_to_output_format",
            "unsectored_xarray_dict_area_to_output_format",
            "unmodified",
        ]
        # If we need interpolation or an algorithm applied, call get_alg_xarray
        # from single_source procflow
        if prod_plugin.family in alg_product_types + interp_only_product_types:
            interp_xarrays[dataset_name] = get_alg_xarray(
                pad_sect_xarrays,
                area_def,
                prod_plugin,
                variable_names=required_variables,
                resector=False,
                resampled_read=False,
            )
            interp_xarrays[dataset_name].attrs["product_plugin"] = prod_plugin
            # Set all the fuse_data attrs on the xarray obj itself
            for attrname in fuse_data[dataset_name].keys():
                if attrname == "metadata_xobj":
                    continue
                interp_xarrays[dataset_name].attrs[attrname] = fuse_data[dataset_name][
                    attrname
                ]
        # If no modification required to data, just set pad_sect_xarrays to
        # interp_xarrays[dataset_name]
        elif prod_plugin.family in noalg_product_types:
            interp_xarrays[dataset_name] = pad_sect_xarrays
            interp_xarrays[dataset_name]["METADATA"].attrs[
                "product_plugin"
            ] = prod_plugin
            # Set all the fuse_data attrs on the METADATA xarray obj
            for attrname in fuse_data[dataset_name].keys():
                if attrname == "metadata_xobj":
                    continue
                interp_xarrays[dataset_name]["METADATA"].attrs[attrname] = fuse_data[
                    dataset_name
                ][attrname]
        else:
            raise ValueError(
                f"Product type {prod_plugin.family} must be one of "
                f"{alg_product_types}, {interp_only_product_types}, or "
                f"{noalg_product_types}"
            )

        # Variable names can be specified as dataset:variable, so determine both
        # dataset name and variable name for the coverage checker.
        covg_dsname = None
        covg_varname = final_covg_args.get("variable_name")

        # If there is a ":" in the requested variable name, split out the dataset
        # name and variable name.
        if covg_varname and ":" in covg_varname:
            covg_dsname, covg_varname = covg_varname.split(":")

        # If this is the requested dataset name, use this dataset.
        if covg_dsname == dataset_name:
            LOG.info(
                "Using requested dataset %s variable %s for coverage",
                covg_dsname,
                covg_varname,
            )
            coverage_dataset = interp_xarrays[dataset_name]
        # If no dataset name was requested, and this dataset includes the variable,
        # use this dataset.
        elif not covg_dsname and covg_varname in interp_xarrays[dataset_name]:
            LOG.info(
                "Now using dataset %s variable %s for coverage",
                dataset_name,
                covg_varname,
            )
            coverage_dataset = interp_xarrays[dataset_name]
        else:
            LOG.info(
                "NOT using dataset %s for coverage",
                dataset_name,
            )

    # Set METADATA xarray object on interp_xarrays dictionary, for consistency
    interp_xarrays["METADATA"] = metadata_xobj
    # Use start and end datetime, and variables from coverage_dataset (leave the
    # rest the same as METADATA)
    if coverage_dataset:
        interp_xarrays["METADATA"].attrs["start_datetime"] = coverage_dataset.attrs[
            "start_datetime"
        ]
        interp_xarrays["METADATA"].attrs["end_datetime"] = coverage_dataset.attrs[
            "end_datetime"
        ]
        for product_name in coverage_dataset.keys():
            interp_xarrays["METADATA"][product_name] = coverage_dataset[product_name]
    # Attach the final product information to the METADATA xarray
    interp_xarrays["METADATA"].attrs["product_plugin"] = final_prod_plugin
    # Attach the area_def information to the METADATA xarray
    interp_xarrays["METADATA"].attrs["area_definition"] = area_def
    interp_xarrays["METADATA"].attrs["product_name"] = final_prod_plugin.name

    no_alg_product_types = [
        "sectored_xarray_dict_to_output_format",
        "sectored_xarray_dict_area_to_output_format",
        "unsectored_xarray_dict_to_output_format",
        "unsectored_xarray_dict_area_to_output_format",
        "xarray_dict_to_output_format",
        "unmodified",
    ]

    # If no algorithm is required for the final output product, just return
    # interp_xarrays
    if final_prod_plugin.family in no_alg_product_types:
        alg_xarray = interp_xarrays
    # Else apply the fusion algorithm
    else:
        alg_xarray = run_fuse_alg(interp_xarrays, final_prod_plugin, final_source_name)
        if "product_name" not in alg_xarray.attrs:
            alg_xarray.attrs["product_name"] = final_prod_plugin.name

    return alg_xarray


def run_fuse_alg(fuse_xarrays, fuse_prod_plugin, fuse_source_name):
    """Run the fusion algorithm."""
    alg_plugin = algorithms.get_plugin(
        fuse_prod_plugin["spec"]["algorithm"]["plugin"]["name"]
    )
    alg_args = fuse_prod_plugin["spec"]["algorithm"]["plugin"]["arguments"]

    # alg_xarray will either be a single xarray Dataset, or a dictionary of
    # xarray Datasets.  single_source procflow handles them separately in
    # "plot_data" (xarray_dict[final_product_name] used for metadata,
    # xarray_dict used for actual plotting if dict based)
    if alg_plugin.family in ["xarray_dict_to_xarray", "xarray_dict_to_xarray_dict"]:
        alg_xarray = alg_plugin(fuse_xarrays, **alg_args)
    else:
        raise TypeError(
            f"Unsupported algorithm type for fusion driver: {alg_plugin.family}"
        )

    return alg_xarray


def call(fnames, command_line_args=None):
    """
    Workflow for running multiple datatypes in a single call.

    Parameters
    ----------
    fnames : list of strings
        List of strings specifying full paths to input file names to process
    command_line_args : dict, default=None
        dictionary of command line arguments

          'reader_name': Explicitly request reader

          *  geoips*.readers.readername.readername

          Optional: 'sector_list': list of str sector names

          * tc<YYYY><BASIN><NUM><NAME> for TCs,
            ie tc2020sh16gabekile

    Returns
    -------
    list
        Return list of strings specifying full paths to output products
        that were produced.
    """
    from datetime import datetime

    process_datetimes = {}
    process_datetimes["overall_start"] = datetime.utcnow()
    final_products = []
    removed_products = []
    saved_products = []

    # These args should always be checked
    check_args = [
        "sector_list",
        "tcdb",
        "tcdb_sector_list",  # TC Database sectors,
        "trackfiles",
        "trackfile_parser",
        "trackfile_sector_list",  # Flat text trackfile,
        "fuse_files",
        "fuse_reader_name",
        "fuse_product_name",
        "product_db",
    ]

    check_command_line_args(check_args, command_line_args)

    compare_path = command_line_args["compare_path"]

    if "product_db" in command_line_args and command_line_args["product_db"]:
        product_db = command_line_args["product_db"]
    else:
        product_db = False

    if product_db:
        if not getenv("GEOIPS_DB_USER") or not getenv("GEOIPS_DB_PASS"):
            raise ValueError("Need to set both $GEOIPS_DB_USER and $GEOIPS_DB_PASS")

    fuse_data = unpack_fusion_arguments(command_line_args)
    final_product_name = fuse_data["final"]["product_name"]
    final_source_name = fuse_data["final"]["source_name"]
    final_prod_plugin = products.get_plugin(final_source_name, final_product_name)

    # Set output_format and product_name in the command_line_args dict, used
    # throughout single_source code.
    command_line_args["output_formatter"] = fuse_data["final"]["output_format"]
    command_line_args["product_name"] = fuse_data["final"]["product_name"]

    # "final" dataset is pre-populated with an intermediate METADATA dataset,
    # with the best-available information.
    # The METADATA will be updated once all algorithms/products have been applied.
    area_defs = get_area_defs_from_command_line_args(
        command_line_args,
        {"METADATA": fuse_data["final"]["metadata_xobj"]},
        filter_time=True,
    )

    output_checker_kwargs = command_line_args.get("output_checker_kwargs", {})

    num_jobs = 0

    for area_def in area_defs:
        process_datetimes[area_def.name] = {}
        process_datetimes[area_def.name]["start"] = datetime.utcnow()
        # This returns xarray.Dataset, or dict of xarray.Datasets
        fused_xarray = get_fused_xarray(area_def, fuse_data, command_line_args)

        if fused_xarray is not None:
            # If it is a dict, set alg_xarray to xarray_dict['METADATA']
            if isinstance(fused_xarray, dict):
                fused_xarray_dict = fused_xarray
                # This should contain all appropriate metadata, for use in setting up
                # filenames, etc in plot_data.
                alg_xarray = fused_xarray["METADATA"]

            # If it is an xarray.Dataset, then just use the alg_xarray for
            # everything (plotting data, and metadata)
            elif isinstance(fused_xarray, xarray.Dataset):
                fused_xarray_dict = None
                alg_xarray = fused_xarray
                final_product_name = fused_xarray.product_name

            # xarray_obj not actually used in output_format_kwargs...
            # This determines what keyword arguments were specified within the
            # product YAML for the output
            output_format_kwargs = get_output_formatter_kwargs(
                command_line_args, xarray_obj=alg_xarray, area_def=area_def
            )

            # Note fused_xarray_dict is used for actual output format call,
            # alg_xarray used for filenames, etc.
            curr_products = plot_data(
                command_line_args,
                alg_xarray,
                area_def,
                final_prod_plugin,
                output_format_kwargs,
                fused_xarray_dict=fused_xarray_dict,
            )

            if isinstance(curr_products, dict):
                final_products += curr_products.keys()
            else:
                final_products += curr_products

            curr_removed_products, curr_saved_products = remove_duplicates(
                curr_products, remove_files=True
            )
            removed_products += curr_removed_products
            saved_products += curr_saved_products

            process_datetimes[area_def.name]["end"] = datetime.utcnow()
            num_jobs += 1
        else:
            LOG.info(
                "SKIPPING No coverage or required variables for %s %s",
                alg_xarray.source_names,
                area_def.name,
            )
            # raise ImportError('Failed to find required fields in product
            # algorithm: {0}.{1}'.format(
            # sect_xarrays[0].source_name,product_name))

    process_datetimes["overall_end"] = datetime.utcnow()
    from geoips.geoips_utils import output_process_times

    output_process_times(process_datetimes, num_jobs)

    mem_usage_stats = print_mem_usage("MEMUSG", verbose=True)
    if product_db:
        if command_line_args.get("sector_list") and (
            command_line_args.get("tcdb") or command_line_args.get("trackfiles")
        ):
            sector_type = "static_and_dynamic_tc"
        elif command_line_args.get("tcdb") or command_line_args.get("trackfiles"):
            sector_type = "dynamic_tc"
        else:
            sector_type = "static"
        write_stats_to_database(
            procflow_name="data_fusion",
            platform=fuse_data["final"]["platform_name"],
            source=fuse_data["final"]["source_name"],
            product=final_product_name,
            sector_type=sector_type,
            process_times=process_datetimes,
            num_products_created=len(final_products),
            num_products_deleted=len(removed_products),
            resource_usage_dict=mem_usage_stats,
        )

    retval = 0

    if compare_path:
        for output_product in final_products:
            plugin_name = output_checkers.identify_checker(output_product)
            output_checker = output_checkers.get_plugin(plugin_name)
            kwargs = {}
            if output_checker.name in output_checker_kwargs:
                kwargs = output_checker_kwargs[output_checker.name]
            retval += output_checker(
                output_checker,
                compare_path.replace("<product>", final_product_name).replace(
                    "<procflow>", "data_fusion"
                ),
                [output_product],
                **kwargs,
            )

    from os.path import basename

    LOG.info(
        "The following products were produced from procflow %s", basename(__file__)
    )
    for output_product in final_products:
        LOG.info("    DATAFUSIONSUCCESS %s", output_product)

    return retval
