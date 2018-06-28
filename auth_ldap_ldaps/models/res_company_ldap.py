# -*- coding: utf-8 -*-

from odoo import models
import ldap


class ResCompanyLdap(models.Model):

    _inherit = 'res.company.ldap'

    # Override the connect to use ldaps
    def connect(self, conf):
        """
        Connect to an LDAP server specified by an ldap
        configuration dictionary.

        :param dict conf: LDAP configuration
        :return: an LDAP object
        """

        uri = 'ldaps://%s:%d' % (conf['ldap_server'], conf['ldap_server_port'])

        connection = ldap.initialize(uri)
        if conf['ldap_tls']:
            connection.start_tls_s()
        return connection

