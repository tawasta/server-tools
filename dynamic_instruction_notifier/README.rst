.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

============================
Dynamic instruction notifier
============================

Overview

The Dynamic Instruction Notifier module enhances Odoo's user experience by displaying contextual instructions or notifications in the backend administration and the portal frontend, based on the user's current view or action.

Key Features

Contextual Instructions: Automatically displays relevant instructions to users based on their current activity or view in Odoo.
Admin and Portal Categories: Supports separate instruction sets for backend administration and portal users, ensuring targeted content delivery.
Rich Text Content: Allows for the creation of rich text instruction messages that can include HTML content.
SweetAlert2 Integration: Utilizes SweetAlert2 for visually appealing and user-friendly notifications.

Configuration
=============
Administrators can manage instruction messages via the "Instruction Message" menu, setting up content, associating it with models or views, and specifying the target audience.

Usage
=====
Backend Notifications: Triggered by actions related to specific models.
Portal Notifications: Based on the user's current portal view, identified through HTML data attributes.

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
