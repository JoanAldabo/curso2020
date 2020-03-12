from odoo import fields, models, api, _


class HelpDeskSetResponsable(models.TransientModel):
    _name = 'helpdesk.set.responsable.wiz'

    tickets_qty = fields.Integer(string="Tickets Qty")

    @api.model
    def _default_get(self, fields):
        res = super(HelpDeskSetResponsable, self).default_get(fields)
        qty = len(self.env["helpdesk.ticket"].search([('responsable_id', '=', self.env.uid)]))
        res['tickets_qty'] = qty
        return res

    def set_current_user_as_responsable(self):
        self.ensure_one()
        active_id = self.env.context.get('active_id')
        active_model = self.env.context.get('active_model')

        if active_id and active_model and active_model == "helpdesk.ticket":
            ticket = self.env["helpdesk.ticket"].browse(active_id)
            ticket.responsable_id = self.env.user
