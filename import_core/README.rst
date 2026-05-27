.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

===========
Import Core
===========

Generic CSV/XLSX import core for Odoo 17.

This module provides a flexible import framework with:

* Configurable import templates
* Ordered import step pipelines
* CSV and XLSX support
* Dynamic field mappings
* Shared import state between steps
* Create/write state link handling
* Pluggable runner modules

The module itself does not implement business imports directly.
Business logic is provided by separate step modules.

Features
========

Import templates
----------------

Templates define:

* Import step execution order
* CSV/XLSX column mappings
* Search fields for matching existing records
* State link relations between imported records

Import steps
------------

Each import step is registered as:

* ``generic.import.step``

and dispatched dynamically to:

* ``generic.import.runner.<code>``

Example:

* Step code: ``partner``
* Runner model: ``generic.import.runner.partner``

If the runner model is not installed, the step is skipped automatically.

Steps may also declare required models:

.. code-block:: python

    required_models = "res.partner,sale.order"

Unavailable model dependencies automatically disable the step.

Supported file formats
----------------------

CSV
^^^

* UTF-8 with BOM supported
* Latin-1 fallback supported

XLSX
^^^^

Implemented using:

* ``openpyxl``

The first worksheet is imported automatically.

Configuration
=============

Install ``import_core`` and one or more step modules.

Example:

* ``import_step_contacts``

After installation:

1. Go to: ``Imports -> Templates``
2. Create a new template
3. Add import steps
4. Configure field mappings
5. Configure optional state links

Import steps
------------

Templates use template-specific step ordering.

This means:

* Global step sequence does not affect template execution order
* Each template controls its own pipeline independently

Field mappings
--------------

Each mapping line defines:

* CSV/XLSX column name
* Target model
* Target field
* Whether the field is used for record matching

Search fields are used to build lookup domains before creating records.

Example:

* ``email`` may be marked as a search field for ``res.partner``

Allowed models are automatically restricted based on selected import steps.

State links
-----------

State links allow imported records to reference previously created records.

Two modes are supported:

Create
^^^^^^

Applied before record creation.

Used for required many2one fields that must exist during ``create()``.

Write
^^^^^

Applied after step execution using ``write()``.

Useful when records must exist before linking.

Example flow:

1. Partner step creates ``res.partner``
2. Sale order step creates ``sale.order``
3. State link writes:

   * ``sale.order.partner_id -> state["partner"]``

Usage
=====

Create / edit templates
-----------------------

1. Open: ``Imports -> Templates``
2. Create a template
3. Add import steps
4. Configure field mappings
5. Configure optional state links

Run an import
--------------

1. Open: ``Imports -> Templates -> Import (Upload)``
2. Select the template
3. Download the CSV template if needed
4. Upload CSV or XLSX file
5. Click ``Upload``

Import processing
=================

The import wizard:

1. Reads the uploaded file
2. Converts rows into model-specific values
3. Executes import steps sequentially
4. Passes shared state between steps
5. Applies state links

Shared state
------------

Steps may store created/found records into shared state.

Example:

.. code-block:: python

    state["partner"] = partner

Later steps may reuse these records.

Automatic model state keys are also generated:

.. code-block:: python

    state["res_partner"] = partner

Runner helpers
---------------

``generic.import.runner.base`` provides reusable helpers:

* ``_get_or_create()``
* ``_get_or_create_from_lines()``
* ``_build_domain()``
* ``_clean_vals()``
* ``_set_state_record()``

These helpers simplify custom runner implementations.

Example runner
--------------

.. code-block:: python

    from odoo import models


    class ImportPartner(models.AbstractModel):
        _name = "generic.import.runner.partner"
        _inherit = "generic.import.runner.base"

        def run(self, row_index, row, lines_by_model, state):
            partner = self._get_or_create_from_lines(
                "res.partner",
                lines_by_model,
                row_index,
                row,
                state=state,
            )

            return self._set_state_record(
                state,
                "partner",
                partner,
            )

Security
========

Access rights are included for:

* Import templates
* Template lines
* Template state links
* Template steps
* File upload wizard

Import step definitions are read-only for normal users.

Technical notes
===============

Step execution is skipped automatically when:

* Required Odoo models are unavailable
* Runner implementations are missing

This allows optional business modules to extend the framework safely.

Dependencies
============

Python dependencies:

* ``openpyxl``

Known issues / Roadmap
======================

Credits
=======

Contributors
------------

* Valtteri Lattu <valtteri.lattu@tawasta.fi>

Maintainer
----------

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
    :alt: Oy Tawasta OS Technologies Ltd.
    :target: http://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.