from odoo import models, fields, api
class AppointmentTag(models.Model):
    _name = 'appointment.tag'
    _description = 'Appointment Tag'

    name = fields.Char(string='Tag Name', required=True)