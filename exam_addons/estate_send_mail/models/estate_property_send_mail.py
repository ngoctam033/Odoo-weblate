from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import re

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    # Thêm trường buyer_mail
    buyer_mail = fields.Char(string='Buyer Mail', tracking=True)
    # Thêm trường user_sold
    user_sold = fields.Many2one('res.users', string='Sold By', tracking=True)

    @api.onchange('buyer_id')
    def _onchange_buyer_id(self):
        if self.buyer_id:
            self.buyer_mail = self.buyer_id.email
        else:
            self.buyer_mail = ''

    @api.onchange('buyer_mail')
    def _onchange_buyer_mail(self):
        if self.buyer_mail:
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_regex, self.buyer_mail):
                self.buyer_mail = ''
                return {
                    'warning': {
                        'title': "Invalid Email",
                        'message': "The email address is not valid. Please enter a valid email address.",
                    }
                }
                
    @api.constrains('buyer_mail')
    def _check_buyer_mail(self):
        for record in self:
            if record.buyer_mail:
                email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(email_regex, record.buyer_mail):
                    raise ValidationError("The email address is not valid: %s" % record.buyer_mail)
                
    def action_set_sold(self):
        super(EstateProperty, self).action_set_sold()
        self.user_sold = self.env.user

    def action_send_mail(self):
        template = self.env.ref('estate_send_mail.email_template_estate_property')
        template.send_mail(self.id, force_send=True)
        template.auto_delete = False