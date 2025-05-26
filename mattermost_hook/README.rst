.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

================
Mattermost Hooks
================

Adds possibility to add Mattermost hooks to be used from Odoo.
Currently supports only Mattermost incoming hooks.

Hooks are created in separate modules which use this module as a dependency.
Each module then adds the logic for gathering the message and use hooks method
post_mattermost to post the message into mattermost.

Hooks are shown under companies' form view.


Installation
============

Install the module form Settings->Local Modules

Configuration
=============
\-

Usage
=====
\-

Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* Jarmo Kortetjärvi <jarmo.kortetjarvi@futural.fi>
* Aleksi Savijoki <aleksi.savijoki@futural.fi>
* Miika Nissi <miika.nissi@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
