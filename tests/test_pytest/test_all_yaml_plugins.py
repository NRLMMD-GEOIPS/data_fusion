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

"""Test all YAML plugins."""
import pytest
import yaml
from importlib import resources

from geoips.schema import PluginValidator


validator = PluginValidator()


def yield_plugins():
    """Yield plugins."""
    fpath = resources.files("data_fusion") / "plugins/yaml"
    plugin_files = fpath.rglob("*.yaml")
    for pf in plugin_files:
        yield yaml.safe_load(open(pf, "r"))


@pytest.mark.parametrize("plugin", yield_plugins())
def test_is_plugin_valid(plugin):
    """Test if plugin is valid."""
    validator.validate(plugin)
