.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===================
API Request Handler
===================

Base module for handling API/HTTP requests.
Uses httpx library for making the requests

Configuration
=============
\-

Usage
=====
This module provides a mixin class `ApiRequestMixin` that can be inherited by any Odoo model to enable API request handling capabilities. The mixin includes a method `_api_request_make` that allows you to make HTTP requests to external APIs.

The _api_request_make is called in the same way as httpx.request method,
but it will also log the request and response details in the `api.request` model.

Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* Jarmo Kortetjärvi <jarmo.kortetjarvi@futural.fi>

Maintainer
----------

.. image:: https://futural.fi/templates/tawastrap/images/logo.png
   :alt: Futural Oy
   :target: https://futural.fi/

This module is maintained by Futural Oy
