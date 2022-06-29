import logging
from odoo import models, fields, api


_logger = logging.getLogger(__name__)


class RiskPremiumDCurves(models.Model):
    _name = 'risk.premium.d.curves'
    _description = 'No description at the moment'

    period = fields.Integer('Period', required=True)
    rate = fields.Float('Rate', digits=(5, 2), required=True)