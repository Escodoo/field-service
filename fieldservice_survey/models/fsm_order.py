# Copyright 2023 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class FsmOrder(models.Model):

    _inherit = "fsm.order"

    partner_feedback_ids = fields.Many2many("res.partner", string="Asked Feedback")
    person_partner_id = fields.Many2one("res.partner", related="person_id.partner_id")
    person_user_ids = fields.One2many("res.users", related="person_partner_id.user_ids")

    def action_ask_feedback(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "fsm.order.appraisal.ask.feedback",
            "target": "new",
            "name": "Ask Feedback",
        }

    def action_open_survey_inputs(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_url",
            "name": "Survey Feedbacks",
            "target": "self",
            "url": "/fsm_order/%s/results/" % (self.id),
        }
