.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
        :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
        :alt: License: AGPL-3

===========
Import Core
===========
Generic CSV import core for Odoo 17.

This module provides:

* Import templates (field mappings + ordered import steps)
* A file upload wizard to execute the import
* A step runner dispatcher framework for pluggable “step modules” (partners, products, subscriptions, etc.)

Configuration
=============

Install ``import_core`` and (optionally) one or more step modules, for example:

* ``import_step_contacts`` (partners / contacts)

After installing the needed modules:

1. Go to: ``Imports -> Templates``
2. Create an import template
3. Select **Import steps** (these are provided by installed step modules)
4. Define **Field mappings**:

   * **CSV column name**: the header name in your CSV file
   * **Model**: restricted to the models allowed by the selected steps
   * **Field**: restricted by the selected model
   * **Is search field**: marks fields used to find existing records before creating new ones


Usage
=====
Create / edit templates
-----------------------

1. Open: ``Imports -> Templates``
2. Create a template
3. Select the import steps in the order you want them executed
4. Add field mapping lines

Run an import
-------------

1. Open: ``Imports -> Templates -> Import (Upload)``
2. Select the template
3. Download the CSV template if needed
4. Upload your CSV file
5. Click **Upload**

How step chaining works
-----------------------

The wizard reads each CSV row and:

1. Splits the row into model-specific mapping values using your template lines
2. Executes the selected steps in sequence
3. Passes a shared ``state`` dictionary between steps so they can chain records, for example:

   * Step 1 (partners) sets ``state["partner"]``

The dispatcher calls step runners by model name:

* Step code ``partner`` -> model ``generic.import.runner.partner``

If a runner model is not installed, that step is ignored automatically.

Known issues / Roadmap
======================
\-

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
