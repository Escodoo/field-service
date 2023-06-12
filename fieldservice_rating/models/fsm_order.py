# Copyright 2023 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.tools.safe_eval import safe_eval


class FsmOrder(models.Model):
    _name = 'fsm.order'
    _inherit = ["fsm.order", "rating.mixin"]

    positive_rate_percentage = fields.Integer(
        string="Positive Rates Percentage",
        compute="_compute_percentage",
        store=True,
        default=-1,
    )

    rating_status = fields.Selection(
        selection=[
            ("stage_change", "Rating when changing stage"),
            ("no_rate", "No rating"),
        ],
        string="Customer Rating",
        default="stage_change",
        require=True,
    )

    @api.depends("rating_ids.rating")
    def _compute_percentage(self):
        for fsm_order in self:
            activity = fsm_order.rating_get_grades()
            fsm_order.positive_rate_percentage = (
                activity["great"] * 100 / sum(activity.values())
                if sum(activity.values())
                else -1
            )

    def write(self, vals):
        res = super().write(vals)
        if "stage_id" in vals and vals.get("stage_id"):
            stage = self.env["fsm.stage"].browse(vals.get("stage_id"))
            if stage.rating_mail_template_id:
                self._send_fsm_order_rating_mail(force_send=False)
        return res

    def _send_fsm_order_rating_mail(self, force_send=False):
        for fsm_order in self:
            if fsm_order.rating_status == "stage_change":
                survey_template = fsm_order.stage_id.rating_mail_template_id
                if survey_template:
                    fsm_order.rating_send_request(
                        survey_template,
                        lang=fsm_order.location_id.partner_id.lang,
                        force_send=force_send,
                    )

    def rating_apply(self, rate, token=None, feedback=None, subtype=None):
        return super().rating_apply(
            rate,
            token=token,
            feedback=feedback,
            subtype="fieldservice_rating.mt_fsm_order_rating",
        )

    def rating_get_partner_id(self):
        res = super().rating_get_partner_id()
        if not res and self.location_id.partner_id:
            return self.location_id.partner_id
        return res

    def rating_get_rated_partner_id(self):
        res = super().rating_get_partner_id()
        if hasattr(self, 'person_id') and self.person_id.partner_id:
            return self.person_id.partner_id
        return res

    def rating_get_parent_model_name(self, vals):
        return "fsm.order"

    def rating_get_fsm_order_id(self):
        return self.id

    def action_view_fsm_order_rating(self):
        action = self.env["ir.actions.act_window"].for_xml_id(
            "fieldservice_rating", "fieldservice_fsm_order_rating_action"
        )
        action["name"] = _("FSM Order Rating")
        action_context = safe_eval(action["context"]) if action["context"] else {}
        action_context.update(self._context)
        action_context.pop("group_by", None)
        return dict(action, context=action_context)
