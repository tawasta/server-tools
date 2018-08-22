.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===============================
Read Access Group for Purchases
===============================

* Adds a new group that is allowed to read purchase-related model data in
  Purchases main menu
* Intended for situations where Employees should have additional read-only 
  acccess rights to purchases

Configuration
=============
* Add the user of your choice to the new "Read access to purchases" group

Usage
=====
\-

Known issues / Roadmap
======================
* Note that as a byproduct this module grants read access to other models 
  that are utilized on e.g. purchase-related forms. This means the user
  could read e.g. invoices indirectly (via XMLRPC or by following hyperlink 
  paths inside Odoo), even though the accounting menu remains invisible

Credits
=======

Contributors
------------

* Timo Talvitie <timo.talvitie@tawasta.fi>

Maintainer
----------

.. image:: http://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: http://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
