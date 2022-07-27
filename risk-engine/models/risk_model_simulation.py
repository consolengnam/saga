import logging
from odoo import models, fields, api
from datetime import datetime
from odoo.osv import expression

_logger = logging.getLogger(__name__)


class RiskModelsSimulation(models.Model):
    '''This class is for simulation of Risk transaction ie Country Risk Simulation, Lender Risk Simulation, Borrower Riqk Simualtion and Transaction Risk Simulation
    NB:we will revisite this class to more refactorie the code in a futur iteration'''

    _name = 'risk.models.simulation'
    _description = 'This applies to simulation of country risk, borrower risk, lender risk and transaction risk'
    _rec_name = 'model_simulation_name'

    model_simulation_name = fields.Char(string='Model Simulation Name', required=True)
    model_simulation_description = fields.Text(string='Model Simulation Description', required=False)
    status = fields.Selection([('1', 'In progress'), ('2', 'Ended')], required=True, default='1')

    def _get_risk_models(self):
        print("-------------bonjour------------------")
        print(self._context)

    risk_model_ids = fields.Many2many('risk.models', string='Country Risk', required=False)
    # risk_model_country_ids = fields.Many2many('risk.models', string='Country Risk', required=False)
    # risk_model_lender_ids = fields.Many2many('risk.models', string='Country Risk', required=False)

    country_risk_model_id = fields.Many2one('risk.models', string='Country Risk',
                                            domain="[('type_risk', '=', 'country_risk_models')]", required=False)

    # country_risk_model_id = fields.Many2one('risk.models', string='Country Risk', domain="[('type_risk', '=', 'country_risk_models')]", required=False)
    lender_risk_model_id = fields.Many2one('risk.models', string='Lender Risk',
                                           domain="[('type_risk', '=', 'lender_risk_models')]", required=False)
    borrower_risk_model_id = fields.Many2one('risk.models', string='Borrower Risk',
                                             domain="[('type_risk', '=', 'borrower_risk_models')]", required=False)
    transaction_risk_model_id = fields.Many2one('risk.models', string='Transaction Risk',
                                                domain="[('type_risk', '=', 'transaction_risk_models')]",
                                                required=False)

    # type_risk = fields.Char(string='Type ', related='country_risk_model_id.type_risk')

    # country_risk_models_factors = fields.Many2one('risk.model.factor', string='Country Risk', required=False)
    # lender_risk_models_factors = fields.Many2one('risk.model.factor', string='Lender Risk', required=False)
    # borrower_risk_models_factors = fields.Many2one('risk.model.factor', string='Borrower Risk', required=False)
    # transaction_risk_models_factors = fields.Many2one('risk.model.factor', string='Transaction Risk', required=False)

    risk_models_simulation_models_model_factor_ids = fields.One2many('risk.models.simulation.models.model.factor',
                                                                     'risk_models_simulation_id', required=False
                                                                     )
    risk_models_simulation_models_model_sub_factor_ids = fields.One2many(
        'risk.models.simulation.models.model.sub.factor', 'risk_models_simulation_id', required=False)

    lender_risk_models_simulation_models_model_factor_ids = fields.One2many(
        'risk.models.simulation.models.model.factor.lender',
        'risk_models_simulation_id', required=False,
        )
    lender_risk_models_simulation_models_model_sub_factor_ids = fields.One2many(
        'risk.models.simulation.models.model.sub.factor.lender', 'risk_models_simulation_id', required=False)

    borrower_risk_models_simulation_models_model_factor_ids = fields.One2many(
        'risk.models.simulation.models.model.factor.borrower',
        'risk_models_simulation_id', required=False,
    )
    borrower_risk_models_simulation_models_model_sub_factor_ids = fields.One2many(
        'risk.models.simulation.models.model.sub.factor.borrower', 'risk_models_simulation_id', required=False)

    transaction_risk_models_simulation_models_model_factor_ids = fields.One2many(
        'risk.models.simulation.models.model.factor.transact',
        'risk_models_simulation_id', required=False,
    )
    transaction_risk_models_simulation_models_model_sub_factor_ids = fields.One2many(
        'risk.models.simulation.models.model.sub.factor.transact', 'risk_models_simulation_id', required=False)

    weighted_score_total = fields.Float(compute='_compute_weighted_score_total')
    weighted_score_total_lender = fields.Float(compute='_compute_weighted_score_total_lender')
    weighted_score_total_borrower = fields.Float(compute='_compute_weighted_score_total_borrower')
    weighted_score_total_transaction = fields.Float(compute='_compute_weighted_score_total_transaction')

    @api.depends('country_risk_model_id')
    def _compute_weighted_score_total(self):
        total = sum(item.weighted_score for item in self.risk_models_simulation_models_model_factor_ids)
        self.weighted_score_total = total

    @api.depends('lender_risk_model_id')
    def _compute_weighted_score_total_lender(self):
        total = sum(item.weighted_score for item in self.lender_risk_models_simulation_models_model_factor_ids)
        self.weighted_score_total_lender = total

    @api.depends('borrower_risk_model_id')
    def _compute_weighted_score_total_borrower(self):
        total = sum(item.weighted_score for item in self.borrower_risk_models_simulation_models_model_factor_ids)
        self.weighted_score_total_borrower = total

    @api.depends('transaction_risk_model_id')
    def _compute_weighted_score_total_transaction(self):
        total = sum(item.weighted_score for item in self.transaction_risk_models_simulation_models_model_factor_ids)
        self.weighted_score_total_transaction = total

    def init_risk_score_and_weighted_score(self, risk_models_simulation_models_model_factor_value, populated):
        total = sum(item[2]['score'] for item in populated)
        risk_models_simulation_models_model_factor_value["risk_score"] = total
        risk_models_simulation_models_model_factor_value["weighted_score"] = total * \
                                                                             risk_models_simulation_models_model_factor_value[
                                                                                 "factor_weight"] / 100

    def init_risk_score_and_weighted_score_write(self, risk_models_simulation_models_model_factor_value, populated):

        total = sum( item[2]['score'] for item in populated)

        risk_models_simulation_models_model_factor_value.risk_score = total
        risk_models_simulation_models_model_factor_value.weighted_score= total * \
                                                                             risk_models_simulation_models_model_factor_value.factor_weight / 100

    # def init_risk_score_and_weighted_score_write(self, risk_models_simulation_models_model_factor_value, populated):
    #     print(populated)
    #     total = sum(item[2]['score'] for item in populated)
    #     print(total)
    #     risk_models_simulation_models_model_factor_value["risk_score"] = total
    #     risk_models_simulation_models_model_factor_value["weighted_score"] = total * \
    #                                                                          risk_models_simulation_models_model_factor_value[
    #                                                                              "factor_weight"] / 100

    @api.model
    def create(self, vals):

        '''This action is used to create Simulation transaction in the database.'''

        if "risk_models_simulation_models_model_factor_ids" in vals.keys():
            risk_models_simulation_models_model_factor_ids = vals['risk_models_simulation_models_model_factor_ids']
            for risk_models_simulation_models_model_factor_id in risk_models_simulation_models_model_factor_ids:
                risk_models_simulation_models_model_factor_value = risk_models_simulation_models_model_factor_id[2]
                if "risk_models_simulation_models_model_sub_factor_ids" in vals.keys():
                    risk_models_simulation_models_model_sub_factor_ids = vals[
                        'risk_models_simulation_models_model_sub_factor_ids']
                    populated = list(filter(
                        lambda c: c[2]["risk_model_factor_id"] == risk_models_simulation_models_model_factor_value[
                            'risk_model_factor_id'], risk_models_simulation_models_model_sub_factor_ids))
                    self.init_risk_score_and_weighted_score(risk_models_simulation_models_model_factor_value, populated)

        if "lender_risk_models_simulation_models_model_factor_ids" in vals.keys():
            risk_models_simulation_models_model_factor_ids = vals[
                'lender_risk_models_simulation_models_model_factor_ids']
            for risk_models_simulation_models_model_factor_id in risk_models_simulation_models_model_factor_ids:
                risk_models_simulation_models_model_factor_value = risk_models_simulation_models_model_factor_id[2]
                if "lender_risk_models_simulation_models_model_sub_factor_ids" in vals.keys():
                    risk_models_simulation_models_model_sub_factor_ids = vals[
                        'lender_risk_models_simulation_models_model_sub_factor_ids']
                    populated = list(filter(
                        lambda c: c[2]["risk_model_factor_id"] == risk_models_simulation_models_model_factor_value[
                            'risk_model_factor_id'], risk_models_simulation_models_model_sub_factor_ids))
                    self.init_risk_score_and_weighted_score(risk_models_simulation_models_model_factor_value, populated)

        if "borrower_risk_models_simulation_models_model_factor_ids" in vals.keys():
            risk_models_simulation_models_model_factor_ids = vals[
                'borrower_risk_models_simulation_models_model_factor_ids']
            for risk_models_simulation_models_model_factor_id in risk_models_simulation_models_model_factor_ids:
                risk_models_simulation_models_model_factor_value = risk_models_simulation_models_model_factor_id[2]
                if "borrower_risk_models_simulation_models_model_sub_factor_ids" in vals.keys():
                    risk_models_simulation_models_model_sub_factor_ids = vals[
                        'borrower_risk_models_simulation_models_model_sub_factor_ids']
                    populated = list(filter(
                        lambda c: c[2]["risk_model_factor_id"] == risk_models_simulation_models_model_factor_value[
                            'risk_model_factor_id'], risk_models_simulation_models_model_sub_factor_ids))
                    self.init_risk_score_and_weighted_score(risk_models_simulation_models_model_factor_value, populated)

        if "transaction_risk_models_simulation_models_model_factor_ids" in vals.keys():
            risk_models_simulation_models_model_factor_ids = vals[
                'transaction_risk_models_simulation_models_model_factor_ids']
            for risk_models_simulation_models_model_factor_id in risk_models_simulation_models_model_factor_ids:
                risk_models_simulation_models_model_factor_value = risk_models_simulation_models_model_factor_id[2]
                if "transaction_risk_models_simulation_models_model_sub_factor_ids" in vals.keys():
                    risk_models_simulation_models_model_sub_factor_ids = vals[
                        'transaction_risk_models_simulation_models_model_sub_factor_ids']
                    populated = list(filter(
                        lambda c: c[2]["risk_model_factor_id"] == risk_models_simulation_models_model_factor_value[
                            'risk_model_factor_id'], risk_models_simulation_models_model_sub_factor_ids))
                    self.init_risk_score_and_weighted_score(risk_models_simulation_models_model_factor_value, populated)

        riskModelsSimulation = super(RiskModelsSimulation, self).create(vals)
        return riskModelsSimulation

    def init_risk_model_factor_id_key(self, risk_models_simulation_models_model_sub_factor_ids, subfactor_model):
        for risk_models_simulation_models_model_sub_factor_id in risk_models_simulation_models_model_sub_factor_ids :
            result = self.env[subfactor_model].browse(risk_models_simulation_models_model_sub_factor_id[1])
            if not risk_models_simulation_models_model_sub_factor_id[2] :
                risk_models_simulation_models_model_sub_factor_id[2] = {}

            risk_models_simulation_models_model_sub_factor_id[2]["risk_model_factor_id"] = result.risk_model_factor_id.id
            if not "score" in risk_models_simulation_models_model_sub_factor_id[2].keys() :
                risk_models_simulation_models_model_sub_factor_id[2]["score"] = result.answer.point



    def write(self, vals):
        '''This action is used to update Simulation transaction in the database.'''

        if self.risk_models_simulation_models_model_factor_ids:
             for risk_models_simulation_models_model_factor_id in self.risk_models_simulation_models_model_factor_ids:
                risk_models_simulation_models_model_factor_value = risk_models_simulation_models_model_factor_id
                if "risk_models_simulation_models_model_sub_factor_ids" in vals.keys():
                    risk_models_simulation_models_model_sub_factor_ids = vals[
                        'risk_models_simulation_models_model_sub_factor_ids']
                    self.init_risk_model_factor_id_key(risk_models_simulation_models_model_sub_factor_ids, 'risk.models.simulation.models.model.sub.factor')
                    populated = list(filter(
                        lambda c: c[2] and (c[2]["risk_model_factor_id"] == risk_models_simulation_models_model_factor_value.risk_model_factor_id.id),
                        risk_models_simulation_models_model_sub_factor_ids))
                    self.init_risk_score_and_weighted_score_write(risk_models_simulation_models_model_factor_value, populated)

        if self.lender_risk_models_simulation_models_model_factor_ids:
            for risk_models_simulation_models_model_factor_id in self.lender_risk_models_simulation_models_model_factor_ids:
                risk_models_simulation_models_model_factor_value = risk_models_simulation_models_model_factor_id
                if "lender_risk_models_simulation_models_model_sub_factor_ids" in vals.keys():
                    risk_models_simulation_models_model_sub_factor_ids = vals[
                        'lender_risk_models_simulation_models_model_sub_factor_ids']
                    self.init_risk_model_factor_id_key(risk_models_simulation_models_model_sub_factor_ids,
                                                       'risk.models.simulation.models.model.sub.factor.lender')
                    populated = list(filter(
                        lambda c: c[2] and (c[2][
                                                "risk_model_factor_id"] == risk_models_simulation_models_model_factor_value.risk_model_factor_id.id),
                        risk_models_simulation_models_model_sub_factor_ids))
                    self.init_risk_score_and_weighted_score_write(risk_models_simulation_models_model_factor_value,
                                                                  populated)

        if self.borrower_risk_models_simulation_models_model_factor_ids:
            for risk_models_simulation_models_model_factor_id in self.borrower_risk_models_simulation_models_model_factor_ids:
                risk_models_simulation_models_model_factor_value = risk_models_simulation_models_model_factor_id
                if "borrower_risk_models_simulation_models_model_sub_factor_ids" in vals.keys():
                    risk_models_simulation_models_model_sub_factor_ids = vals[
                        'borrower_risk_models_simulation_models_model_sub_factor_ids']
                    self.init_risk_model_factor_id_key(risk_models_simulation_models_model_sub_factor_ids,
                                                       'risk.models.simulation.models.model.sub.factor.borrower')
                    populated = list(filter(
                        lambda c: c[2] and (c[2][
                                                "risk_model_factor_id"] == risk_models_simulation_models_model_factor_value.risk_model_factor_id.id),
                        risk_models_simulation_models_model_sub_factor_ids))
                    self.init_risk_score_and_weighted_score_write(risk_models_simulation_models_model_factor_value,
                                                                  populated)

        if self.transaction_risk_models_simulation_models_model_factor_ids:
            for risk_models_simulation_models_model_factor_id in self.transaction_risk_models_simulation_models_model_factor_ids:
                risk_models_simulation_models_model_factor_value = risk_models_simulation_models_model_factor_id
                if "transaction_risk_models_simulation_models_model_sub_factor_ids" in vals.keys():
                    risk_models_simulation_models_model_sub_factor_ids = vals[
                        'transaction_risk_models_simulation_models_model_sub_factor_ids']
                    self.init_risk_model_factor_id_key(risk_models_simulation_models_model_sub_factor_ids,
                                                       'risk.models.simulation.models.model.sub.factor.transact')
                    populated = list(filter(
                        lambda c: c[2] and (c[2][
                                                "risk_model_factor_id"] == risk_models_simulation_models_model_factor_value.risk_model_factor_id.id),
                        risk_models_simulation_models_model_sub_factor_ids))
                    self.init_risk_score_and_weighted_score_write(risk_models_simulation_models_model_factor_value,
                                                                  populated)

        riskModelsSimulation = super(RiskModelsSimulation, self).write(vals)
        return riskModelsSimulation

    def init_risk_models_simulation_data(self, risk_models_id):

        ligne_risk_models_simulation_models_model_factor_ids = []
        ligne_risk_models_simulation_models_model_sub_factor_ids = []

        for rec in self:
            rec.write({'risk_models_simulation_models_model_factor_ids': [(5, 0, 0)]})
            rec.write({'risk_models_simulation_models_model_sub_factor_ids': [(5, 0, 0)]})

        if risk_models_id:

            risk_model_factor = self.env['risk.model.factor']
            risk_model_sub_factor = self.env['risk.model.sub.factor']

            risk_model_factor_results = risk_model_factor.search([('risk_model_id', '=', risk_models_id)])
            for rec in risk_model_factor_results:
                if rec:
                    factor_name = rec.factor_name
                    factor_id = rec.id
                    value = {
                        'risk_model_factor_id': rec.id,
                        'factor_name': rec.factor_name,
                        'risk_score': 0,
                        'factor_weight': rec.Weight,
                        'weighted_score': 0,
                    }

                ligne_risk_models_simulation_models_model_factor_ids.append((0, 0, value))
                risk_model_sub_factor_results = risk_model_sub_factor.search([('risk_model_factor_id', '=', rec.id)])
                for rec in risk_model_sub_factor_results:
                    if rec:
                        value = {

                            'risk_model_factor_id': factor_id,
                            # 'factor_name': factor_name,
                            # 'sub_factor_name':rec.subfactor_name,
                            'risk_model_sub_factor_id': rec.id,
                            'sub_factor_weight': rec.weight,
                            'answer': False,
                            'score': 0,
                        }
                    ligne_risk_models_simulation_models_model_sub_factor_ids.append((0, 0, value))
        return {'value': {
            'risk_models_simulation_models_model_factor_ids': ligne_risk_models_simulation_models_model_factor_ids,
            'risk_models_simulation_models_model_sub_factor_ids': ligne_risk_models_simulation_models_model_sub_factor_ids}}

    def init_param_risk_models_simulation_data(self, risk_models_id, risk_models_simulation_models_model_factor_ids,
                                               risk_models_simulation_models_model_sub_factor_ids):

        ligne_risk_models_simulation_models_model_factor_ids = []
        ligne_risk_models_simulation_models_model_sub_factor_ids = []

        for rec in self:
            rec.write({risk_models_simulation_models_model_factor_ids: [(5, 0, 0)]})
            rec.write({risk_models_simulation_models_model_sub_factor_ids: [(5, 0, 0)]})

        if risk_models_id:

            risk_model_factor = self.env['risk.model.factor']
            risk_model_sub_factor = self.env['risk.model.sub.factor']

            risk_model_factor_results = risk_model_factor.search([('risk_model_id', '=', risk_models_id)])
            for rec in risk_model_factor_results:
                if rec:
                    factor_name = rec.factor_name
                    factor_id = rec.id
                    value = {
                        'risk_model_factor_id': rec.id,
                        'factor_name': rec.factor_name,
                        'risk_score': 0,
                        'factor_weight': rec.Weight,
                        'weighted_score': 0,

                    }

                ligne_risk_models_simulation_models_model_factor_ids.append((0, 0, value))
                risk_model_sub_factor_results = risk_model_sub_factor.search([('risk_model_factor_id', '=', rec.id)])
                for rec in risk_model_sub_factor_results:
                    if rec:
                        value = {

                            'risk_model_factor_id': factor_id,
                            # 'factor_name': factor_name,
                            # 'sub_factor_name':rec.subfactor_name,
                            'risk_model_sub_factor_id': rec.id,
                            'sub_factor_weight': rec.weight,
                            'answer': False,
                            'score': 0,
                        }
                    ligne_risk_models_simulation_models_model_sub_factor_ids.append((0, 0, value))
        return {'value': {
            risk_models_simulation_models_model_factor_ids: ligne_risk_models_simulation_models_model_factor_ids,
            risk_models_simulation_models_model_sub_factor_ids: ligne_risk_models_simulation_models_model_sub_factor_ids}}

    @api.onchange('country_risk_model_id')
    def _onchange_country_risk_model_id(self):
        if self.country_risk_model_id:
            return self.init_risk_models_simulation_data(self.country_risk_model_id.id)

    @api.onchange('lender_risk_model_id')
    def _onchange_lender_risk_model_id(self):
        if self.lender_risk_model_id:
            return self.init_param_risk_models_simulation_data(self.lender_risk_model_id.id,
                                                               'lender_risk_models_simulation_models_model_factor_ids',
                                                               'lender_risk_models_simulation_models_model_sub_factor_ids')
            # return self.init_risk_models_simulation_data(self.lender_risk_model_id.id)

    @api.onchange('borrower_risk_model_id')
    def _onchange_borrower_risk_model_id(self):
        if self.borrower_risk_model_id:
            return self.init_param_risk_models_simulation_data(self.borrower_risk_model_id.id,
                                                               'borrower_risk_models_simulation_models_model_factor_ids',
                                                               'borrower_risk_models_simulation_models_model_sub_factor_ids')
            # return self.init_risk_models_simulation_data(self.lender_risk_model_id.id)

    @api.onchange('transaction_risk_model_id')
    def _onchange_transaction_risk_model_id(self):
        if self.transaction_risk_model_id:
            return self.init_param_risk_models_simulation_data(self.transaction_risk_model_id.id,
                                                               'transaction_risk_models_simulation_models_model_factor_ids',
                                                               'transaction_risk_models_simulation_models_model_sub_factor_ids')
            # return self.init_risk_models_simulation_data(self.lender_risk_model_id.id)

    def init_multiple_risk_models_simulation_data(self, risk_models_ids):

        ligne_risk_models_simulation_models_model_factor_ids = []
        ligne_risk_models_simulation_models_model_sub_factor_ids = []

        for rec in self:
            rec.write({'risk_models_simulation_models_model_factor_ids': [(5, 0, 0)]})
            rec.write({'risk_models_simulation_models_model_sub_factor_ids': [(5, 0, 0)]})

        if risk_models_ids:

            risk_model_factor = self.env['risk.model.factor']
            risk_model_sub_factor = self.env['risk.model.sub.factor']

            risk_model_factor_results = risk_model_factor.search([('risk_model_id', 'in', risk_models_ids)])
            for rec in risk_model_factor_results:
                if rec:
                    factor_name = rec.factor_name
                    factor_id = rec.id
                    value = {
                        'risk_model_factor_id': rec.id,
                        'factor_name': rec.factor_name,
                        'risk_score': 0,
                        'factor_weight': rec.Weight,
                        'weighted_score': 0,
                    }

                ligne_risk_models_simulation_models_model_factor_ids.append((0, 0, value))
                risk_model_sub_factor_results = risk_model_sub_factor.search(
                    [('risk_model_factor_id', '=', rec.id)])
                for rec in risk_model_sub_factor_results:
                    if rec:
                        value = {

                            'risk_model_factor_id': factor_id,
                            # 'factor_name': factor_name,
                            # 'sub_factor_name':rec.subfactor_name,
                            'risk_model_sub_factor_id': rec.id,
                            'sub_factor_weight': rec.weight,
                            'answer': False,
                            'score': 0,
                        }
                    ligne_risk_models_simulation_models_model_sub_factor_ids.append((0, 0, value))
        return {'value': {
            'risk_models_simulation_models_model_factor_ids': ligne_risk_models_simulation_models_model_factor_ids,
            'risk_models_simulation_models_model_sub_factor_ids': ligne_risk_models_simulation_models_model_sub_factor_ids}}

    @api.onchange('risk_model_ids')
    def _onchange_risk_model_ids(self):
        if self.risk_model_ids.ids:
            return self.init_multiple_risk_models_simulation_data(self.risk_model_ids.ids)

    @api.onchange('risk_model_country_ids')
    def _onchange_risk_model_country_ids(self):
        if self.risk_model_country_ids.ids:
            return self.init_multiple_risk_models_simulation_data(self.risk_model_country_ids.ids)

    @api.onchange('risk_model_lender_ids')
    def _onchange_risk_model_lender_ids(self):
        if self.risk_model_lender_ids.ids:
            return self.init_multiple_risk_models_simulation_data(self.risk_model_lender_ids.ids)


