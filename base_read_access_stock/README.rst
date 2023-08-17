.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===============================
Read Access Group for Inventory
===============================

* Adds a new group that is allowed to read stock-related model data in
  Inventory main menu
* Intended for situations where employees should have additional read-only 
  acccess rights to inventory

Configuration
=============
* Add the user of your choice to the new "Read access to inventory" group

Usage
=====
\-

Known issues / Roadmap
======================
* Note that as a byproduct this module grants read access to other models 
  that are utilized on e.g. stock picking related forms. This means the user
  could read e.g. invoices indirectly (via XMLRPC or by following hyperlink 
  paths inside Odoo), even though the accounting menu remains invisible

Credits
=======

Contributors
------------

* Timo Talvitie <timo.talvitie@tawasta.fi>

Maintainer
----------

.. image:: https://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: https://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
