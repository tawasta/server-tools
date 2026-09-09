.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===============
Customer Manual
===============

An in-app "Help Center": a manual for one installation, organized into
topics that are always derived live from the installed modules.

Features
========

* **Topics from installed modules**: the left sidebar shows one topic per
  module category (``ir.module.category``) actually used by an installed
  module. Topics whose category names are the same after trimming
  whitespace and ignoring case (e.g. two modules that both declare a
  "CRM" category, spelled slightly differently) are automatically merged
  into a single topic instead of showing as duplicates.
* **Instructions per topic** (``customer.manual.note``): rich text
  (CKEditor, including image upload) instructions, written by users in
  the "Edit Instructions" group. Each topic shows whether instructions
  exist yet.
* **Installation overview**: the sidebar shows how many topics, installed
  modules and written instructions the installation has, counting only
  the topics that are actually visible.
* **Editable "Open original manual" link** (``customer.manual.section``):
  an editor can set/change a link per topic, for example to a
  ``website_slides`` channel with detailed instructions for that
  feature.
* **Automatic filtering of technical modules**: a topic is hidden from
  the list when none of its modules are marked as an application and
  every one of them sits in the category tree Odoo itself excludes from
  its own Apps view ("Technical" and the two theme categories, see
  ``ir.module.module.search_panel_select_range()`` in Odoo core).
* **Maintainer details**: a collapsible section per topic listing the
  installed modules and their technical descriptions, for support use.

Configuration
=============
* Add users who should be able to write instructions or set manual links
  to the "Edit Instructions" group
  (``customer_manual.group_customer_manual_edit``). All internal users
  can read.

Usage
=====
* Open "Customer Manual" from the main menu.
* Pick a topic on the left, click "Edit" to write/update instructions.
* Click the pencil next to "Open original manual" (or "Set original
  manual link" if none is set yet) to point the topic at external
  documentation.

Known issues / Roadmap
======================
* Default instruction content is not seeded automatically when a new
  module is installed; instructions are always written by hand. A
  curated template library and an automated sync could add this later.
* CKEditor is loaded from an external CDN (``cdn.ckeditor.com``) in the
  backend assets. Vendoring it locally would remove that runtime
  dependency on a third-party CDN.
* Images uploaded into an instruction are stored as ``ir.attachment``
  records as soon as they are inserted, even if the instruction is
  discarded afterwards without saving. Nothing currently cleans up
  attachments left behind this way.

Credits
=======

Contributors
------------

* Valtteri Lattu <valtteri.lattu@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
