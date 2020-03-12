from odoo import fields, models, api, _


class HelpDeskSetResponsable(models.TransientModel):
    _name = 'helpdesk.set.responsable.wiz'

    def set_current_user_as_responsable(self):
        self.ensure_one()

        ticket = self.env["helpdesk.ticket"].search([("id", "=", self.env.context.get('active_id'))])
        ticket.responsable_id = self.env.user
