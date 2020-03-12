from odoo import fields, models, api, _


class HelpdeskTicket (models.Model):
    _name = 'helpdesk.ticket'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    date_deadline = fields.Datetime(string='Date limit')

    stage_id = fields.Many2one(
        comodel_name='helpdesk.ticket.stage',
        string='Stage',
        required=False)
    team_id = fields.Many2one(
        comodel_name='helpdesk.team',
        string='Team',
        required=False)
    user_ids = fields.Many2many(
        comodel_name='res.users',
        relation="helpdesk_ticket_users_rel",
        column1="ticket_id", column2="user_id",
        string='Users',)
    responsable_id = fields.Many2one(
        comodel_name='res.users',
        string='Responsable',
        required=False)

    def set_current_user_as_responsable(self):
        self.ensure_one()
        self.responsable_id = self.env.user

    @api.onchange("team_id")
    @api.depends("team_id")
    def _onchange_team_id_set_to_users(self):
        self.user_ids = False
        users = []
        if self.team_id is not None and self.team_id is not False and self.team_id.user_ids is not None and self.team_id.user_ids is not False and len(self.team_id.user_ids) > 0:
            for user in self.team_id.user_ids:
                users.append(user.id)
        self.user_ids = users
