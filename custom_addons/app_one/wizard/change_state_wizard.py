from odoo import models, fields, api

class ChangeState(models.TransientModel):
    _name = "change.state"
    property_id = fields.Many2one('property')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending')
    ])
    reason = fields.Char()
    def confirm_change_state(self):
        print("Hello from the wizard")
        if self.property_id.state == 'closed':
            self.property_id.state = self.state
            self.property_id.create_history('closed', self.state, self.reason)