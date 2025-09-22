from odoo import fields, models

class AuthSamlAttributeEntity(models.Model):

    _name = "auth.saml.attribute.entity"
    _description = "Entity attributes for SAML provider"

    provider_id = fields.Many2one(
        comodel_name="auth.saml.provider",
        index=True,
        required=True,
    )
    name_format = fields.Char(
        string="Name format",
        help="What's the attributes name format",
        default="urn:oasis:names:tc:SAML:2.0:attrname-format:uri",
        required=True,
    )
    name = fields.Char(
        string="Name",
        help="What's the attributes name",
        required=True,
    )
    friendly_name = fields.Char(
        string="Friendly name",
        help="What's the attributes friendly name",
    )
    value = fields.Char(
        string="Attribute value(s)",
        help="What's the attributes values (separate multiple with comma)",
        required=True,
    )

    def get_entity_attributes_metadata(self):
        """Return list for metadata from defined attributes"""
        result = []
        for rec in self:
            vals = {
                "name_format": rec.name_format,
                "name": rec.name,
                "values": [val.strip() for val in rec.value.split(",")],
            }
            if rec.friendly_name:
                vals["friendly_name"] = rec.friendly_name
            result.append(vals)
        return result
