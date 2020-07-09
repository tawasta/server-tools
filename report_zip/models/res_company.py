import os
from random import randrange

from odoo import fields, models


class ResCompany(models.Model):

    _inherit = "res.company"
