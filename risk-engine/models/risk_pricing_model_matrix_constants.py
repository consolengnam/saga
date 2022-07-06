import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class RiskPricingModelConstants(models.Model):
    _name = 'risk.pricing.model.constants'
    _description = 'No description at the moment'
    _rec_name = 'conversion_factor_default_rate'

    premium_d = fields.Many2one('risk.premium.d.curves', string='Premium D', required=True)
    premium_f = fields.Many2one('risk.premium.f.curves', string='Premium F', required=True)
    conversion_factor_default_rate = fields.Float(string='Conversion Factor Default Rate', digits=(5, 2), required=True)
