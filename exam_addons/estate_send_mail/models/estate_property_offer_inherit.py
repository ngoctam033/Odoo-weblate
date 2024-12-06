from odoo import models, fields, api, _
from odoo.exceptions import UserError


# create a model estate.property.offer for the estate module
class EstatePropertyOffer(models.Model):
    _inherit = 'estate.property.offer'

    user_accept = fields.Many2one('res.users', string='Accepted By')
    user_reject = fields.Many2one('res.users', string='Rejected By')


    def action_accept(self):
        mail_template = self.env.ref('estate_send_mail.email_template_estate_property_offer')
        for record in self:
            if record.status == 'refused':
                raise UserError(_('A refused offer cannot be accepted.'))
            record.user_accept = self.env.user
            record.status = 'accepted'
            record.property_id.write({'state': 'offer_accepted'})
            record.property_id.write({'selling_price': record.price})
            record.property_id.buyer_id = record.partner_id
            record.property_id.buyer_mail = record.partner_id.email
        mail_template.send_mail(self.id, force_send=True)


    def action_refuse(self):
        super(EstatePropertyOffer, self).action_refuse()
        self.user_reject = self.env.user