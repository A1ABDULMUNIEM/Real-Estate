from email.policy import default
from string import digits

from docutils.nodes import title
from odoo import fields, models, api
from odoo.exceptions import ValidationError, UserError


# from odoo17.odoo.addons.test_impex.tests.test_load import message
from odoo.addons.test_impex.tests.test_load import message

from odoo17.odoo.tools.populate import compute


class Building(models.Model):
    _name = "building"
    _description = "Building Record"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'code'
    no = fields.Integer()
    code = fields.Char()
    description = fields.Text()
    active = fields.Boolean(default=True)
