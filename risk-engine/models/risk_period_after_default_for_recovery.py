import logging
from odoo import models, fields, api
from datetime import datetime
from odoo.osv import expression

_logger = logging.getLogger(__name__)


class PeriodAfterDefaultforRecoveries(models.Model):
    _name = 'risk.period.after.default.for.recovery'
    _description = 'Pricing model matrix period after default for recovery'
    _rec_name = 'period'

    period = fields.Float(string='Period(Tenor)', digits=(5, 2), required=True)
    status = fields.Selection([('1', 'Active'), ('2', 'Inactive')], required=True, default='1' , readonly=True)
    country_id = fields.Many2one('res.country', string='Country', required=True)

