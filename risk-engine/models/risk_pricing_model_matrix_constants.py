import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class RiskPricingModelConstants(models.Model):
    _name = 'risk.pricing.model.constants'
    _description = 'No description at the moment'

    premium_d = fields.Float('Premium D', digits=(5, 2), required=True)
    premium_f = fields.Float('Premium F', digits=(5, 2), required=True)
    conversion_factor_default_rate = fields.Float('Conversion Factor Default Rate', digits=(5,2), required=True)