class RiskModelsSimulationModelsModelFactor(models.Model):
    _name = 'risk.models.simulation.models.model.factor'
    _description = 'This applies to country risk, borrower risk, lender risk and transaction risk'

    risk_models_simulation_id = fields.Many2one('risk.models.simulation', string='Simulation', required=False)
    risk_models_id = fields.Many2one('risk.models', string='Simulation Models', required=False)
    risk_model_factor_id = fields.Many2one('risk.model.factor', string='Simulation Factor', required=False)
    factor_name = fields.Char(string='Component', related='risk_model_factor_id.factor_name', Store=True)
    factor_weight = fields.Float(string='Weight', Store=True)
    risk_score = fields.Float(string='Risk Score', required=False)
    # weighted_score = fields.Float(string='Weighted Score', required=False,  compute="_compute_weighted_score")
    weighted_score = fields.Float(string='Weighted Score', required=False)
    #weighted_score_total = fields.Float(string='Weighted Score', required=False)

    # @api.depends('weighted_score', 'risk_models_simulation_id.country_risk_model_id')
    # def _compute_weighted_score_total(self):
    #     total = sum(item.weighted_score for item in self)
    #     self.weighted_score_total = total


    # @api.depends('risk_score')
    # def _compute_weighted_score(self):
    #    print("bonjour")



