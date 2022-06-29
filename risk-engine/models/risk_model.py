import logging
from odoo import models, fields, api
from datetime import datetime
from odoo.osv import expression


_logger = logging.getLogger(__name__)


class RiskModels(models.Model):
    _name = 'risk.models'
    _description = 'This applies to country risk, borrower risk, lender risk and transaction risk'

    model_name = fields.Char(string='Model Name', required=True)
    model_description = fields.Text(string='Model Description', required=True)
    status = fields.Selection([('1', 'Active'), ('2', 'Inactive')], required=True,   default='1')
    type_id = fields.Many2one('risk.models.types', string='Type', required=True)


class RiskModelTypes(models.Model):
    _name = 'risk.models.types'
    _description = 'This applies to country risk, borrower risk, lender risk and transaction risk'

    risk_type = fields.Char(string='Type', required=True)
    risk_description = fields.Text(string='Description', required=True)
    risk_models = fields.One2many('risk.models', 'type_id', string='Risks')






