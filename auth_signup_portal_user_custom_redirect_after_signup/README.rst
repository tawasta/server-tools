.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=====================================================
Auth Signup: Portal User Custom Redirect After Signup
=====================================================

* Add support for redirecting to a user-specific page after signup email
* Intended for situations where you link to the Signup page from e.g. product 
  pages, and you want to redirect the user back to the same product after
  they have finished signing up via the e-mail link.


Configuration
=============
* In addition to installing this module, you need to also modify those links that
  point to the signup page that you want to utilize this feature. That is done in
  separate custom module(s).
* For a usage example, see the website_sale_force_login module and how it's 
  linking to the signup page.

Usage
=====
 \-

Known issues / Roadmap
======================
* This module has been written to be used together with OCA's auth_signup_verify_email.
  With other modules or authentication setups, further modification may be needed.

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