class RiskModelsSimulationModelsModelSubFactor(models.Model):
    _name = 'risk.models.simulation.models.model.sub.factor'
    _description = 'This applies to country risk, borrower risk, lender risk and transaction risk'

    risk_models_simulation_id = fields.Many2one('risk.models.simulation', string='Simulation', required=False)
    risk_models_id = fields.Many2one('risk.models', string='Simulation Models', required=False)
    risk_model_sub_factor_id = fields.Many2one('risk.model.sub.factor', string='Simulation sub factor', required=False)
    risk_model_factor_id = fields.Many2one('risk.model.factor', string='Simulation  factor', required=False)
    # factor_name = fields.Char(string='Factor name', related='risk_model_sub_factor_id.risk_model_factor_id.factor_name', Store=False)
    sub_factor_name = fields.Char(string='Sub factor name', related='risk_model_sub_factor_id.subfactor_name',
                                  Store=True)
    sub_factor_weight = fields.Float(string='Sub factor weight', related='risk_model_sub_factor_id.weight', Store=True)
    # answer = fields.Char(string='Answer', required=False)
    answer = fields.Many2one('risk.model.sub.factor.answers', string='Answer', required=False,
                             domain="[('risk_model_subfactor_id', '=', risk_model_sub_factor_id)]")
    score = fields.Float(string='Score', required=False, compute='_compute_score', inverse='_inverse_score', Store=True)

    # score = fields.Float(string='Score', required=False, related='answer.point', inverse='_inverse_score', Store=True)
    # inverse_score = fields.Float(string='Score', required=False)

    @api.depends('answer')
    def _compute_score(self):
        for rec in self:
            if rec.answer.point:
                rec.score = rec.answer.point

    def _inverse_score(self):
        pass
        # print('---------Computing Margin----------')
        # for rec in self:
        #     rec.inverse_score = rec.score


