from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import date
class Machine(models.Model):
    _name = "machinery.machine"
    _description = "Machine"

    name = fields.Char(required=True)
    serial_number = fields.Char()
    manufacturer = fields.Char()
    location = fields.Char()
    commission_date = fields.Date()
    status = fields.Selection(
        [("ok", "Healthy"), ("due", "Due Soon"), ("down", "Under Repair")],
        default="ok",
    )
    maintenance_ids = fields.One2many("machinery.maintenance", "machine_id", string="Maintenance Logs")
    next_maintenance_date = fields.Date(compute="_compute_next_maintenance_date", store=True)

    @api.depends("maintenance_ids.next_due_date")
    def _compute_next_maintenance_date(self):
        for rec in self:
            dates = [d for d in rec.mapped("maintenance_ids.next_due_date") if d]
            rec.next_maintenance_date = min(dates) if dates else False

class Maintenance(models.Model):
    _name = "machinery.maintenance"
    _description = "Maintenance Log"
    _order = "date desc"

    machine_id = fields.Many2one("machinery.machine", required=True, ondelete="cascade")
    date = fields.Date(default=fields.Date.today, required=True)
    type = fields.Selection([("pm", "Preventive"), ("cm", "Corrective")], default="pm")
    hours_run = fields.Float()
    description = fields.Text()
    parts_used = fields.Char()
    next_due_date = fields.Date()
    cost = fields.Float()

    @api.constrains("next_due_date", "date")
    def _check_due_after_date(self):
        for rec in self:
            if rec.next_due_date and rec.date and rec.next_due_date < rec.date:
                raise UserError("Next due date must be on/after maintenance date.")
