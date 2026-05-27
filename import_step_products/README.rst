.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

======================
Import Step: Products
======================

Adds a **Products** import step for the ``import_core`` framework.

This module registers a step with code ``product`` and implements
the corresponding runner ``generic.import.runner.product``.

The step:

* Creates new products
* Finds existing products using search fields
* Stores created/found products into import state for later steps


Configuration
=============

1. Install:

   * ``import_core``
   * ``product``
   * this module

2. Go to:

   ``Imports → Templates``

3. Add the step:

   * **Products**

4. Create field mappings for model:

   * ``product.template``

5. Mark one or more fields as **Is search field** if you want to
   search for existing products before creating new ones.


Usage
=====

Basic product import
--------------------

* Map CSV columns to ``product.template`` fields.
* If search fields are defined and a matching product is found,
  that product is reused.
* If no match is found, a new product is created.

Import state integration
------------------------

The step stores the following objects into import state:

* ``state["product_template"]``
* ``state["product"]``

This allows later import steps to automatically use the imported product,
for example when creating:

* Sale order lines
* Event registrations
* Customer-specific custom flows


Known issues / Roadmap
======================

- No automatic update of existing products.
- No advanced normalization or validation beyond basic empty-value cleanup.
- Assumes single-variant product usage via ``product_variant_id``.


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