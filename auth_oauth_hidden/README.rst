.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

============
Oauth hidden
============

Adds a parameter for OAuth providers to allow hiding them

IMPORTANT: This is not supposed to LIMIT logins, but avoid confusion for
end users in an environment where admin logins use OAuth login.

Configuration
=============
Set OAuth provider as hidden and provide a hidden key

Usage
=====
If you want to use a hidden provider, add the hidden key to url.
E.g. `..web/login?key=mykey`

Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* Jarmo Kortetjärvi <jarmo.kortetjarvi@futural.fi>
* Aleksi Savijoki <aleksi.savijoki@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
