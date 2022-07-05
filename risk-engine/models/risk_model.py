import logging
from odoo import models, fields, api
from datetime import datetime
from odoo.osv import expression

_logger = logging.getLogger(__name__)


class RiskModels(models.Model):
    _name = 'risk.models'
    _description = 'This applies to country risk, borrower risk, lender risk and transaction risk'
    _rec_name = 'model_name'

    model_name = fields.Char(string='Model Name', required=True)
    model_description = fields.Text(string='Model Description', required=True)
    status = fields.Selection([('1', 'Active'), ('2', 'Inactive')], required=True, default='1')
    # type_id = fields.Many2one('risk.models.types', string='Type', required=True)
    risk_model_factors = fields.One2many('risk.model.factor', 'risk_model_id', required=True)
    type_risk = fields.Selection([
        ('country_risk_models', 'Country Risk Models'), ('lender_risk_models', 'Lender Risk Models'),
        ('borrower_risk_models', 'Borrower Risk Models'), ('transaction_risk_models', 'Transaction Risk Model')],
        string='Type', required=True, default='country_risk_models')


class RiskModelTypes(models.Model):
    _name = 'risk.models.types'
    _description = 'This applies to country risk, borrower risk, lender risk and transaction risk'
    _rec_name = 'type'

    type = fields.Char(string='Type', required=True)
    description = fields.Text(string='Description', required=True)
    #risk_models = fields.One2many('risk.models', 'type_id', string='Risks')
    code = fields.Char(string='Type', required=True)
