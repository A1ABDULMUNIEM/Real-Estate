from odoo import models, fields

class TodoTask(models.Model):
    _name = 'todo.task'
    task_name = fields.Char()
    assign_to_id = fields.Many2one('res.partner')
    description = fields.Char()
    due_date = fields.Date()
    status = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In progress'),
        ('completed', 'Completed')
    ], default='new')
    def set_new(self):
        for rec in self:
            print("This task is new!!!")
            rec.status = 'new'
    def set_in_progress(self):
        for rec in self:
            print("This task is in progress!!!")
            rec.status = 'in_progress'

    def set_completed(self):
        for rec in self:
            print("This task is completed!!!")
            rec.status = 'completed'