{
    'name': 'Appointment Letter Management',
    'version': '1.0',
    'summary': 'Manage Appointment Letters',
    'description': 'A module to manage appointment letters for employees.',
    'depends':['mail','hr'],
    'author': 'Aravindhan',
    'data': [
        'security/ir.model.access.csv',
        'views/appointment_letter_views.xml',
        'views/menu.xml',
        'report/report.xml',
        'report/letter.xml',
        'views/hr_employee_views.xml',
        'views/company_rules_views.xml',
        'data/sequence.xml',
        'security/appointment_letter_record_rules.xml',
        'security/groups.xml',
        'data/mail_template.xml'
    ],

    'installable': True,
    'application': True,

}