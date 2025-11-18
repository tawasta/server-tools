from odoo import api, fields, models
from lxml import etree

import copy
import logging
import urllib.parse

# dependency name is pysaml2 # pylint: disable=W7936
import saml2
from saml2.config import Config as Saml2Config
import saml2.xmldsig as ds

_logger = logging.getLogger(__name__)

class AuthSamlProvider(models.Model):
    _inherit = "auth.saml.provider"
    group_ids = fields.Many2many(
        comodel_name="res.groups",
        string="Default groups for users",
        help="What groups are assigned to newly created users",
    )
    use_hashed_id = fields.Boolean(
        string="SAML identifier hashed",
        help="Save SAML identifier only as hashed string (SHA256)",
    )
    contact_person_ids = fields.Many2many(
        comodel_name="res.users",
        string="Contact Persons",
    )
    entity_attribute_ids = fields.One2many(
        comodel_name="auth.saml.attribute.entity",
        inverse_name="provider_id",
        string="Entity attributes",
        help="Entity attributes used in metadata",
    )
    required_attributes = fields.Char(
        string="Required attributes",
        help="Attributes that are required from IdP (comma separated)",
    )
    optional_attributes = fields.Char(
        string="Optional attributes",
        help="Attributes that are optional from IdP (comma separated)",
    )

    @api.model
    def _metadata_string(self, valid=None, base_url=None):
        metadata = super()._metadata_string(valid, base_url)
        metadata = metadata.replace("&#xE4;", "ä")
        file = etree.fromstring(metadata)
        for elem in file.findall(".//{*}ServiceName"):
            duplicate_sv = copy.deepcopy(elem)
            duplicate_sv.attrib["{http://www.w3.org/XML/1998/namespace}lang"] = "sv"
            duplicate_en = copy.deepcopy(elem)
            duplicate_en.attrib["{http://www.w3.org/XML/1998/namespace}lang"] = "en"
            parent = elem.getparent()
            parent.insert(parent.index(elem) + 1, duplicate_sv)
            parent.insert(parent.index(elem) + 1, duplicate_en)
            break
        metadata = etree.tostring(
            file, pretty_print=True, encoding="utf-8", xml_declaration=True
        )
        return metadata

    @api.model
    def _get_config_for_provider(self, base_url=None):
        """
        Internal helper to get a configured Saml2Client
        """
        self.ensure_one()

        if self.sp_baseurl:
            base_url = self.sp_baseurl

        if not base_url:
            base_url = (
                self.env["ir.config_parameter"].sudo().get_param("web.base.url", "")
            )

        acs_url = urllib.parse.urljoin(base_url, "/auth_saml/signin")
        # EDIT: Add single logout service
        slo_url = urllib.parse.urljoin(base_url, "/auth_saml/slo")

        # ADD: Contact persons to metadata, from Futural
        contact_persons = []
        for person in self.contact_person_ids:
            contact_persons.append(
                {
                    "given_name": person.firstname,
                    "sur_name": person.lastname,
                    "email_address": person.login,
                    "contact_type": "technical",
                    # Static company name
                    "company": "Futural Oy",
                }
            )
        entity_attribute_ids = (
            self.entity_attribute_ids.get_entity_attributes_metadata()
        )

        # Get algorithms, pass to settings
        sig_alg = ds.SIG_RSA_SHA1
        if self.sig_alg:
            sig_alg = getattr(ds, self.sig_alg)
        digest_alg = ds.DIGEST_SHA1
        if self.sig_alg:
            # No selection for digest, use same variant as sign
            key = "DIGEST_{}".format(self.sig_alg.split("_")[-1])
            digest_alg = getattr(ds, key)

        if self.required_attributes:
            required_attrs = self.required_attributes.split(",")
        else:
            required_attrs = []

        if self.optional_attributes:
            optional_attrs = self.optional_attributes.split(",")
        else:
            optional_attrs = []

        name_id_policy = "urn:oasis:names:tc:SAML:2.0:nameid-format:transient"
        settings = {
            "name": (self.env.ref("base.main_company").name, "fi"),
            "metadata": {"inline": [self.idp_metadata]},
            "entityid": self.entity_id,
            "entity_attributes": entity_attribute_ids,
            "service": {
                "sp": {
                    "endpoints": {
                        "assertion_consumer_service": [
                            (acs_url, saml2.BINDING_HTTP_REDIRECT),
                            (acs_url, saml2.BINDING_HTTP_POST),
                            ],
                        "single_logout_service": [
                            (slo_url, saml2.BINDING_HTTP_REDIRECT),
                            (slo_url, saml2.BINDING_HTTP_POST),
                            ],
                        },
                    "required_attributes": required_attrs,
                    "optional_attributes": optional_attrs,
                    "allow_unsolicited": False,
                    "authn_requests_signed": self.authn_requests_signed,
                    "logout_requests_signed": self.logout_requests_signed,
                    "want_assertions_signed": self.want_assertions_signed,
                    "want_response_signed": self.want_response_signed,
                    "ui_info": {
                        "display_name": [
                            {
                                "lang": "fi",
                                "text": self.env.ref("base.main_company").name,
                                },
                            {
                                "lang": "sv",
                                "text": self.env.ref("base.main_company").name,
                                },
                            {
                                "lang": "en",
                                "text": self.env.ref("base.main_company").name,
                                },
                            ],
                        "description": [
                            {
                                "lang": "fi",
                                "text": self.env.ref("base.main_company").name,
                                },
                            {
                                "lang": "sv",
                                "text": self.env.ref("base.main_company").name,
                                },
                            {
                                "lang": "en",
                                "text": self.env.ref("base.main_company").name,
                                },
                            ],
                        },
                    "name_id_policy_format": name_id_policy,
                },
            },
            "cert_file": self._get_cert_key_path("sp_pem_public"),
            "key_file": self._get_cert_key_path("sp_pem_private"),
            "encryption_keypairs": [
                {
                    "key_file": self._get_cert_key_path("sp_pem_private"),
                    "cert_file": self._get_cert_key_path("sp_pem_public"),
                },
            ],
            "organization": {
                "name": (self.env.ref("base.main_company").name, "fi"),
                "display_name": (self.env.ref("base.main_company").name, "fi"),
                "url": (self.env.ref("base.main_company").website, "fi"),
            },
            "contact_person": contact_persons,
            "signing_algorithm": sig_alg,
            "digest_algorithm": digest_alg,
        }
        spConfig = Saml2Config()
        spConfig.load(settings)
        spConfig.allow_unknown_attributes = True
        return spConfig
