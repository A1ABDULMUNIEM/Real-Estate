from odoo import fields, models, api

from odoo17.odoo.fields import One2many


class PropertyHistory(models.Model):
    _name='property.history'
    _description='Property history'
    user_id = fields.Many2one('res.users')
    property_id = fields.Many2one('property')
    old_state = fields.Char()
    new_state= fields.Char()
    reason = fields.Char()
    line_ids = fields.One2many('history.line', 'history_id')


class HistoryLine(models.Model):
    _name="history.line"

    history_id = fields.Many2one('property.history')
    desciription = fields.Char()
    area = fields.Float()