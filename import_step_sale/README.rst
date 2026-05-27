.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

===================
Import Step: Sales
===================

Adds a **Sales Orders + Lines** import step for the ``import_core`` framework.

This module registers a step with code ``sale`` and implements
the corresponding runner ``generic.import.runner.sale``.

The step:

* Creates or reuses sales orders
* Creates or reuses sales order lines
* Automatically links imported contacts and products from previous steps
* Stores created/found sale records into import state


Configuration
=============

1. Install:

   * ``import_core``
   * ``sale_management``
   * ``import_step_partner``
   * ``import_step_product``
   * this module

2. Go to:

   ``Imports → Templates``

3. Add the step:

   * **Sales Orders + Lines**

4. Create field mappings for models:

   * ``sale.order``
   * ``sale.order.line``

5. Mark one or more fields as **Is search field** if you want to
   search for existing sale orders or lines before creating new ones.


Usage
=====

Sales order import
------------------

* Map CSV columns to ``sale.order`` fields.
* The imported or previously found partner is automatically assigned
  to ``partner_id`` using import state.
* If search fields are defined and a matching sales order is found,
  that order is reused.
* If no match is found, a new sales order is created.

Sales order line import
-----------------------

* Map CSV columns to ``sale.order.line`` fields.
* The imported sales order is automatically assigned to ``order_id``.
* The imported or previously found product is automatically assigned
  to ``product_id`` using import state.
* If search fields are defined and a matching sales order line is found,
  that line is reused.
* If no match is found, a new sales order line is created.

Import state integration
------------------------

The step uses these state values from previous steps:

* ``state["partner"]``
* ``state["product"]``

The step stores:

* ``state["sale_order"]``
* ``state["sale_order_line"]``

This enables building customer-specific generic import pipelines such as:

* Contact + Product + Sales
* Contact + Product + Event + Registration
* Contact + Product + Custom business process


Known issues / Roadmap
======================

- No automatic update of existing sales orders or lines.
- No advanced normalization or validation beyond basic empty-value cleanup.
- Assumes products are imported through ``import_step_product``.


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