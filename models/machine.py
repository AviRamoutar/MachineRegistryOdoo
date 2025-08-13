# models/machine.py
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date

class Machine(models.Model):
    _name = "machinery.machine"
    _description = "Machine"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True, tracking=True)
    serial_number = fields.Char(tracking=True)
    manufacturer = fields.Char(tracking=True)
    location = fields.Char(tracking=True)
    commission_date = fields.Date(tracking=True)

    status = fields.Selection(
        [('ok', 'Healthy'), ('due', 'Due Soon'), ('down', 'Under Repair')],
        default='ok', tracking=True
    )

    maintenance_ids = fields.One2many('machinery.maintenance', 'machine_id', string="Maintenance Logs")
    next_maintenance_date = fields.Date(compute="_compute_next_maintenance_date", store=True)

    user_id = fields.Many2one('res.users', string="Assigned To", tracking=True)
    maintenance_count = fields.Integer(compute='_compute_maintenance_count')

    @api.depends('maintenance_ids.next_due_date')
    def _compute_next_maintenance_date(self):
        for rec in self:
            dates = [d for d in rec.mapped('maintenance_ids.next_due_date') if d]
            rec.next_maintenance_date = min(dates) if dates else False

    def _compute_maintenance_count(self):
        groups = self.env['machinery.maintenance'].read_group(
            [('machine_id', 'in', self.ids)], ['machine_id'], ['machine_id']
        )
        count_by = {g['machine_id'][0]: g['machine_id_count'] for g in groups}
        for rec in self:
            rec.maintenance_count = count_by.get(rec.id, 0)

    def action_open_maintenance(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _("Maintenance Logs"),
            'res_model': 'machinery.maintenance',
            'view_mode': 'tree,form,kanban',
            'domain': [('machine_id', '=', self.id)],
            'context': {'default_machine_id': self.id},
        }

    @api.model
    def create(self, vals):
        rec = super().create(vals)
        rec._schedule_assignment_activity_if_needed(vals)
        return rec

    def write(self, vals):
        res = super().write(vals)
        self._schedule_assignment_activity_if_needed(vals)
        return res

    def _schedule_assignment_activity_if_needed(self, vals):
        if 'user_id' in vals:
            for rec in self.filtered(lambda r: r.user_id):
                rec.activity_schedule(
                    'mail.mail_activity_data_todo',
                    user_id=rec.user_id.id,
                    summary=_("Maintenance assignment"),
                    note=_("You were assigned to machine: %s (SN: %s)")
                         % (rec.name or '', rec.serial_number or '')
                )

class Maintenance(models.Model):
    _name = "machinery.maintenance"
    _description = "Maintenance Log"
    _order = "date desc, id desc"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    machine_id = fields.Many2one('machinery.machine', required=True, ondelete='cascade', tracking=True)
    date = fields.Date(default=fields.Date.today, required=True, tracking=True)

    report_type = fields.Selection([
        ('ok', 'Good to go!'),
        ('advice', 'Preventive advice'),
        ('part', 'Needs part'),
    ], default='ok', required=True, tracking=True)

    note = fields.Text(help="e.g. Keep belt lubed; relube every 2 weeks")

    product_id = fields.Many2one('product.product', string="Part")
    quantity = fields.Float(default=1.0)

    next_due_date = fields.Date(string="Next Maintenance Due")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('to_approve', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('done', 'Done'),
    ], default='draft', tracking=True)

    approved_by = fields.Many2one('res.users', readonly=True)
    approved_on = fields.Datetime(readonly=True)
    reject_reason = fields.Char(readonly=True)
    purchase_id = fields.Many2one('purchase.order', readonly=True, copy=False)

    def action_submit(self):
        self.write({'state': 'to_approve'})
        manager_group = self.env.ref('base.group_system')
        for rec in self:
            rec.message_post(body=_('Submitted for approval.'))
            for user in manager_group.users:
                rec.activity_schedule(
                    'mail.mail_activity_data_todo', user_id=user.id,
                    summary=_("Review maintenance report"),
                    note=_("Machine: %s\nType: %s\nNote: %s") % (
                        rec.machine_id.display_name,
                        dict(self._fields['report_type'].selection).get(rec.report_type),
                        rec.note or ''
                    )
                )

    def action_approve(self):
        for rec in self:
            if rec.report_type == 'part' and rec.product_id and rec.quantity > 0 and not rec.purchase_id:
                po = self.env['purchase.order'].create({
                    'partner_id': rec.env.user.company_id.partner_id.id,
                    'order_line': [(0, 0, {
                        'product_id': rec.product_id.id,
                        'name': rec.product_id.display_name,
                        'product_qty': rec.quantity,
                        'price_unit': rec.product_id.standard_price or 0.0,
                        'date_planned': fields.Datetime.now(),
                    })]
                })
                rec.purchase_id = po.id
            rec.write({
                'state': 'approved',
                'approved_by': self.env.user.id,
                'approved_on': fields.Datetime.now(),
                'reject_reason': False,
            })
            rec.message_post(body=_("Approved by %s") % self.env.user.display_name)

    def action_reject_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Reject Maintenance Report'),
            'res_model': 'machinery.maintenance.reject.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_maintenance_id': self.id}
        }

    def action_reject(self, reason=False):
        reason = reason or _("No reason provided")
        self.write({'state': 'rejected', 'reject_reason': reason})
        self.message_post(body=_("Rejected by %s: %s") % (self.env.user.display_name, reason))

    def action_mark_done(self):
        self.write({'state': 'done'})
        for rec in self:
            rec.message_post(body=_('Marked as Done.'))

# Reject Wizard
class MaintenanceRejectWizard(models.TransientModel):
    _name = 'machinery.maintenance.reject.wizard'
    _description = 'Maintenance Reject Wizard'

    maintenance_id = fields.Many2one('machinery.maintenance', required=True)
    reason = fields.Text(required=True)

    def action_reject(self):
        self.maintenance_id.action_reject(self.reason)
        return {'type': 'ir.actions.act_window_close'}