# ----------------------------------------MANAGE OF LENDER RISK-------------------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class RiskModelsSimulationModelsModelFactorLender(models.Model):
    _name = 'risk.models.simulation.models.model.factor.lender'
    _description = 'This applies to country risk, borrower risk, lender risk and transaction risk'

    risk_models_simulation_id = fields.Many2one('risk.models.simulation', string='Simulation', required=False)
    risk_models_id = fields.Many2one('risk.models', string='Simulation Models', required=False)
    risk_model_factor_id = fields.Many2one('risk.model.factor', string='Simulation Factor', required=False)
    factor_name = fields.Char(string='Component', related='risk_model_factor_id.factor_name', Store=True)
    factor_weight = fields.Float(string='Weight', Store=True)
    risk_score = fields.Float(string='Risk Score', required=False)
    # weighted_score = fields.Float(string='Weighted Score', required=False,  compute="_compute_weighted_score")
    weighted_score = fields.Float(string='Weighted Score', required=False)

    # @api.depends('risk_score')
    # def _compute_weighted_score(self):
    #    print("bonjour")


class RiskModelsSimulationModelsModelSubFactorLender(models.Model):
    _name = 'risk.models.simulation.models.model.sub.factor.lender'
    _description = 'This applies to country risk, borrower risk, lender risk and transaction risk'

    risk_models_simulation_id = fields.Many2one('risk.models.simulation', string='Simulation', required=False)
    risk_models_id = fields.Many2one('risk.models', string='Simulation Models', required=False)
    risk_model_sub_factor_id = fields.Many2one('risk.model.sub.factor', string='Simulation sub factor', required=False)
    risk_model_factor_id = fields.Many2one('risk.model.factor', string='Simulation  factor', required=False)
    # factor_name = fields.Char(string='Factor name', related='risk_model_sub_factor_id.risk_model_factor_id.factor_name', Store=False)
    sub_factor_name = fields.Char(string='Sub factor name', related='risk_model_sub_factor_id.subfactor_name',
                                  Store=True)
    sub_factor_weight = fields.Float(string='Sub factor weight', related='risk_model_sub_factor_id.weight', Store=True)
    # answer = fields.Char(string='Answer', required=False)
    answer = fields.Many2one('risk.model.sub.factor.answers', string='Answer', required=False,
                             domain="[('risk_model_subfactor_id', '=', risk_model_sub_factor_id)]")
    score = fields.Float(string='Score', required=False, compute='_compute_score', inverse='_inverse_score', Store=True)

    # score = fields.Float(string='Score', required=False, related='answer.point', inverse='_inverse_score', Store=True)
    # inverse_score = fields.Float(string='Score', required=False)

    @api.depends('answer')
    def _compute_score(self):
        for rec in self:
            if rec.answer.point:
                rec.score = rec.answer.point

    def _inverse_score(self):
        pass
        # print('---------Computing Margin----------')
        # for rec in self:
        #     rec.inverse_score = rec.score


