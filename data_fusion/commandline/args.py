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

""" Command line script for kicking off geoips based procflows"""

import argparse
import logging

from geoips.commandline.args import add_args as geoips_add_args
from geoips.commandline.args import check_command_line_args as geoips_check_args
from geoips.commandline.args import get_command_line_args as geoips_get_args

LOG = logging.getLogger(__name__)


def check_command_line_args(arglist, argdict):
    """Check formatting of command line arguments

    Args:
        arglist (list) : List of desired command line arguments to check within argdict for appropriate formatting
        argdict (dict) : Dictionary of command line arguments

    Returns:
        (bool) : Return True if all arguments are of appropriate formatting.

    Raises:
        (TypeError) : Incorrect command line formatting
    """
    geoips_check = geoips_check_args(arglist, argdict)

    num_fusion_datasets = len(argdict["fuse_files"])

    if not argdict["fuse_files"] or not argdict["fuse_reader_name"]:
        raise ValueError(
            "Need to pass --fuse_files and --fuse_reader_name at the command line"
        )

    if not argdict["fuse_product_name"]:
        raise ValueError("Need to pass --fuse_product_name at the command line")

    if not argdict["fuse_dataset_name"]:
        raise ValueError("Need to pass --fuse_dataset_name at the command line")

    # --fuse_reader_name and --fuse_product_name required for each fusion dataset -
    # raise ValueError if not included for each set of files.
    if len(argdict["fuse_reader_name"]) != num_fusion_datasets:
        raise ValueError(
            "Number of passed readers does not match the number of fusion file groups"
        )
    if len(argdict["fuse_product_name"]) != num_fusion_datasets:
        raise ValueError(
            "Number of passed products does not match the number of fusion file groups"
        )

    # All other --fuse_* arguments are optional - but if they are included for one fusion dataset,
    # they must be included for all.  If there is more than one included, ensure the number of arguments
    # passed matches the number of fusion datasets.
    if (
        argdict["fuse_output_format"]
        and len(argdict["fuse_output_format"]) != num_fusion_datasets
    ):
        raise ValueError(
            "If --fuse_output_format passed for any fusion dataset, must be passed for all"
        )
    if argdict["fuse_order"] and len(argdict["fuse_order"]) != num_fusion_datasets:
        raise ValueError(
            "If --fuse_order passed for any fusion dataset, must be passed for all"
        )
    if (
        argdict["fuse_dataset_name"]
        and len(argdict["fuse_dataset_name"]) != num_fusion_datasets
    ):
        raise ValueError(
            "If --fuse_dataset_name passed for any fusion dataset, must be passed for all"
        )
    if (
        argdict["fuse_self_register_source"]
        and len(argdict["fuse_self_register_source"]) != num_fusion_datasets
    ):
        raise ValueError(
            "If --fuse_self_register_source passed for any fusion dataset, must be passed for all"
        )
    if (
        argdict["fuse_self_register_platform"]
        and len(argdict["fuse_self_register_platform"]) != num_fusion_datasets
    ):
        raise ValueError(
            "If --fuse_self_register_platform passed for any fusion dataset, must be passed for all"
        )
    if (
        argdict["fuse_self_register_dataset"]
        and len(argdict["fuse_self_register_dataset"]) != num_fusion_datasets
    ):
        raise ValueError(
            "If --fuse_self_register_dataset passed for any fusion dataset, must be passed for all"
        )
    if (
        argdict["fuse_sectored_read"]
        and len(argdict["fuse_sectored_read"]) != num_fusion_datasets
    ):
        raise ValueError(
            "If --fuse_sectored_read passed for any fusion dataset, must be passed for all"
        )
    if (
        argdict["fuse_resampled_read"]
        and len(argdict["fuse_resampled_read"]) != num_fusion_datasets
    ):
        raise ValueError(
            "If --fuse_resampled_read passed for any fusion dataset, must be passed for all"
        )

    # These data_fusion-based arguments are REQUIRED for data_fusion procflow
    if not argdict["fusion_final_source_name"]:
        raise ValueError("Must specify --fusion_final_source_name at the command line")
    if not argdict["fusion_final_platform_name"]:
        raise ValueError(
            "Must specify --fusion_final_platform_name at the command line"
        )
    if not argdict["fusion_final_output_formatter"]:
        raise ValueError(
            "Must specify --fusion_final_output_formatter at the command line"
        )
    if not argdict["fusion_final_product_name"]:
        raise ValueError("Must specify --fusion_final_product_name at the command line")

    # These single-source-based arguments are NOT supported for data_fusion procflow
    if argdict["reader_name"]:
        raise ValueError(
            "--reader_name not supported, need to pass --fuse_files and --fuse_reader at the command line"
        )
    if argdict["product_name"]:
        raise ValueError(
            "--product_name not supported, need to pass --fusion_final_product_name at the command line"
        )
    if argdict["output_formatter"]:
        raise ValueError(
            "--output_formatter not supported, need to pass --fusion_final_output_formatter at the command line"
        )

    return geoips_check


def get_command_line_args(arglist=None, description=None):
    """Parse command line arguments specified by the requested list of arguments

    Args:
        arglist (:obj:`list`, optional) : DEFAULT None.
                                            list of requested arguments to add to the ArgumentParser
                                            if None, include all arguments
        description (:obj:`str`, optional) : DEFAULT None. String description of arguments
    Returns:
        (dict) : Dictionary of command line arguments
    """
    return geoips_get_args(
        arglist,
        description,
        add_args_func=add_args,
        check_args_func=check_command_line_args,
    )


