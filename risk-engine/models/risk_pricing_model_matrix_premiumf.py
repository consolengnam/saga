import logging
from odoo import models, fields, api
from datetime import datetime
from odoo.osv import expression

_logger = logging.getLogger(__name__)


class RiskPricingModelMatrixPremium(models.Model):
    _name = 'risk.premium.f.curves'
    _description = 'Pricing model matrix - premium F'

    _rec_name = 'period'
    period = fields.Integer('period', required=True)
    rate = fields.Float('rate', digits=(12, 6), required=True)
    status = fields.Selection([('1', 'Active'), ('2', 'Inactive')], required=True, default='1')
    conversion_factor_default_rate_id = fields.Many2one('risk.pricing.model.constants', string='Conversion_factor_default_rate' , required=True)