# ----------------------------------------MANAGE OF BORROWER RISK-------------------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class RiskModelsSimulationModelsModelFactorBorrower(models.Model):
    _name = 'risk.models.simulation.models.model.factor.borrower'
    _description = 'This applies to country risk, borrower risk, lender risk and transaction risk'

    risk_models_simulation_id = fields.Many2one('risk.models.simulation', string='Simulation', required=False)
    risk_models_id = fields.Many2one('risk.models', string='Simulation Models', required=False)
    risk_model_factor_id = fields.Many2one('risk.model.factor', string='Simulation Factor', required=False)
    factor_name = fields.Char(string='Component', related='risk_model_factor_id.factor_name', Store=True)
    factor_weight = fields.Float(string='Weight', Store=True)
    risk_score = fields.Float(string='Risk Score', required=False)
    # weighted_score = fields.Float(string='Weighted Score', required=False,  compute="_compute_weighted_score")
    weighted_score = fields.Float(string='Weighted Score', required=False)

    # @api.depends('risk_score')
    # def _compute_weighted_score(self):
    #    print("bonjour")


class RiskModelsSimulationModelsModelSubFactorBorrower(models.Model):
    _name = 'risk.models.simulation.models.model.sub.factor.borrower'
    _description = 'This applies to country risk, borrower risk, lender risk and transaction risk'

    risk_models_simulation_id = fields.Many2one('risk.models.simulation', string='Simulation', required=False)
    risk_models_id = fields.Many2one('risk.models', string='Simulation Models', required=False)
    risk_model_sub_factor_id = fields.Many2one('risk.model.sub.factor', string='Simulation sub factor', required=False)
    risk_model_factor_id = fields.Many2one('risk.model.factor', string='Simulation  factor', required=False)
    # factor_name = fields.Char(string='Factor name', related='risk_model_sub_factor_id.risk_model_factor_id.factor_name', Store=False)
    sub_factor_name = fields.Char(string='Sub factor name', related='risk_model_sub_factor_id.subfactor_name',
                                  Store=True)
    sub_factor_weight = fields.Float(string='Sub factor weight', related='risk_model_sub_factor_id.weight', Store=True)
    # answer = fields.Char(string='Answer', required=False)
    answer = fields.Many2one('risk.model.sub.factor.answers', string='Answer', required=False,
                             domain="[('risk_model_subfactor_id', '=', risk_model_sub_factor_id)]")
    score = fields.Float(string='Score', required=False, compute='_compute_score', inverse='_inverse_score', Store=True)

    # score = fields.Float(string='Score', required=False, related='answer.point', inverse='_inverse_score', Store=True)
    # inverse_score = fields.Float(string='Score', required=False)

    @api.depends('answer')
    def _compute_score(self):
        for rec in self:
            if rec.answer.point:
                rec.score = rec.answer.point

    def _inverse_score(self):
        pass
        # print('---------Computing Margin----------')
        # for rec in self:
        #     rec.inverse_score = rec.score