def add_args(parser, arglist=None):
    """List of available standard arguments for calling data file processing command line.

    Args:
        parser (ArgumentParser) : argparse ArgumentParser to add appropriate arguments
        arglist (:obj:`list`, optional) : DEFAULT None
                    list of requested arguments to add to the ArgumentParser
                    if None, include all arguments

    Returns:
        No return values (parser modified in place)
    """

    geoips_add_args(parser, arglist)

    # Eventually we probably want all of these here - but we'll have to consolidate the satval procflow first.
    fusion_group = parser.add_argument_group(
        title="Options for specifying fusion products"
    )
    if arglist is None or "fuse_files" in arglist:
        # fusion_group.add_argument('--fuse_files', action='append', nargs='+', default=None,
        #                           help='''Provide additional files required for fusion product. Files passed under
        #                                this flag MUST be from the same source. fuse_files may be passed multiple times.
        #                                Reader name for these files is specified with the fuse_reader flag.''')
        fusion_group.add_argument(
            "--fuse_reader_name",
            action="append",
            default=None,
            help="""Provide the reader name for files passed under the fuse_files flag.
                                       Only provide one reader to this flag. If multiple fuse_files flags are passed,
                                       the same number of fuse_readers must be passed in the same order.""",
        )
        fusion_group.add_argument(
            "--fuse_product_name",
            action="append",
            default=None,
            help="""Provide the product name for files passed under the fuse_files flag.
                                       Only provide one product to this flag. If multiple fuse_files flags are passed,
                                       the same number of fuse_products must be passed in the same order.""",
        )
        # fusion_group.add_argument('--fuse_resampled_read', action='append', default=None,
        #                           help='''Identify whether the reader specified for --fuse_files / --fuse_reader
        #                                perform a resampled_read.  If not specified, a resampled read will NOT
        #                                be performed.  If multiple fuse_files flags are passed, either
        #                                the same number of fuse_resampled_read flags must be passed
        #                                in the same order, or no fuse_resampled_read flags can be passed.''')
        # fusion_group.add_argument('--fuse_sectored_read', action='append', default=None,
        #                           help='''Identify whether the reader specified for --fuse_files / --fuse_reader
        #                                perform a sectored_read.  If not specified, a sectored_read will NOT
        #                                be performed.  If multiple fuse_files flags are passed, either
        #                                the same number of fuse_sectored_read flags must be passed
        #                                in the same order, or no fuse_sectored_read flags can be passed.''')
        # fusion_group.add_argument('--fuse_self_register_dataset', action='append', default=None,
        #                           help='''Identify the DATASET of the data to which the associated fuse_files should
        #                                be registerd.
        #                                If not specified, data will not be registered to a dataset, but the requested
        #                                area_def. If multiple fuse_files flags are passed, either
        #                                the same number of fuse_self_register_dataset flags must be passed
        #                                in the same order, or no fuse_self_register_dataset flags can be passed.''')
        # fusion_group.add_argument('--fuse_self_register_source', action='append', default=None,
        #                           help='''Identify the SOURCE of the data to which the associated fuse_files
        #                                should be registerd.
        #                                If not specified, data will not be registered to a dataset, but the requested
        #                                area_def. If multiple fuse_files flags are passed, either
        #                                the same number of fuse_self_register_source flags must be passed
        #                                in the same order, or no fuse_self_register_source flags can be passed.''')
        # fusion_group.add_argument('--fuse_self_register_platform', action='append', default=None,
        #                           help='''Identify the SOURCE of the data to which the associated fuse_files
        #                                should be registerd.
        #                                If not specified, data will not be registered to a dataset, but the requested
        #                                area_def. If multiple fuse_files flags are passed, either
        #                                the same number of fuse_self_register_source flags must be passed
        #                                in the same order, or no fuse_self_register_source flags can be passed.''')
        fusion_group.add_argument(
            "--fusion_final_product_name",
            nargs="?",
            default=None,
            help="""Identify the name of the final product (which includes all fusion datasets)
                                       """,
        )
        fusion_group.add_argument(
            "--fusion_final_output_formatter",
            nargs="?",
            default=None,
            help="""Identify the output_format for the final product (using all fusion datasets)
                                       """,
        )
        fusion_group.add_argument(
            "--fusion_final_source_name",
            nargs="?",
            default=None,
            help="""Identify the source name that will be attributed to the final dataset.
                                       This will be an identifier that encompasses all datasets contained within
									   the final product, and will be referenced in "product_inputs" yamls
									   (ie, multi, visir-winds, visir, etc)
                                       """,
        )
        fusion_group.add_argument(
            "--fusion_final_platform_name",
            nargs="?",
            default=None,
            help="""Identify the platform name that will be attributed to the final dataset.
                                       This will be an identifier that encompasses all datasets contained within
									   the final product, and will be referenced in filenames, titles and metadata yamls
									   (ie, multi, geos, geo-polar, etc)
                                       """,
        )
        fusion_group.add_argument(
            "--fuse_output_format",
            action="append",
            default=None,
            help="""If applicable, identify the output format module to be used with
                                       the given product.""",
        )
        fusion_group.add_argument(
            "--fuse_order",
            action="append",
            default=None,
            help="""If applicable, identify the order each fused product should be
                                       implemented within the final product (integer values,
                                       lowest number will be the bottom, highest number top -
                                       must all be unique).""",
        )
        fusion_group.add_argument(
            "--fuse_dataset_name",
            action="append",
            default=None,
            help="""If applicable, identify a unique dataset id (can be numeric or string)
                                       """,
        )
