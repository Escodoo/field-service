# Copyright 2023 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class FsmStage(models.Model):
    _inherit = "fsm.stage"

    rating_mail_template_id = fields.Many2one(
        comodel_name="mail.template",
        string="Rating Email Template",
        domain=[("model", "=", "fsm.order")],
        help="If set, an email will be sent to the customer  "
        "with a rating survey when the fsm order reaches this stage.",
    )
