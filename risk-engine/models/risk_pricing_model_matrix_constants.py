import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class RiskPricingModelConstants(models.Model):
    _name = 'risk.pricing.model.constants'
    _description = 'No description at the moment'

    risk_premium_d_curves = fields.One2many('risk.premium.d.curves', 'conversion_factor_default_rate_id', required=True)
    risk_premium_f_curves = fields.One2many('risk.premium.f.curves', 'conversion_factor_default_rate_id', required=True)
    conversion_factor_default_rate = fields.Float('Conversion Factor Default Rate', digits=(5, 2), required=True)
    _rec_name = 'conversion_factor_default_rate'
