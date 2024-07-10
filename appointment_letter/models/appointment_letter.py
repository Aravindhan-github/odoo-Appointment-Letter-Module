from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AppointmentLetter(models.Model):
    _name = 'appointment.letter'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Appointment Letter'

    name = fields.Char(string='Sequence', copy=False, readonly=True, index=True,default='New')
    name_id = fields.Char(string='Candidate')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company.id)
    work_phone = fields.Char(string='Work Phone',size=10)
    mobile_phone = fields.Char(string='Mobile Phone',size=10)
    hr_id = fields.Many2one('res.users', string='HR', default=lambda self: self.env.user)
    job_id = fields.Many2one('hr.job',string='Job')
    mail = fields.Char(string="email")
    appointment_date = fields.Date(string='Joining Date')
    user_id = fields.Many2one("res.users",string="HR email")

    salary = fields.Float(string='Salary')
    street = fields.Char(string='Street')
    street2 = fields.Char(string='street2')
    city = fields.Char(string='City')
    state_id = fields.Many2one('res.country.state', string='State')
    #state = fields.Char(string='State')
    pincode = fields.Char(string='pincode')
    country_id = fields.Many2one('res.country', string='Country')
    rule_ids = fields.One2many('appointment.rule', 'appointment_rule_id', string='Company Rules')
    tag_ids = fields.Many2many('appointment.tag',string= 'Tags')
    image_128 = fields.Image(string="Image", max_width=100, max_height=100)
    employee_id = fields.Many2one('hr.employee', string='Employee',readonly=True)


    status = fields.Selection([
        ('draft', 'Draft'),
        ('verified', 'Verified'),
        ('done', 'Done'),
        ('cancelled','Cancelled')
    ], default='draft', string='Status', tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            a = self.env['ir.sequence'].next_by_code('appointment.letter.seq')
            print(a,"aaa")
            vals['name'] = self.env['ir.sequence'].next_by_code('appointment.letter.seq') or ('New')
            print(vals['name'],"vals['name']")
        return super(AppointmentLetter, self).create(vals)




    @api.constrains('work_phone')
    def _check_work_No_length(self):
        for record in self:
            if record.work_phone and len(record.work_phone) != 10:
                raise ValidationError('Phone number must be exactly 10 digits long.')

    @api.constrains('mobile_phone')
    def _check_mobile_No_length(self):
        for record in self:
            if record.mobile_phone and len(record.mobile_phone) != 10:
                raise ValidationError('Phone number must be exactly 10 digits long.')



    def action_draft(self):
        self.write({'status': 'draft'})


    def action_verify(self):
        self.write({'status': 'verified'})

    def action_done(self):
        self.write({'status': 'done'})

    def action_cancel(self):
        self.write({'status':'cancelled'})

    def action_create_employee(self):
        self.ensure_one()


        employee_vals = {
            'name': self.name_id,
            'work_email': self.mail,
            'work_phone': self.work_phone,
            'mobile_phone': self.mobile_phone,
            'job_id': self.job_id.id,
            'appointment_id': self.id,
            'active': True,
        }

        employee = self.env['hr.employee'].create(employee_vals)

        self.employee_id = employee.id





    def apply_rules(self):
        appointment_rule_obj = self.env['appointment.rule']
        company_rule_objs = self.env['company.rules'].search([])

        for company_rule in company_rule_objs:
            vals = {
                'name': company_rule.name,
                'description': company_rule.description,
                'company_rule_id': company_rule.id,
                'appointment_rule_id': self.id
            }
            appointment_rule_obj.create(vals)

    def action_send_mail(self):
        template = self.env.ref('appointment_letter.appointment_letter_email_template')

        for rec in self:
            template.send_mail(rec.id,force_send=True)

    # def action_send_mail(self):
    #     template=self.env.ref('appointment_letter.appointment_letter_email_template')


class Appointmentrule(models.Model):
    _name = 'appointment.rule'
    _description = 'Company Rule'

    company_rule_id = fields.Many2one('company.rules', string='Company Rule')
    name = fields.Char(string='Rule Name', related='company_rule_id.name', readonly=True)
    description = fields.Text(string='Description', related='company_rule_id.description', readonly=True)
    #name_id = fields.Many2one('company.rules',string='Rule Name')

    #description = fields.Many2one('company.rules',string='Description')


    appointment_rule_id = fields.Many2one('appointment.letter', string='Appointment Letter')

