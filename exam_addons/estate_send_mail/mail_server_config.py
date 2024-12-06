from odoo import api, SUPERUSER_ID

def configure_mail_server(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    mail_server = env['ir.mail_server'].search([('smtp_user', '=', '2151040051@ut.edu.vn')], limit=1)
    if not mail_server:
        env['ir.mail_server'].create({
            'name': 'Gmail SMTP Server',
            'smtp_host': 'smtp.gmail.com',
            'smtp_port': 587,
            'smtp_user': '2151040051@ut.edu.vn',
            'smtp_pass': '*#0303*#@@',
            'smtp_encryption': 'starttls',
            'sequence': 10,
            'active': False,
        })
    else:
        mail_server.write({
            'smtp_host': 'smtp.gmail.com',
            'smtp_port': 587,
            'smtp_user': '2151040051@ut.edu.vn',
            'smtp_pass': '*#0303*#@@',
            'smtp_encryption': 'starttls',
            'sequence': 1,
            'active': False,
        })