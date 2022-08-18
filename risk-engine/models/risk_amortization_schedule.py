import logging
from typing import List, Tuple

from odoo import models, fields, api
from datetime import datetime
from odoo.osv import expression

_logger = logging.getLogger(__name__)

class RiskAmortizationSchedule(models.Model):
    _name = 'risk.amortization.schedule'
    _description = 'This applies to country risk, borrower risk, lender risk and transaction risk'

    #amortization_schedule_ids = fields.One2many('risk.models.simulation', 'amortization_schedule_id', required=False)
    amortization_schedule_id = fields.Many2one('risk.models.simulation', string='Amortization Schedule', required=False)

    risk_amortization_period = fields.Integer(string='Period', related='amortization_schedule_id.amortization_period', required=False)
    risk_amortization_facility_amount = fields.Float(string='Facility Amount', digits=(5, 2),
                                                     related='amortization_schedule_id.facility_amount',
                                                     required=False)
    risk_amortization_principal_amount = fields.Float(string='Principal Amount', related='amortization_schedule_id.amortization_principal_amount', digits=(5, 2),
                                                      required=False)

    risk_amortization_principal_repayment = fields.Float(string='Principal Repayment',
                                                         related='amortization_schedule_id.amortization_principal_repayment',
                                                         digits=(5, 2), required=False, )
    risk_amortization_probability_of_default = fields.Float(string='Probaility of Default',
                                                         related='amortization_schedule_id.amortization_probability_of_default',
                                                         digits=(5, 2), required=False, )
    risk_amortization_expected_default = fields.Float(string='Expected Default', digits=(5, 2), required=False, )
    risk_amortization_expected_claim = fields.Float(string='Expected Claim', digits=(5, 2), required=False, )
    risk_amortization_recoveries = fields.Float(string='Recoveries', digits=(5, 2), required=False, )
    risk_amortization_net_loss = fields.Float(string='Net Loss', digits=(5, 2), required=False, )
    risk_amortization_utilization_fee = fields.Float(string='Utilization Fee', digits=(5, 2), required=False, )
    risk_amortization_expected_guarantee_fee = fields.Float(string='Expected Guarantee Fee', digits=(5, 2),
                                                            required=False)


    def _compute_amortization_period(self):

        for rec in self:
            period_choose = rec.period_id.id
            print(period_choose)
            step = 1
            while(step <= period_choose):
                rec.amortization_period = step
                print(step)
                step += 1
            # rec.amortization_period = rec.period
            # print(rec.amortization_period)