# ----------------------------------------MANAGE OF TRANSACTION RISK-------------------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class RiskModelsSimulationModelsModelFactorTransact(models.Model):
    _name = 'risk.models.simulation.models.model.factor.transact'
    _description = 'This applies to country risk, borrower risk, lender risk and transaction risk'

    risk_models_simulation_id = fields.Many2one('risk.models.simulation', string='Simulation', required=False)
    risk_models_id = fields.Many2one('risk.models', string='Simulation Models', required=False)
    risk_model_factor_id = fields.Many2one('risk.model.factor', string='Simulation Factor', required=False)
    factor_name = fields.Char(string='Component', related='risk_model_factor_id.factor_name', Store=True)
    factor_weight = fields.Float(string='Weight', Store=True)
    risk_score = fields.Float(string='Risk Score', required=False)
    # weighted_score = fields.Float(string='Weighted Score', required=False,  compute="_compute_weighted_score")
    weighted_score = fields.Float(string='Weighted Score', required=False)

    # @api.depends('risk_score')
    # def _compute_weighted_score(self):
    #    print("bonjour")


class RiskModelsSimulationModelsModelSubFactorTransact(models.Model):
    _name = 'risk.models.simulation.models.model.sub.factor.transact'
    _description = 'This applies to country risk, borrower risk, lender risk and transaction risk'

    risk_models_simulation_id = fields.Many2one('risk.models.simulation', string='Simulation', required=False)
    risk_models_id = fields.Many2one('risk.models', string='Simulation Models', required=False)
    risk_model_sub_factor_id = fields.Many2one('risk.model.sub.factor', string='Simulation sub factor', required=False)
    risk_model_factor_id = fields.Many2one('risk.model.factor', string='Simulation  factor', required=False)
    # factor_name = fields.Char(string='Factor name', related='risk_model_sub_factor_id.risk_model_factor_id.factor_name', Store=False)
    sub_factor_name = fields.Char(string='Sub factor name', related='risk_model_sub_factor_id.subfactor_name',
                                  Store=True)
    sub_factor_weight = fields.Float(string='Sub factor weight', related='risk_model_sub_factor_id.weight', Store=True)
    # answer = fields.Char(string='Answer', required=False)
    answer = fields.Many2one('risk.model.sub.factor.answers', string='Answer', required=False,
                             domain="[('risk_model_subfactor_id', '=', risk_model_sub_factor_id)]")
    score = fields.Float(string='Score', required=False, compute='_compute_score', inverse='_inverse_score', Store=True)

    # score = fields.Float(string='Score', required=False, related='answer.point', inverse='_inverse_score', Store=True)
    # inverse_score = fields.Float(string='Score', required=False)

    @api.depends('answer')
    def _compute_score(self):
        for rec in self:
            if rec.answer.point:
                rec.score = rec.answer.point

    def _inverse_score(self):
        pass
        # print('---------Computing Margin----------')
        # for rec in self:
        #     rec.inverse_score = rec.score
