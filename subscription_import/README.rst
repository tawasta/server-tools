.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
        :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
        :alt: License: AGPL-3

=================================
Upload and Generate Subscriptions
=================================
This module adds a configurable CSV import for creating subscriptions and
related data:

* contacts (``res.partner``)
* products (``product.product``)
* subscriptions (``sale.subscription``)
* subscription lines (``sale.subscription.line``)

Instead of hard-coding column names in Python, the import is driven by a
template that you configure in the UI. The template defines which CSV column
maps to which field on which model and which columns should be used to search
for existing records.

The import wizard also supports **child contacts** (sub-addresses) using a
special ``Tyyppi`` column in the CSV.

Configuration
=============
Templates
---------

1. Go to:

   ``Subscriptions → Subscription import templates``

2. Create a new template:

   * **Template Name** – any descriptive name

3. Add template lines under *Field mappings*:

   * **Template** – filled automatically
   * **Model** – one of:

     * ``res.partner`` – contact / customer
     * ``product.product`` – subscription product
     * ``sale.subscription`` – subscription header
     * ``sale.subscription.line`` – subscription line

   * **CSV Column Name** – the exact column header as it appears in the CSV
   * **Field Name** – the Odoo field to map to (filtered by selected model)
   * **Is Search Field** – if checked, the value from this column will be used
     to search for an existing record before creating a new one
   * **Sequence** – ordering in the mapping list (for readability only)

Usage
=====

1. Configure at least one template as described above.

2. Open the import wizard:

   ``Subscriptions → File Upload Wizard``

3. In the wizard:

   * Select a **Template**
   * Optionally click **CSV template** to open the template file in a new tab,
     save it locally, and fill it with your data.
   * Upload the completed CSV file in **File**.

4. Click **Upload**.

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
