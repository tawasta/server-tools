.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===============================================
Remove "Sent using Odoo" from mail notification
===============================================

 * Removes the default 'Sent by Company X using Odoo' footer from the generic 'Notification Email' template.

Installation
============
* Just install the module

Configuration
=============
* No configuration needed

Usage
=====
\- 

Known issues / Roadmap
======================
* Note that some follower notifications may use a different template than this generic one, so you may need to override them separately.
* The noupdate=0 attribute in the core's mail template means that you cannot override this template in the UI without a module upgrade resetting it

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
