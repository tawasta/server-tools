.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

=====================
Import Step: Contacts
=====================

Adds a **Partners** import step for the ``import_core`` framework.

This module registers:

* Import step: ``partner``
* Runner model: ``generic.import.runner.partner``

The step integrates with the generic dispatcher provided by
``import_core``.

Features
========

The partner import step supports:

* Creating new partners
* Reusing existing partners via search fields
* Parent/child contact imports
* Shared import state integration
* Automatic child contact linking
* Sequential import chaining

The module depends on:

* ``import_core``
* ``contacts``

Import step registration
========================

The module registers the following import step:

.. code-block:: xml

    <record id="generic_import_step_partner" model="generic.import.step">
        <field name="name">Partners</field>
        <field name="code">partner</field>
        <field name="sequence">10</field>
        <field name="required_models">res.partner</field>
    </record>

This means:

* The dispatcher executes runner:

  ``generic.import.runner.partner``

* The step is only available when model ``res.partner`` exists.

Configuration
=============

1. Install modules:

   * ``import_core``
   * ``contacts``
   * ``import_step_contacts``

2. Open:

   ``Imports -> Templates``

3. Create or edit a template

4. Add import step:

   * ``Partners``

5. Configure field mappings for:

   * ``res.partner``

6. Optionally mark fields as:

   * ``Is search field``

Search fields are used to find existing partners before creating new ones.

Usage
=====

Basic partner import
--------------------

Map CSV/XLSX columns to ``res.partner`` fields.

Example mappings:

* ``Name -> res.partner.name``
* ``Email -> res.partner.email``
* ``Phone -> res.partner.phone``

Import behavior:

* Existing partners are reused when search fields match
* New partners are created when no match exists
* ``name`` is required for new partner creation

Example CSV
-----------

.. code-block:: text

    Name,Email,Phone
    Test Partner,test@example.com,123456

Search field behavior
---------------------

Fields marked as ``Is search field`` are used to build search domains.

Example:

* ``email`` marked as search field

The runner performs:

.. code-block:: python

    self.env["res.partner"].search([
        ("email", "=", value)
    ], limit=1)

If a record is found:

* Existing record is reused
* Duplicate creation is avoided

Child contacts
===============

Child contacts are supported using CSV/XLSX column:

* ``Tyyppi``

If value equals:

* ``child``

(case-insensitive)

then the row is treated as a child contact.

Example CSV
------------

.. code-block:: text

    Tyyppi,Name,Email
    main,Company A,company@example.com
    child,John Doe,john@example.com
    child,Jane Doe,jane@example.com

Behavior
---------

When importing child rows:

* The latest main partner is stored in shared state
* Child contacts automatically receive:

  ``parent_id = main_partner.id``

* Child rows skip remaining import steps using:

  ``state["_skip_rest"] = True``

This prevents child contact rows from executing unrelated import logic.

Shared import state
===================

The runner stores records into import state using:

.. code-block:: python

    state = self._set_state_record(
        state,
        "partner",
        partner,
    )

For main contacts:

.. code-block:: python

    state["main_partner"] = partner

This allows later rows and later steps to reuse the partner record.

Error handling
===============

The module provides user-friendly validation errors.

Missing main partner
--------------------

If a child row appears before a main partner:

.. code-block:: text

    Child-kontaktirivi ilman pääkontaktia.

Missing partner name
--------------------

If a new partner would be created without ``name``:

.. code-block:: text

    Partnerilta puuttuu nimi (name).

Errors include:

* CSV row number
* Original row data
* Processed values

Technical implementation
========================

The runner inherits:

.. code-block:: python

    _inherit = "generic.import.runner.base"

Available helper methods include:

* ``_get_or_create()``
* ``_clean_vals()``
* ``_set_state_record()``
* ``_build_domain()``

Partner creation flow
---------------------

Simplified flow:

1. Read mapped values
2. Build search domain
3. Search existing partner
4. Create if not found
5. Store result into shared state
6. Handle child logic

Dependencies
============

Python dependencies:

* None

Odoo dependencies:

* ``import_core``
* ``contacts``

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