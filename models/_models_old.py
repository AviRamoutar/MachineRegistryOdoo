# -*- coding: utf-8 -*-
from odoo import models, fields, _

class MachineryMaintenance(models.Model):
    _name = 'machinery.maintenance'
    _description = 'Machinery Maintenance'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc, id desc'

    machine_id = fields.Many2one('machinery.machine', string='Machine', required=True, tracking=True)
    date = fields.Date(string='Date', default=fields.Date.context_today, tracking=True)
    note = fields.Text(string='Notes')
    product_id = fields.Many2one('product.product', string='Product/Part')  # <- matches view
    quantity = fields.Float(string='Quantity', default=1.0)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('to_approve', 'To Approve'),
        ('approved', 'Approved'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], default='draft', tracking=True)

    # -- Buttons used by the form footer ---------------------------------------
    def action_submit(self):
        self.write({'state': 'to_approve'})
        for r in self:
            r.message_post(body=_('Submitted for approval.'))

    def action_approve(self):
        self.write({'state': 'approved'})
        for r in self:
            r.message_post(body=_('Approved.'))

    def action_reject(self):
        # simple flow: send back to draft
        self.write({'state': 'draft'})
        for r in self:
            r.message_post(body=_('Rejected and moved back to Draft.'))

    def action_mark_done(self):
        self.write({'state': 'done'})
        for r in self:
            r.message_post(body=_('Marked as Done.'))
