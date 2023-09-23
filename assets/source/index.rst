.. Project documentation master file, created by
   sphinx-quickstart on Thu Sep 21 00:04:53 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Project's documentation!
================================

This is the official documentation of the Project Transformation pipeline extracted from the docstring of the code.

To visit the Project Website `Click Here`_

.. _Click Here: https://sites.google.com/airbus.com/Projectsite

.. note::
   Every Transformation includes 2 libraries:
      - The `dataset` module that call the main function of procesing
      - The `lib` module that contains the explanation of each function applied

MIP Changelogs
--------------
All the Mip changelogs are found in Confluence `MIP Changelogs`_

.. _MIP Changelogs: https://confluence.airbus.corp/display/D2J08XBOEX/Project2.0+Releases+notes

Common library for Project Transformation pipeline
-----------------------------------------------

:doc:`local_modules.Project_reloaded_common_lib`
   This common library is used in the Project Transformation pipeline. It contains all the functions used in the pipeline.
   These functions can be buisness functions or technical functions.

   🔗 `Xrlib Repository skywise link <https://core.skywise.com/workspace/data-integration/code/repos/ri.stemma.main.repository.fabc943c-781f-4529-a70a-78b5ea9ac6fc/contents/refs%2Fheads%2Fmaster>`_

   .. tip::
      If you want to use this common library in your own project, you can import it in your Code Workbook or Code authoring.
      You also need to have at least version `python 3.8` installed.

Main pipeline and logics
------------------------

:doc:`local_modules.as_designed_logic`
   This is the As designed logics transformations pipeline.

   🔗 `As designed Repository skywise link <https://core.skywise.com/workspace/data-integration/code/repos/ri.stemma.main.repository.d35a088c-cf1b-4829-8614-6a142fa8cb99/contents/refs%2Fheads%2Fmaster>`_

:doc:`local_modules.as_built_bom_logic`
   This is the As built logics transformations pipeline.

   🔗 `As built Repository skywise link <https://core.skywise.com/workspace/data-integration/code/repos/ri.stemma.main.repository.126296f3-4e13-4781-a06e-7bef7fb53212/contents/refs%252Fheads%252Fmaster>`_

:doc:`local_modules.as_planned_logic`
   This is the As Planned logics transformations pipeline.

   🔗 `As planned Repository skywise link <https://core.skywise.com/workspace/data-integration/code/repos/ri.stemma.main.repository.92e5703d-d98d-42eb-9aee-4727d94c89b9/contents/refs%252Fheads%252Fmaster>`_

:doc:`local_modules.digital_costing_logic`
   This is the Digital costing logics transformations pipeline.

   🔗 `Digital Costing Repository skywise link <https://core.skywise.com/workspace/data-integration/code/repos/ri.stemma.main.repository.91fa0bd9-3520-41b9-8507-04e74933e1e4/contents/refs%252Fheads%252Fmaster>`_

:doc:`local_modules.supbom_logic`
   This is the Supplier logics transformations pipeline.

   🔗 `Supbom Repository skywise link <https://core.skywise.com/workspace/data-integration/code/repos/ri.stemma.main.repository.9bd0c771-779f-46eb-a067-452fe975be7b/contents/refs%252Fheads%252Fmaster>`_

:doc:`local_modules.composed_objects_and_analysis_logic`
   This is the Composed objects and analysis logics transformations pipeline.

   🔗 `Composed Repository skywise link <https://core.skywise.com/workspace/data-integration/code/repos/ri.stemma.main.repository.3a9bbd93-9bf6-4c91-96aa-82369ace9293/contents/refs%2Fheads%2Fmaster>`_

   .. note::
      The composed objects is the composition of several objects to create a new object.

:doc:`local_modules.data_quality_indicator`

   This is the Data Quality indicators logics transformations pipeline.

   🔗 `Data quality Repository skywise link <https://core.skywise.com/workspace/data-integration/code/repos/ri.stemma.main.repository.0427f84e-6693-43de-a578-62074f213f51/contents/refs%252Fheads%252Fmaster>`_

.. Hidden TOCs

.. toctree::
   :caption: Home
   :maxdepth: 1
   :hidden:

   index
   MIP Changelogs <https://confluence.airbus.corp/display/D2J08XBOEX/Project2.0+Releases+notes>

.. toctree::
   :caption: Common library
   :maxdepth: 4
   :hidden:

   local_modules.Project_reloaded_common_lib

.. toctree::
   :caption: As designed
   :maxdepth: 4
   :hidden:

   local_modules.as_designed_logic.datasets
   local_modules.as_designed_logic.lib

.. toctree::
   :caption: As Built
   :maxdepth: 4
   :hidden:

   local_modules.as_built_bom_logic.datasets
   local_modules.as_built_bom_logic.lib

.. toctree::
   :caption: As Planned
   :maxdepth: 4
   :hidden:

   local_modules.as_planned_logic.datasets
   local_modules.as_planned_logic.lib

.. toctree::
   :caption: Supplier
   :maxdepth: 4
   :hidden:

   local_modules.supbom_logic.datasets
   local_modules.supbom_logic.lib

.. toctree::
   :caption: Composed objects
   :maxdepth: 4
   :hidden:

   local_modules.composed_objects_and_analysis_logic.datasets
   local_modules.composed_objects_and_analysis_logic.lib

.. toctree::
   :caption: Digital Costing
   :maxdepth: 4
   :hidden:

   local_modules.digital_costing_logic.datasets
   local_modules.digital_costing_logic.lib

.. toctree::
   :caption: Data Quality indicator
   :maxdepth: 4
   :hidden:

   local_modules.data_quality_indicator.datasets
   local_modules.data_quality_indicator.lib