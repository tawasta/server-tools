.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

=====================
Import Step: Contacts
=====================

Adds a **Partners** import step for the ``import_core`` framework.

This module registers a step with code ``partner`` and implements
the corresponding runner ``generic.import.runner.partner``.

The step:

* Creates new partners
* Finds existing partners using search fields
* Supports child contacts via the CSV column ``Tyyppi=child``


Configuration
=============

1. Install:

   * ``import_core``
   * ``contacts``
   * this module

2. Go to:

   ``Imports → Templates``

3. Add the step:

   * **Partners**

4. Create field mappings for model:

   * ``res.partner``

5. Mark one or more fields as **Is search field** if you want to
   search for existing partners before creating new ones.


Usage
=====

Basic partner import
--------------------

* Map CSV columns to ``res.partner`` fields.
* If search fields are defined and a matching partner is found,
  that partner is reused.
* If no match is found, a new partner is created.
* The field ``name`` is required when creating a new partner.

Child contacts
--------------

If the CSV column ``Tyyppi`` equals ``child`` (case-insensitive):

* The row is treated as a child contact.
* The child is linked to the latest previously processed
  main partner using ``parent_id``.
* If no main partner exists before a child row,
  a user-friendly error is raised.

Child rows do not execute remaining steps for that row.


Known issues / Roadmap
======================

- No automatic update of existing partners (search only reuses record).
- No advanced normalization or validation beyond basic checks.


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