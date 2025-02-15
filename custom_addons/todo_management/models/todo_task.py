from email.policy import default

from odoo import models, fields, api

from odoo.exceptions import ValidationError
from odoo17.odoo.tools.populate import compute


class TodoTask(models.Model):
    _name = 'todo.task'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    task_name = fields.Char()
    assign_to_id = fields.Many2one('res.partner')
    description = fields.Char()
    due_date = fields.Date()
    estimated_time = fields.Float()
    status = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In progress'),
        ('completed', 'Completed'),
        ('closed', 'Closed')
    ], default='new')
    line_ids = fields.One2many('estimated.time', 'timesheet_id')
    total_time_spent = fields.Float(compute='_calc_total_time_spent', store=True)
    active = fields.Boolean(default=True)
    is_late = fields.Boolean()
    def set_new(self):
        for rec in self:
            rec.status = 'new'
    def set_in_progress(self):
        for rec in self:
            print("This task is in progress!!!")
            rec.status = 'in_progress'

    def set_completed(self):
        for rec in self:
            print("This task is completed!!!")
            rec.status = 'completed'
    def set_closed(self):
        for rec in self:
            rec.write({
                'status':'closed'
            })
    def check_expected_task_delivry_time(self):
        task_ids= self.search([])
        for rec in task_ids:
            if rec.due_date and rec.due_date < fields.date.today():
                rec.is_late = True

    @api.depends('line_ids.time_spent')
    def _calc_total_time_spent(self):
        for rec in self:
            total_time = sum(line.time_spent for line in rec.line_ids)
            rec.total_time_spent = total_time
    @api.constrains('estimated_time', 'line_ids.time_spent')
    def _estimated_time_should_not_exceed_total_time_spent(self):
        for rec in self:
            if rec.estimated_time < rec.total_time_spent:
                raise ValidationError('The total time spent should not exceed the estimated time for the task')


class EstimatedTime(models.Model):
    _name='estimated.time'
    timesheet_id = fields.Many2one('todo.task')
    time_spent = fields.Float()
    description = fields.Char()




