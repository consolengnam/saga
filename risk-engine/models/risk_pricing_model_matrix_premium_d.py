import logging
from odoo import models, fields, api
from datetime import datetime
from odoo.osv import expression

_logger = logging.getLogger(__name__)


class RiskPricingModelMatrixPremiumD(models.Model):
    _name = 'risk.premium.d.curves'
    _description = 'No description at the moment'
    _rec_name = 'period'

    risk_pricing_model_constant = fields.One2many('risk.pricing.model.constants', 'premium_d', required=True)
    period = fields.Integer(string='Period(Tenor)', required=True)
    rate = fields.Float(string='Rate(%)', digits=(5, 2), required=True)
