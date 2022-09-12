import logging
from odoo import models, fields, api
from datetime import datetime
from odoo.osv import expression
from odoo.exceptions import  ValidationError
_logger = logging.getLogger(__name__)


class RiskModelSubFactorAnswers(models.Model):
    _name = 'risk.model.sub.factor.answers'
    _description = 'This applies to country risk, borrower risk, lender risk and transaction risk'
    _rec_name = 'answer'

    answer = fields.Text(required=True)
    # point = fields.Char(required=True)
    point = fields.Float(required=True)
    risk_model_subfactor_id = fields.Many2one('risk.model.sub.factor', 'subfactor_name', required=True)

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "{} {}".format(record.answer, record.point)))
            # if self.env.context.get('custom_search', False):
            #     result.append((record.id, "{} {}".format(record.name, record.address)))
            # else:
            #     result.append((record.id, record.name))
        return result


class RiskModelSubFactorAnswersWizard(models.TransientModel):
    _name = 'risk.model.sub.factor.answers.wizard'
    _description = 'This applies to country risk, borrower risk, lender risk and transaction risk'
    _rec_name = 'answer'

    answer = fields.Text(required=True)
    # point = fields.Char(required=True)
    point = fields.Float(required=True)
    risk_model_subfactor_id = fields.Many2one('risk.model.sub.factor', 'subfactor_name', required=True)


class RiskModelSubFactor(models.Model):
    _name = 'risk.model.sub.factor'
    _description = 'This applies to country risk, borrower risk, lender risk and transaction risk'
    _rec_name = 'subfactor_name'
    _sql_constraints = [
        ('subfactor_name_uniq', 'UNIQUE(subfactor_name)',
         'Sub Factor name Duplicated. Please Change the Sub Factor Name')
    ]

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
    _sql_constraints = [
        ('factor_name_uniq', 'UNIQUE(factor_name)',
         'Factor name Duplicated. Please Change the Factor Name'),
    ]
    factor_name = fields.Char(string='Name Factor', required=True)
    factor_description = fields.Text(string='Risk Description')
    Weight = fields.Float(store=True)
    risk_model_id = fields.Many2one('risk.models', 'model_name', required=True)
    risk_model_sub_factors = fields.One2many('risk.model.sub.factor', 'risk_model_factor_id', required=True)
    risk_model_number_of_questions = fields.Integer(string='Number of Questions',
                                                    compute='_compute_number_of_questions', required=False)
    # factor_total_weight = fields.Float(compute='_sum_weight', required=False)

    @api.depends('risk_model_sub_factors')
    def _compute_number_of_questions(self):
        for rec in self:
            rec.risk_model_number_of_questions = len(rec.risk_model_sub_factors)

    # @api.constrains('factor_total_weight')
    # def _sum_weight(self):
    #     weight = []
    #     for rec in self:
    #         weight.append(rec.Weight)
    #     self.factor_total_weight = sum(weight)
    #     print(rec.factor_total_weight)
    #     if rec.factor_total_weight > 400:
    #         raise ValidationError('The total weight most be lower than 100%')

