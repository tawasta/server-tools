# -*- coding: utf-8 -*-

from odoo import api, fields, models
import ldap

class ResCompanyLdap(models.Model):

    _inherit = 'res.company.ldap'

    # Skip the cert validation. Please do not use this in production!
    def connect(self, conf):
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)

        return super(ResCompanyLdap, self).connect(conf)