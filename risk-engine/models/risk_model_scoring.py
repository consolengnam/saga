import logging
from odoo import models, fields, api
from datetime import datetime
from odoo.osv import expression

_logger = logging.getLogger(__name__)


class RiskModelSubFactorAnswers(models.Model):
    _name = 'risk.model.sub.factor.answers'
    _description = 'This applies to country risk, borrower risk, lender risk and transaction risk'

    answer = fields.Text(required=True)
    point = fields.Char(required=True)
    risk_model_subfactor_id = fields.Many2one('risk.model.sub.factor', 'subfactor_name', required=True)


class RiskModelSubFactor(models.Model):
    _name = 'risk.model.sub.factor'
    _description = 'This applies to country risk, borrower risk, lender risk and transaction risk'

    subfactor_name = fields.Char(string='sub factor name', required=True)
    subfactor_description = fields.Text(string='factor sub description', required=True)
    weight = fields.Float(compute="_value_pc", store=True)
    risk_model_sub_factor_answers = fields.One2many('risk.model.sub.factor.answers', 'risk_model_subfactor_id', required=True)
    risk_model_factor_id = fields.Many2one('risk.model.factor', 'factor_name', required=True)
    _rec_name = 'subfactor_name'


class RiskModelFactor(models.Model):
    _name = 'risk.model.factor'
    _description = 'This applies to country risk, borrower risk, lender risk and transaction risk'

    factor_name = fields.Char(string='name factor', required=True)
    factor_description = fields.Text(string='Risk Description')
    Weight = fields.Float(compute="_value_pc", store=True)
    risk_model_id = fields.Many2one('risk.models', 'model_name', required=True)
    risk_model_sub_factors = fields.One2many('risk.model.sub.factor', 'risk_model_factor_id', required=True)
    _rec_name = 'factor_name'

#
# class RiskModels(models.Model):
#     _name = 'risk.models'
#     _description = 'This applies to country risk, borrower risk, lender risk and transaction risk'
#
#     model_name = fields.Char(string='Model Name', required=True)
#     model_description = fields.Text(string='Model Description', required=True)
#     status = fields.Selection([('1', 'Active'), ('2', 'Inactive')], required=True, default='1')
#     type_id = fields.Many2one('risk.models.types', string='Type', required=True)
#     risk_model_factor = fields.One2many('risk.model.factor', 'risk_model_id', required=True)
#
#
# class RiskModelTypes(models.Model):
#     _name = 'risk.models.types'
#     _description = 'This applies to country risk, borrower risk, lender risk and transaction risk'
#
#     type = fields.Char(string='Type', required=True)
#     description = fields.Text(string='Description', required=True)
#     risk_models = fields.One2many('risk.models', 'type_id', string='Risks')
