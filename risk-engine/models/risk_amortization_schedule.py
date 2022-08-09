import logging
from typing import List, Tuple

from odoo import models, fields, api
from datetime import datetime
from odoo.osv import expression

_logger = logging.getLogger(__name__)


class RiskAmortizationSchedule(models.Model):
    _name = 'risk.amortization.schedule'
    _description = 'This applies to country risk, borrower risk, lender risk and transaction risk'

    amortization_schedule_ids = fields.One2many('risk.models.simulation', 'amortization_schedule_id', required=False)
    risk_amortization_period = fields.Integer(string='Period', digits=(5, 2), required=False,)
    risk_amortization_principal_amount = fields.Float(string='Principal Amount', digits=(5, 2), required=False,)
    risk_amortization_principal_repayment = fields.Float(string='Principal Repayment', digits=(5, 2), required=False,)
    risk_amortization_expected_default = fields.Float(string='Expected Default', digits=(5, 2), required=False,)
    risk_amortization_expected_claim = fields.Float(string='Expected Claim', digits=(5, 2), required=False,)
    risk_amortization_recoveries = fields.Float(string='Recoveries', digits=(5, 2), required=False,)
    risk_amortization_net_loss = fields.Float(string='Net Loss', digits=(5, 2), required=False,)
    risk_amortization_utilization_fee = fields.Float(string='Utilization Fee', digits=(5, 2), required=False,)
    risk_amortization_expected_guarantee_fee = fields.Float(string='Expected Guarantee Fee', digits=(5, 2), required=False,)