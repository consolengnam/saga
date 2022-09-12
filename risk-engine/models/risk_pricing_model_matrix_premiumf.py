import logging
from odoo import models, fields, api
from datetime import datetime
from odoo.osv import expression

_logger = logging.getLogger(__name__)


class RiskPricingModelMatrixPremium(models.Model):
    _name = 'risk.premium.f.curves'
    _description = 'No description at the moment'

    period = fields.Integer(string='Period(Tenor)', required=True)
    rate = fields.Float(string='Rate(%)', digits=(5, 2), required=True)
    risk_pricing_model_constants = fields.One2many('risk.pricing.model.constants', 'premium_f', required=True)
    _rec_name = 'period'
