# Copyright (C) 2020 Glodo UK <https://www.glodo.uk/>
# Copyright (C) 2010-2016, 2022 XCG Consulting <https://xcg-consulting.fr/>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64
import copy
import json
import logging
import os
import tempfile
import urllib.parse

# dependency name is pysaml2 # pylint: disable=W7936
import saml2
import saml2.xmldsig as ds
from lxml import etree
from saml2.client import Saml2Client
from saml2.config import Config as Saml2Config
from saml2.sigver import security_context

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


def create_metadata_string_fixed(
    configfile,
    config=None,
    valid=None,
    cert=None,
    keyfile=None,
    mid=None,
    name=None,
    sign=None,
):
    """
    TAWASTA: Pysaml2 has an issue, where metadata string doesn't show the
    correct algorithms from config.
    """
    valid_for = 0
    nspair = {"xs": "http://www.w3.org/2001/XMLSchema"}
    # paths = [".", "/opt/local/bin"]

    if valid:
        valid_for = int(valid)  # Hours

    eds = []
    if config is None:
        if configfile.endswith(".py"):
            configfile = configfile[:-3]
        config = Saml2Config().load_file(configfile)
    eds.append(saml2.metadata.entity_descriptor(config))

    conf = Saml2Config()
    conf.key_file = config.key_file or keyfile
    conf.cert_file = config.cert_file or cert
    conf.debug = 1
    conf.xmlsec_binary = config.xmlsec_binary
    secc = security_context(conf)

    if mid:
        eid, xmldoc = saml2.metadata.entities_descriptor(
            eds, valid_for, name, mid, sign, secc
        )
    else:
        eid = eds[0]
        if sign:
            eid, xmldoc = saml2.metadata.sign_entity_descriptor(
                eid, mid, secc, config.signing_algorithm, config.digest_algorithm
            )
        else:
            xmldoc = None

    saml2.metadata.valid_instance(eid)
    return saml2.metadata.metadata_tostring_fix(eid, nspair, xmldoc)


