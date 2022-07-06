import logging
from odoo import models, fields, api
from datetime import datetime
from odoo.osv import expression

_logger = logging.getLogger(__name__)


class RiskModelSubFactorAnswers(models.Model):
    _name = 'risk.model.sub.factor.answers'
    _description = 'This applies to country risk, borrower risk, lender risk and transaction risk'
    _rec_name = 'answer'

    answer = fields.Text(required=True)
    point = fields.Char(required=True)
    risk_model_subfactor_id = fields.Many2one('risk.model.sub.factor', 'subfactor_name', required=True)


class RiskModelSubFactor(models.Model):
    _name = 'risk.model.sub.factor'
    _description = 'This applies to country risk, borrower risk, lender risk and transaction risk'
    _rec_name = 'subfactor_name'

    subfactor_name = fields.Char(string='sub factor name', required=True)
    subfactor_description = fields.Text(string='factor sub description', required=True)
    weight = fields.Float(store=True)
    risk_model_sub_factor_answers = fields.One2many('risk.model.sub.factor.answers', 'risk_model_subfactor_id',
                                                    required=True)
    risk_model_factor_id = fields.Many2one('risk.model.factor', 'factor_name', required=True)


class RiskModelFactor(models.Model):
    _name = 'risk.model.factor'
    _description = 'This applies to country risk, borrower risk, lender risk and transaction risk'
    _rec_name = 'factor_name'

    factor_name = fields.Char(string='Name Factor', required=True)
    factor_description = fields.Text(string='Risk Description')
    Weight = fields.Float(store=True)
    risk_model_id = fields.Many2one('risk.models', 'model_name', required=True)
    risk_model_sub_factors = fields.One2many('risk.model.sub.factor', 'risk_model_factor_id', required=True)
