import logging
from typing import List, Tuple

from odoo import models, fields, api
from datetime import datetime
from odoo.osv import expression

_logger = logging.getLogger(__name__)


class RiskModels(models.Model):
    _name = 'risk.models'
    _description = 'This applies to country risk, borrower risk, lender risk and transaction risk'
    _rec_name = 'model_name'
    _sql_constraints = [
        ('model_name_uniq', 'UNIQUE(model_name)', 'This Model already exist. Please Change the Model Name')
    ]

    model_name = fields.Char(string='Model Name', required=True)
    model_description = fields.Text(string='Model Description', required=True)
    status = fields.Selection([('1', 'Active'), ('2', 'Inactive')], required=True, default='1', readonly=True)
    # type_id = fields.Many2one('risk.models.types', string='Type', required=True)
    risk_model_factors = fields.One2many('risk.model.factor', 'risk_model_id', required=True)
    type_risk = fields.Selection([
        ('country_risk_models', 'Country Risk Models'), ('lender_risk_models', 'Lender Risk Models'),
        ('borrower_risk_models', 'Borrower Risk Models'), ('transaction_risk_models', 'Transaction Risk Model')],
        string='Type', required=True, default='country_risk_models')
    risk_model_number_of_factors = fields.Integer(string='Number of Factors', compute='_compute_number_of_factor')
    risk_model_number_of_questions = fields.Integer(string='Number of Questions',
                                                    compute='_compute_total_number_of_questions_per_model')

    def _compute_number_of_factor(self):
        for rec in self:
            rec.risk_model_number_of_factors = len(rec.risk_model_factors)

    def _compute_total_number_of_questions_per_model(self):
        for rec in self:
            somme = 0
            #print('rec', rec)
            for line in rec.risk_model_factors:
                somme += line.risk_model_number_of_questions
                #print("line", line.risk_model_number_of_questions )
            rec.risk_model_number_of_questions = somme

class RiskModelTypes(models.Model):
    _name = 'risk.models.types'
    _description = 'This applies to country risk, borrower risk, lender risk and transaction risk'
    _rec_name = 'type'

    type = fields.Char(string='Type', required=True)
    description = fields.Text(string='Description', required=True)
    code = fields.Char(string='Type', required=True)
