# Copyright 2016 ICTSTUDIO <http://www.ictstudio.eu>
# Copyright 2021 ACSONE SA/NV <https://acsone.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{
    "name": "OpenID Connect Telia",
    "version": "17.0.1.1.0",
    "license": "AGPL-3",
    "summary": "",
    "external_dependencies": {"python": ["jwcrypto"]},
    "depends": ["auth_oauth", "auth_signup", "partner_firstname"],
    "data": ["views/auth_oauth_provider.xml", "data/auth_oauth_data.xml"],
}
