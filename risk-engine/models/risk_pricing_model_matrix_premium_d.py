import logging
from odoo import models, fields, api
from datetime import datetime
from odoo.osv import expression

_logger = logging.getLogger(__name__)


class RiskPricingModelMatrixPremiumD(models.Model):
    _name = 'risk.premium.d.curves'
    _description = 'No description at the moment'

    # risk_premium_d_curves = fields.Many2one('risk.pricing.model.constants', required=True)
    period = fields.Integer('period', required=True)
    rate = fields.Float('rate', digits=(12, 6), required=True)
