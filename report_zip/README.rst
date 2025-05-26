.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

============
Report - Zip
============

This module allows users to **download invoice reports as a ZIP file** in Odoo.

Features
========
- Generate invoice reports in PDF format.
- Bundle multiple invoices into a ZIP archive.

Configuration
=============
\-

Usage
=====
1. Select multiple invoices in the **Invoices** list view.
2. Click the **Download as ZIP** action.
3. The system generates a ZIP file containing the selected invoice reports.
4. The ZIP file is available for download.

Known issues / Roadmap
======================
* TODO Refactor module to be more generic like OCA module report_xlsx
* TODO Make cron action that removes the file after some time
* TODO Add support for sale orders

Credits
=======

Contributors
------------

* Joona Isoaho <joona.isoaho@futural.fi>
* Miika Nissi <miika.nissi@futural.fi>
* Valtteri Lattu <valtteri.lattu@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
