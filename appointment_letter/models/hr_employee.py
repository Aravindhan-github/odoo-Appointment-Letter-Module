


from odoo import models, fields, api, exceptions, _


class HrEmployee(models.Model):
    _inherit = "hr.employee"


    appointment_id = fields.Many2one('appointment.letter', string="Appointment Letter")