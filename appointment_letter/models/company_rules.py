from odoo import models, fields

class CompanyRules(models.Model):
    _name = 'company.rules'
    _description = 'Company Rules'

    name = fields.Char(string='Rule Name', required=True)
    description = fields.Text(string='Description')
