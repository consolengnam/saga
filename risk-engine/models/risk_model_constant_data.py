import logging
from odoo import models, fields, api
from datetime import datetime
from odoo.osv import expression

_logger = logging.getLogger(__name__)

class RiskAgencyDefaultRates(models.Model):
    _name = 'risk.agency.default.rates'
    _description = 'This applies to RiskAgencyDefaultRates'
    _rec_name = 'period'

    period = fields.Integer(required=True)
    rating = fields.Integer(required=True)
    value = fields.Float(required=True)


class RiskFreeVectors(models.Model):
    _name = 'risk.free.vectors'
    _description = 'This applies to RiskFreeVectors'
    _rec_name = 'period'

    period = fields.Integer(required=True)
    treasury_rate = fields.Float(required=True)

