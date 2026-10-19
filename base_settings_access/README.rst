.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===============
Settings Access
===============

A limited settings menu for users without administrator rights. The menu
items under it are defined in the user interface, no code is needed.

Configuration
=============
* Set the user's *Settings Access* to *Access* under the *Administration*
  category on the user form.
* In developer mode, open *Settings / Technical / User Interface / Menu Items*
  and create a menu item for each settings menu the users should reach:

  * *Parent Menu*: *Limited Settings*
  * *Action*: the wanted action, for example the one of the core menu
    *Email Templates*
  * *Groups*: *Settings Access / Access*

* Do not move or edit the core menu items. Their parent and groups are reset on
  module update, and their parent *Settings* menu is only visible to
  administrators.
* The group does not grant access rights to the models behind the actions.
  Give them separately if the default employee rights are not enough, for
  example by adding the user to the core group of the feature.
* Menu items created this way are stored only in that database, so repeat
  them in each environment.

Usage
=====
* Members of the group see the **Limited Settings** top-level menu with the
  menu items created under it.
* The menu is hidden from users who have none of its children.

Known issues / Roadmap
======================
\-

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
