.. dropdown:: Distribution Statement

 | # # # This source code is subject to the license referenced at
 | # # # https://github.com/NRLMMD-GEOIPS.

.. _procflow_guide:

**************************
Data Fusion procflow guide
**************************


Product Types
=============

Layered
-------
Layered products display mutliple different products, or instruments over the same region for 
vizualiation or validation/verification. Data fusion itself can be used in both static, tc, or 
dyanmic sectors. Several arguments within the data fusion command line processing pipeline help 
denote the products, order, and format of each product used to merge to a final product.


Individual layers are called within sub-sections of the fusion command line arguments, denoted as fuse products, and 
combined in the final 'fusion' product, each require specific arguments.


Individual fuse arguments: Each set of arguments fully defines a product for a single layer of the final
image.  Ensure the fuse arguments are grouped together appropriately for each layer:

* ``@datatype_N@`` should reference the Nth datatype you are interested in processing
  (and will reference test data repositories set up through
  https://github.com/NRLMMD-GEOIPS/template_test_data)
* ``--fuse_files`` is the appropriate path to the data files of @datatype_N@ within the test data repo.
* ``--fuse_reader_name`` is the appropriate reader associated with your @datatype_N@
* ``--fuse_product_name`` is the product you would like to create from your data files
* ``--fuse_output_format`` is the output format you would like to use for plotting the current layer.
          * Note this is most likely going to be a "clean" output format (no gridlines, coastlines, titles, etc), since we want to simply layer the different images, and the annotations will be applied via the "fusion_final_output_format".
          * Valid image formats for layering must include fig, main_ax, mapobj inputs (If passed, use the existing fig, main_ax, and mapobj rather than recreating)
          * Valid image formats for layering must support not producing output if output_fnames is None (so we can avoid producing images for each layer individually)
          * See geoips imagery_clean.py and imagery_windbarbs_clean.py for examples of valid output formats.
* ``--fuse_dataset_name``: arbitrary string that defines the name of the current dataset.
          * Any instance of @fuse_dataset_name_N@ in the template script must match those in the template product/layered.yaml file
* ``--fuse_order``: Integer specifying the order of the layers.
          * Lower numbers are on the bottom, higher numbers on the top


Final fusion arguments: These are the arguments to specify the final output product, after layering
each individual "fuse" product specification below. The "fusion_final" arguments indicate how to
bring all the individual products together into a single "final" product.

* ``--fusion_final_product_name``: This is the name of your final product.  This MUST match the product specified within products/layered.yaml
* ``--fusion_final_source_name`` layered: The source name "layered" must match both:
                      * the name of the file product_inputs/layered.yaml and
                      * the key at the top level of product_inputs/layered.yaml
                      * This is an arbitrarily defined "source" name, but it must be consistent.
* ``--fusion_final_platform_name`` multi: This is an entirely arbitrarily defined platform name.
                      * It is only used for filename and title generation
                      * (sets "platform_name" on the final xarray object)
* ``--fusion_final_output_format`` layered_imagery: Do not change this argument
          * The "layered_imagery" output_format in the data_fusion repository is the magic that plots the separate products together.

An example of a layered products yaml file is posted below:

.. code-block:: python

  # The "layered" product_inputs file provides the specifications for the final @My-Layered-Product@ output.
  # The individual layers are specified within the command line call - this file indicates how the final image
  # should be generated.

  # @My-Layered-Product@ MUST match the fusion_final_product_name specified in the command line call.

  #    coverage_checker
  #    specifies which dataset (as specified in --fuse_dataset_name via command line)
  #    and variable should be used for calculating the final coverage of the product
  #    (for determining % coverage in filenames, and to determine
  #    if the product should be produced at all).
  #    Please choose @fuse_dataset_name_N@ from the command line call
  #    appropriately (this just depends on how you want coverage defined for
  #    your final product)
  #       coverage_checker:
  #          plugin:

  #    name indicates the appropriate coverage function to use for the given dataset
  #    (ie, defining coverage for windbarb data is different than for raster data).
  #    coverage checkers are found in plugins/modules/coverage_checkers
  #            name: masked_arrays
  #            arguments:
  #              variable_name: @fuse_dataset_name_N@:@variable_name_from_dataset@

  # Currently there is no method for including multiple datasets in the final coverage calculation. Please let the
  #    GeoIPS Team know if that is required functionality.

  # product_template: "Layered"
  #   indicates the base product to use in creating "@My-Layered-Product@"
  #   All fields under @My-Layered-Product@ override those in data_fusion/yaml_configs/product_params/Layered.yaml
  #
  # mpl_colors_info:
  #   Each key within mpl_colors_info refers to a @fuse_dataset_name_N@ as defined in the test script / command line call
  #   This option allows overriding fields within the current layer's colormap specification with a specific value.
  #   Please see various YAML files in data_fusion/yaml_configs/product_params/Layered-*.yaml for a variety of
  #   options for setting mpl_colors_info values specifically for adjusting colorbar locations/positioning

  interface: products
  family: list

  # @ This can be any unique identifier for this product list.
  name: my_layered_list

  # @ Include your own descriptive docstring that describes this list of products.
  docstring: |
    The default products_source_name fusion plugin configuration.

  spec:
    products:
      # @ product name is the identifier for the current product - note it *can*
      # @ match the name specified in "product_defaults".
      # @ product can be defined in ANY repo!  Does not have to be this repo!
      # @ NOTE: Please use '-' as a delimeter in product names by GeoIPS convention.
      # @ This allows using either '_' or '.' as a delimiter in filenames,
      # @ another GeoIPS convention.
      # @ Capitalization of each word in Product-Name can aid in human readability,
      # @ but is not strictly required. GeoIPS *is* case sensitive.
      - name: My-Layered-Winds

        # @ source_name must be a valid geoips "source_name", as found in the
        # @ reader for this data type.  Readers can be specified in any repository,
        # @ does not have to be specified in this repo!
        source_names: [my_layered_source]

        # @ Include your own descriptive docstring that describes this
        # @ particular product.
        docstring: |
          Layered winds product using default 2 colorbar placement.

          This example layered image includes default colorbar placement
          for both windspeed and ir products, and no colorbar for windbarbs.

        # @ product_defaults references a "product_defaults" plugin (found in any repo)
        product_defaults: Layered-Winds-Horizontal-Adjust

        spec:
          coverage_checker:
            plugin:
              name: masked_arrays
              arguments:
                variable_name: windspeed:wind_speed_kts

          mpl_colors_info: # These use "dataset_id" as specified in command line call as keys,
            # and override defaults found in the product's colormap specification
            windbarbs:
              colorbar: False
            windspeed:
              colorbar: True
            ir:
              colorbar: True



Stiched 
-------

