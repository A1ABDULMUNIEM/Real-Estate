from email.policy import default
from string import digits

from docutils.nodes import title
from odoo import fields, models, api
from odoo.exceptions import ValidationError, UserError


# from odoo17.odoo.addons.test_impex.tests.test_load import message
from odoo.addons.test_impex.tests.test_load import message

from odoo17.odoo.tools.populate import compute


class Property(models.Model):
    _name = "property"
    _description = "Property Record"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=1, default='New', size=7)
    description = fields.Text(tracking=1)
    postcode = fields.Char(required=1)
    date_availability = fields.Date(tracking=1)
    expected_price = fields.Float(digits=(0, 3))
    selling_price = fields.Float(digits=(0, 3))
    diff = fields.Float(compute='_compute_diff', store='1', readonly='0')
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('west', 'West'),
        ('east', 'East')
    ], default='north')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
    ], default='draft')
    owner_id = fields.Many2one('owner')
    tag_ids = fields.Many2many('tag')
    owner_address = fields.Char(related='owner_id.address', readonly=0, store=0)
    owner_phone = fields.Char(related='owner_id.phone', readonly=0, store=0)
    _sql_constraints = [
        ('unique_name', 'unique("name")', 'the name already exists!!')
    ]
    line_ids = fields.One2many("property.line", "bedroom_id")
    @api.constrains('bedrooms')
    def _check_bedrooms_value_npt_zero(self):
        for rec in self:
            if rec.bedrooms == 0:
                raise ValidationError('You must add the bedrooms number, as zero is not a valid entry.')
    def state_draft(self):
        for rec in self:
            print("This is from the draft.")
            rec.state = 'draft'
    def state_pending(self):
        for rec in self:
            print("This is from the pending.")
            rec.state = 'pending'
    def state_sold(self):
        for rec in self:
            print("This is from the sold.")
            # rec.state = 'sold'
            rec.write({
                'state':'sold'
            })
    @api.depends('expected_price', 'selling_price', 'owner_id.phone')
    def _compute_diff(self):
        for rec in self:
            print(rec)
            print("This is the computed field depends method.")
            rec.diff = rec.expected_price - rec.selling_price
    @api.onchange('expected_price')
    def _onchange_expected_price(self):
        for rec in self:
            print(rec)
            print("This is the computed field Onchange method.")
            return {
                'warning': {'title': 'warning','message': 'Negative Number', 'type': 'notification'}
            }

    #@api.model
    # @api.model_create_multi
    # def create(self, vals):
    #     res = super(Property, self).create(vals)
    #     # res = super().create(self, vals)
    #     print("This is an example of overriding/changing the behavior of the method create")
    #     return res
    #
    # @api.model
    # def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
    #     res = super(Property, self)._search(domain, offset=0, limit=None, order=None, access_rights_uid=None)
    #     print("This is an example of overriding/changing the behavior of the method search/read")
    #     return res
    # def write(self, vals):
    #     res = super(Property, self).write(vals)
    #     print("This is an example of overriding/changing the behavior of the method write/update")
    #     return res
    # def unlink(self):
    #     res= super(Property, self).unlink()
    #     print("This is an example of overriding/changing the behavior of the method delete/unlink")
    #     return res

class PropertyLine(models.Model):
    _name="property.line"

    bedroom_id = fields.Many2one('property')
    desciription = fields.Char()
    area = fields.Float()
