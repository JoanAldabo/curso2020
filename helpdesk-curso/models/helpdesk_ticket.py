from odoo import fields, models, api, _


class HelpdeskTicket(models.Model):
    _name = 'helpdesk.ticket'

    _inherit = ['mail.thread', 'mail.activity.mixin']

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
        string='Users', )
    responsable_id = fields.Many2one(
        comodel_name='res.users',
        string='Responsable',
        required=False)
    ticket_qty = fields.Integer(
        string="Ticket Quantity",
        compute="_compute_tickets_qty"
    )

    @api.depends("responsable_id")
    def _compute_tickets_qty(self):
        ticket_env = self.env["helpdesk.ticket"]
        for ticket in self:
            responsable = ticket.responsable_id
            stage = ticket.stage_id
            # (A o B) y C
            tickets = ticket_env.search([
                '&',
                ('stage_id', '=', stage.id),
                '|',
                ('responsable_id', '=', responsable.id),
                ('responsable_id', '=', False)
            ])

    def set_current_user_as_responsable(self):
        self.ensure_one()
        self.responsable_id = self.env.user

    @api.onchange("team_id")
    @api.depends("team_id")
    def _onchange_team_id_set_to_users(self):
        self.user_ids = False
        users = []
        if self.team_id is not None and self.team_id is not False and self.team_id.user_ids is not None and self.team_id.user_ids is not False and len(
                self.team_id.user_ids) > 0:
            for user in self.team_id.user_ids:
                users.append(user.id)
        self.user_ids = users

    @api.onchange("date_deadline", "name")
    @api.depends("date_deadline", "name")
    def _onchange_date_deadline_name(self):
        self.description = "{}:\t{}".format("" if self.name is None or self.name is False else self.name,
                                            "" if self.date_deadline is None or self.date_deadline is False else
                                            self.date_deadline.strftime("%d/%m/%Y"))
