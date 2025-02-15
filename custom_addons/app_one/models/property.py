from email.policy import default
from lib2to3.fixes.fix_input import context
from string import digits

from docutils.nodes import title
from odoo import fields, models, api
from odoo.exceptions import ValidationError, UserError
from datetime import timedelta
import requests
# from odoo17.odoo.addons.test_impex.tests.test_load import message
from odoo.addons.test_impex.tests.test_load import message

from odoo17.odoo.tools.populate import compute


class Property(models.Model):
    _name = "property"
    _description = "Property Record"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    ref = fields.Char(default='New', readonly=1)
    name = fields.Char(required=1, default='New', size=7)
    description = fields.Text(tracking=1)
    postcode = fields.Char(required=1)
    date_availability = fields.Date(tracking=1)
    expected_selling_date= fields.Date()
    is_late = fields.Boolean()
    create_time = fields.Datetime(default=fields.Datetime.now())
    next_time = fields.Datetime(compute='_add_six_hours')
    expected_price = fields.Float(digits=(0, 3))
    selling_price = fields.Float(digits=(0, 3))
    diff = fields.Float(compute='_compute_diff', store='1', readonly='0')
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean(groups='app_one.security_groups')
    garden = fields.Boolean()
    garden_area = fields.Integer()
    active = fields.Boolean(default=True)
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
        ('closed', 'Closed'),

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
            rec.create_history(rec.state, 'draft')
            rec.state = 'draft'
    def state_pending(self):
        for rec in self:
            print("This is from the pending.")
            rec.create_history(rec.state, 'pending')
            rec.state = 'pending'
    def state_sold(self):
        for rec in self:
            print("This is from the sold.")
            rec.create_history(rec.state, 'sold')
            # rec.state = 'sold'
            rec.write({
                'state':'sold'
            })
    def state_closed(self):
        for rec in self:
            print("This is from the closed.")
            rec.create_history(rec.state, 'closed')
            # rec.state = 'closed'
            rec.write({
                'state':'closed'
            })
    def check_expected_selling_date(self):
        # self is empty it does not have the set of records it refers to the model not for records
        print(self)
        #since the self is empty we read through the model using search,
        # and we assign the domain which  is a list to an empty list
        property_ids = self.search([])
        print(property_ids)
        for rec in property_ids:
            print(rec)
            if rec.expected_selling_date and rec.expected_selling_date < fields.date.today():
                rec.is_late = True
        print('from check_expected_selling_date')
    def change_state_wizard(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.change_state_action_wizard')
        action['context'] = {'default_property_id': self.id}
        return action
    def action_related_owner(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.owners_action')
        view_id = self.env.ref('app_one.owner_view_form').id
        action['res_id'] = self.owner_id.id
        action['views'] = [[view_id, 'form']]
        return action
    @api.depends('create_time')
    def _add_six_hours(self):
        for rec in self:
            if rec.create_time:
                rec.next_time = rec.create_time + timedelta(hours=6)
            else:
                rec.next_time = False

    @api.depends('expected_price', 'selling_price', 'owner_id.phone')
    def _compute_diff(self):
        for rec in self:
            print(rec)
            print("This is the computed field depends method.")
            rec.diff = rec.selling_price - rec.expected_price
    @api.onchange('expected_price')
    def _onchange_expected_price(self):
        for rec in self:
            print(rec)
            print("This is the computed field Onchange method.")
            return {
                'warning': {'title': 'warning','message': 'Negative Number', 'type': 'notification'}
            }
    def action(self):
        print(self.env)
        print(self.env.user)
        print(self.env.uid)
        print(self.env.company)
        print(self.env.cr)
        print(self.env['owner'].create({
            'name':'Ayman',
            'phone':'01020953526',
        }))
        print(self.env['owner'].search([ ]))
        print(self.env['property'].search([ ('name', '=', 'prop-1') ]))
        print(self.env['property'].search([ ('postcode', '=', '11511') ]))
        print(self.env['property'].search([ ('postcode', '!=', '11511') ]))
        print(self.env['property'].search([('postcode', '=', '11511'), ('name', '=', 'prop-1')]))
        print(self.env['property'].search(['|', ('postcode', '=', '11511'), ('name', '=', 'prop-1')]))


    @api.model
    def create(self, vals):
        res= super(Property, self).create(vals)
        if res.ref == "New":
            res.ref = self.env['ir.sequence'].next_by_code('property_seq')
        return res
    def create_history(self, old_state, new_state, reason=""):
        for rec in self:
            rec.env['property.history'].create({
                'user_id':rec.env.uid,
                'property_id':rec.id,
                'old_state':old_state,
                'new_state':new_state,
                'reason': reason or '',
                'line_ids': [(0,0,{'area': line.area, 'desciription': line.desciription}) for line in rec.line_ids]
            })
    def get_properties(self):
        payload = dict()
        try:
            response= requests.get('http://localhost:8069/v1/properties', data=payload)
            if response.status_code==200:
                print("successful")
            else:
                print("fail")
        except Exception as error:
            raise ValidationError(str(error))
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
