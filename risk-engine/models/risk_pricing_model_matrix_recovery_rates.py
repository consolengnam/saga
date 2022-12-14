import logging
from odoo import models, fields, api
from datetime import datetime
from odoo.osv import expression


_logger = logging.getLogger(__name__)


class RecoveryRates(models.Model):

    _name = 'risk.recovery.rate'
    _description = 'Pricing model matrix'
    _rec_name = 'rate'

    rate = fields.Float(string='Rate(%)', digits=(5, 2), required=True)
    status = fields.Selection([('1', 'Active'), ('2', 'Inactive')], required=True, default='1' , readonly=True)
    country_id = fields.Many2one('res.country', string='Country', required=True)