class AuthSamlProvider(models.Model):
    """Configuration values of a SAML2 provider"""

    _name = "auth.saml.provider"
    _description = "SAML2 Provider"
    _order = "sequence, name"

    name = fields.Char("Provider Name", required=True, index=True)
    entity_id = fields.Char(
        "Entity ID",
        help="EntityID passed to IDP, used to identify the Odoo",
        required=True,
        default="odoo",
    )
    idp_metadata = fields.Text(
        string="Identity Provider Metadata",
        help=(
            "Configuration for this Identity Provider. Supplied by the"
            " provider, in XML format."
        ),
        required=True,
    )
    sp_baseurl = fields.Text(
        string="Override Base URL",
        help="""Base URL sent to Odoo with this, rather than automatically
        detecting from request or system parameter web.base.url""",
    )
    sp_pem_public = fields.Binary(
        string="Odoo Public Certificate",
        attachment=True,
        required=True,
    )
    sp_pem_public_filename = fields.Char("Odoo Public Certificate File Name")
    sp_pem_private = fields.Binary(
        string="Odoo Private Key",
        attachment=True,
        required=True,
    )
    sp_pem_private_filename = fields.Char("Odoo Private Key File Name")
    sp_metadata_url = fields.Char(
        compute="_compute_sp_metadata_url",
        string="Metadata URL",
        readonly=True,
    )
    matching_attribute = fields.Char(
        string="Identity Provider matching attribute",
        default="subject.nameId",
        required=True,
        help=(
            "Attribute to look for in the returned IDP response to match"
            " against an Odoo user."
        ),
    )
    matching_attribute_to_lower = fields.Boolean(
        string="Lowercase IDP Matching Attribute",
        help="Force matching_attribute to lower case before passing back to Odoo.",
    )
    attribute_mapping_ids = fields.One2many(
        "auth.saml.attribute.mapping",
        "provider_id",
        string="Attribute Mapping",
    )
    active = fields.Boolean(default=True)
    sequence = fields.Integer(index=True)
    css_class = fields.Char(
        string="Button Icon CSS class",
        help="Add a CSS class that serves you to style the login button.",
    )
    body = fields.Char(string="Button Description")
    autoredirect = fields.Boolean(
        "Automatic Redirection",
        default=False,
        help="Only the provider with the higher priority will be automatically "
        "redirected",
    )
    sig_alg = fields.Selection(
        selection=lambda s: s._sig_alg_selection(),
        required=True,
        string="Signature Algorithm",
    )
    # help string is from pysaml2 documentation
    authn_requests_signed = fields.Boolean(
        default=True,
        help="Indicates if the Authentication Requests sent by this SP should be signed"
        " by default.",
    )
    logout_requests_signed = fields.Boolean(
        default=True,
        help="Indicates if this entity will sign the Logout Requests originated from it"
        ".",
    )
    want_assertions_signed = fields.Boolean(
        default=True,
        help="Indicates if this SP wants the IdP to send the assertions signed.",
    )
    want_response_signed = fields.Boolean(
        default=True,
        help="Indicates that Authentication Responses to this SP must be signed.",
    )
    want_assertions_or_response_signed = fields.Boolean(
        default=True,
        help="Indicates that either the Authentication Response or the assertions "
        "contained within the response to this SP must be signed.",
    )
    # this one is used in Saml2Client.prepare_for_authenticate
    sign_authenticate_requests = fields.Boolean(
        default=True,
        help="Whether the request should be signed or not",
    )
    sign_metadata = fields.Boolean(
        default=True,
        help="Whether metadata should be signed or not",
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
    def _sig_alg_selection(self):
        return [(sig[0], sig[0]) for sig in ds.SIG_ALLOWED_ALG]

    @api.onchange("name")
    def _onchange_name(self):
        if not self.body:
            self.body = self.name

    @api.depends("sp_baseurl")
    def _compute_sp_metadata_url(self):
        icp_base_url = (
            self.env["ir.config_parameter"].sudo().get_param("web.base.url", "")
        )

        for record in self:
            if isinstance(record.id, models.NewId):
                record.sp_metadata_url = False
                continue

            base_url = icp_base_url
            if record.sp_baseurl:
                base_url = record.sp_baseurl

            qs = urllib.parse.urlencode({"p": record.id, "d": self.env.cr.dbname})

            record.sp_metadata_url = urllib.parse.urljoin(
                base_url, ("/auth_saml/metadata?%s" % qs)
            )

    def _get_cert_key_path(self, field="sp_pem_public"):
        self.ensure_one()

        model_attachment = self.env["ir.attachment"].sudo()
        keys = model_attachment.search(
            [
                ("res_model", "=", self._name),
                ("res_field", "=", field),
                ("res_id", "=", self.id),
            ],
            limit=1,
        )

        if model_attachment._storage() != "file":
            # For non-file locations we need to create a temp file to pass to pysaml.
            fd, keys_path = tempfile.mkstemp()
            with open(keys_path, "wb") as f:
                f.write(base64.b64decode(keys.datas))
            os.close(fd)
        else:
            keys_path = model_attachment._full_path(keys.store_fname)

        return keys_path

    def _get_config_for_provider(self, base_url: str = None):
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
        # ADD: Contact persons to metadata, from Tawasta
        contact_persons = []
        for person in self.contact_person_ids:
            contact_persons.append(
                {
                    "given_name": person.firstname,
                    "sur_name": person.lastname,
                    "email_address": person.login,
                    "contact_type": "technical",
                    # Static company name
                    "company": "Oy Tawasta OS Technologies Ltd.",
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

        name_id_policy = "urn:oasis:names:tc:SAML:2.0:nameid-format:transient"

        settings = {
            # EDIT: Add service name
            "name": (self.env.ref("base.main_company").name, "fi"),
            "metadata": {"inline": [self.idp_metadata]},
            "entityid": self.entity_id,
            # EDIT: Add entity attributes
            "entity_attributes": entity_attribute_ids,
            "service": {
                "sp": {
                    "endpoints": {
                        "assertion_consumer_service": [
                            (acs_url, saml2.BINDING_HTTP_REDIRECT),
                            (acs_url, saml2.BINDING_HTTP_POST),
                            (acs_url, saml2.BINDING_HTTP_REDIRECT),
                            (acs_url, saml2.BINDING_HTTP_POST),
                        ],
                        # EDIT: SLO service
                        "single_logout_service": [
                            (slo_url, saml2.BINDING_HTTP_REDIRECT),
                            (slo_url, saml2.BINDING_HTTP_POST),
                        ],
                    },
                    "allow_unsolicited": False,
                    "authn_requests_signed": self.authn_requests_signed,
                    "logout_requests_signed": self.logout_requests_signed,
                    "want_assertions_signed": self.want_assertions_signed,
                    "want_response_signed": self.want_response_signed,
                    "want_assertions_or_response_signed": (
                        self.want_assertions_or_response_signed
                    ),
                    # EDIT: logout responses signed
                    "required_attributes": self.required_attributes.split(","),
                    "optional_attributes": self.optional_attributes.split(","),
                    "logout_responses_signed": self.authn_requests_signed,
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
            # EDIT: Encryption keypairs, organization details etc.
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
        sp_config = Saml2Config()
        sp_config.load(settings)
        sp_config.allow_unknown_attributes = True
        return sp_config

    def _get_client_for_provider(self, base_url: str = None):
        sp_config = self._get_config_for_provider(base_url)
        saml_client = Saml2Client(config=sp_config)
        return saml_client

    def _get_auth_request(self, extra_state=None, url_root=None):
        """
        build an authentication request and give it back to our client
        """
        self.ensure_one()

        if extra_state is None:
            extra_state = {}
        state = {
            "d": self.env.cr.dbname,
            "p": self.id,
        }
        state.update(extra_state)

        sig_alg = ds.SIG_RSA_SHA1
        if self.sig_alg:
            sig_alg = getattr(ds, self.sig_alg)

        saml_client = self._get_client_for_provider(url_root)
        reqid, info = saml_client.prepare_for_authenticate(
            sign=self.sign_authenticate_requests,
            relay_state=json.dumps(state),
            sigalg=sig_alg,
        )

        redirect_url = None
        # Select the IdP URL to send the AuthN request to
        for key, value in info["headers"]:
            if key == "Location":
                redirect_url = value

        self._store_outstanding_request(reqid)

        return redirect_url

    def _validate_auth_response(self, token: str, base_url: str = None):
        """return the validation data corresponding to the access token"""
        self.ensure_one()

        client = self._get_client_for_provider(base_url)
        response = client.parse_authn_request_response(
            token,
            saml2.entity.BINDING_HTTP_POST,
            self._get_outstanding_requests_dict(),
        )
        matching_value = None

        if self.matching_attribute == "subject.nameId":
            matching_value = response.name_id.text
        else:
            attrs = response.get_identity()

            for k, v in attrs.items():
                if k == self.matching_attribute:
                    matching_value = v
                    break

            if not matching_value:
                raise Exception(
                    "Matching attribute %s not found in user attrs: %s"
                    % (self.matching_attribute, attrs)
                )

        if matching_value and isinstance(matching_value, list):
            matching_value = next(iter(matching_value), None)

        if isinstance(matching_value, str) and self.matching_attribute_to_lower:
            matching_value = matching_value.lower()

        vals = {"user_id": matching_value}

        post_vals = self._hook_validate_auth_response(response, matching_value)
        if post_vals:
            vals.update(post_vals)

        return vals

    def _get_outstanding_requests_dict(self):
        self.ensure_one()

        requests = (
            self.env["auth_saml.request"]
            .sudo()
            .search([("saml_provider_id", "=", self.id)])
        )
        return {record.saml_request_id: record.id for record in requests}

    def _store_outstanding_request(self, reqid):
        self.ensure_one()

        self.env["auth_saml.request"].sudo().create(
            {"saml_provider_id": self.id, "saml_request_id": reqid}
        )

    def _metadata_string(self, valid=None, base_url=None):
        self.ensure_one()

        sp_config = self._get_config_for_provider(base_url)
        # return saml2.metadata.create_metadata_string(
        #     None,
        #     config=sp_config,
        #     valid=valid,
        #     cert=self._get_cert_key_path("sp_pem_public"),
        #     keyfile=self._get_cert_key_path("sp_pem_private"),
        #     sign=self.sign_metadata,
        # )
        metadata = create_metadata_string_fixed(
            None,
            config=sp_config,
            valid=valid,
            cert=self._get_cert_key_path("sp_pem_public"),
            keyfile=self._get_cert_key_path("sp_pem_private"),
            sign=self.sign_metadata,
        )
        # TODO: Metadata string can't present ä or ö, temporary fix
        metadata = metadata.replace("&#xE4;", "ä")
        # TODO: ServiceName allowed only in one language, duplicate for sv + en?
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

    def _hook_validate_auth_response(self, response, matching_value):
        self.ensure_one()
        vals = {}
        attrs = response.get_identity()

        for attribute in self.attribute_mapping_ids:
            if attribute.attribute_name not in attrs:
                _logger.debug(
                    "SAML attribute '%s' found in response %s",
                    attribute.attribute_name,
                    attrs,
                )
                continue

            attribute_value = attrs[attribute.attribute_name]
            if isinstance(attribute_value, list):
                attribute_value = attribute_value[0]

            vals[attribute.field_name] = attribute_value

        return {"mapped_attrs": vals}
