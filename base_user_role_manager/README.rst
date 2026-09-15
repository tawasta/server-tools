.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==========================================
An user group for managing users and roles
==========================================

Allow user to manage users and their roles

Configuration
=============
* Installing the module creates a new group, *Users and Roles*
  (``base_user_role_manager.group_role_manager``)
* This group is implied by *Administration / Access Rights*
  (``base.group_erp_manager``), so full administrators have it automatically
* Assign *Users and Roles* to users who should be able to manage users and
  their roles without granting them full Settings/administrator access

Usage
=====
* Members of *Users and Roles* get a dedicated **Users** top-level menu with:

  * **Users** - a restricted view of ``res.users`` that excludes admin,
    sysadmin, template and ``@futural.fi`` accounts, so they cannot be edited
    or removed by mistake
  * **Roles** - the roles defined by ``base_user_role``, read-only

* On the user form, members of this group can also see and edit the user's
  roles (``user_role_ids``, ``role_line_ids``) and record rules / access
  rights, which are otherwise only visible to full administrators

Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* Jarmo Kortetjärvi <jarmo.kortetjarvi@futural.fi>
* Valtteri Lattu <valtteri.lattu@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
