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
    _order = 'id desc'

    def _default_model_simulation_name(self):
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        default_model_simulation_name = 'Simulation-' + str(self._uid) + '-' + date_time
        return default_model_simulation_name

    model_simulation_name = fields.Char(string='Model Simulation Name', required=True,
                                        default=_default_model_simulation_name)
    model_simulation_description = fields.Text(string='Model Simulation Description', required=False)
    status = fields.Selection([('1', 'Draft'), ('2', 'Validate')], required=True, default='1', readonly=True)

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

    weighted_score_total = fields.Float(compute='_compute_weighted_score_total', string='Country Risk ',
                                        inverse='_inverse_weighted_score_total')
    weighted_score_total_lender = fields.Float(compute='_compute_weighted_score_total_lender', string='Lender Risk ',
                                               inverse='_inverse_weighted_score_total_lender')
    weighted_score_total_borrower = fields.Float(compute='_compute_weighted_score_total_borrower',
                                                 string='Borrower Risk ',
                                                 inverse='_inverse_weighted_score_total_borrower')
    weighted_score_total_transaction = fields.Float(compute='_compute_weighted_score_total_transaction',
                                                    string='Transaction Risk ',
                                                    inverse='_inverse_weighted_score_total_transaction')

    product_id = fields.Many2one('risk.warf.weight.matrices', string='Product ', required=False)

    weighted_product = fields.Float(compute='_compute_weighted_product',
                                    inverse='_inverse_weighted_product')
    weighted_product_lender = fields.Float(compute='_compute_weighted_product',
                                           inverse='_inverse_weighted_product')
    weighted_product_borrower = fields.Float(compute='_compute_weighted_product',
                                             inverse='_inverse_weighted_product')
    weighted_product_transaction = fields.Float(compute='_compute_weighted_product',
                                                inverse='_inverse_weighted_product')

    sum_weighted_product = fields.Float(compute='_compute_sum_weighted_product',
                                        inverse='_inverse_sum_weighted_product')

    @api.depends('product_id')
    def _compute_weighted_product(self):
        for rec in self:
            if rec.product_id:
                rec.weighted_product = rec.product_id.country_weight
                rec.weighted_product_lender = rec.product_id.lender_weight
                rec.weighted_product_borrower = rec.product_id.borrower_weight
                rec.weighted_product_transaction = rec.product_id.transaction_weight

    def _inverse_weighted_product(self):
        pass

    @api.depends('product_id')
    def _compute_sum_weighted_product(self):
        for rec in self:
            if rec.product_id:
                rec.sum_weighted_product = rec.weighted_product + rec.weighted_product_lender + rec.weighted_product_borrower + rec.weighted_product_transaction

    def _inverse_sum_weighted_product(self):
        pass

    weighted_product_score = fields.Float(compute='_compute_weighted_product_score',
                                          inverse='_inverse_weighted_product_score')
    weighted_product_score_lender = fields.Float(compute='_compute_weighted_product_score',
                                                 inverse='_inverse_weighted_product_score')
    weighted_product_score_borrower = fields.Float(compute='_compute_weighted_product_score',
                                                   inverse='_inverse_weighted_product_score')
    weighted_product_score_transaction = fields.Float(compute='_compute_weighted_product_score',
                                                      inverse='_inverse_weighted_product_score')

    sum_weighted_product_score = fields.Float(compute='_compute_sum_weighted_product_score',
                                              inverse='_inverse_sum_weighted_product_score')

    @api.depends('product_id')
    def _compute_weighted_product_score(self):
        for rec in self:
            if rec.product_id:
                if rec.weighted_score_total: rec.weighted_product_score = rec.product_id.country_weight * rec.weighted_score_total / 100
                if rec.weighted_score_total_lender: rec.weighted_product_score_lender = rec.product_id.lender_weight * rec.weighted_score_total_lender / 100
                if rec.weighted_score_total_borrower: rec.weighted_product_score_borrower = rec.product_id.borrower_weight * rec.weighted_score_total_borrower / 100
                if rec.weighted_score_total_transaction:   rec.weighted_product_score_transaction = rec.product_id.transaction_weight * rec.weighted_score_total_transaction / 100

    def _inverse_weighted_product_score(self):
        pass

    @api.depends('product_id')
    def _compute_sum_weighted_product_score(self):
        for rec in self:
            if rec.product_id:
                rec.sum_weighted_product_score = rec.weighted_product_score + rec.weighted_product_score_lender + rec.weighted_product_score_borrower + rec.weighted_product_score_transaction

    def _inverse_sum_weighted_product_score(self):
        pass

    period_id = fields.Many2one('risk.premium.f.curves', string='Period(Tenor)', required=False)

    @api.onchange('period_id', 'facility_amount', 'sum_weighted_product_score', 'conversion_factor_default_rate',
                  'coverage_ratio', 'recovery_rate', 'period_after_default_for_recovery', 'premium_d', 'premium_f',
                  'weighted_score_total', 'weighted_score_total_lender', 'weighted_score_total_borrower',
                  'weighted_score_total_transaction')
    def _onchange_period_id(self):

        '''This event is used to compute the amortization table when any of each field next the @api.change annotation change'''


        if self.period_id:
            return self.init_risk_models_armotization_schedule_data(self.period_id.period, self.facility_amount,
                                                                    self.sum_weighted_product_score,
                                                                    self.conversion_factor_default_rate,
                                                                    self.coverage_ratio, self.recovery_rate,
                                                                    self.period_after_default_for_recovery,
                                                                    self.premium_d, self.premium_f)

    def init_risk_models_armotization_schedule_data(self, period, facility_amount, sum_weighted_product_score,
                                                    conversion_factor_default_rate, coverage_ratio, recovery_rate,
                                                    period_after_default_for_recovery, premium_d, premium_f):
        '''This action is for initialisation of amortization schedule data. this action is called by _on_change_period_id event'''

        ligne_risk_models_amortization_schedule_ids = []

        for rec in self:
            rec.write({'risk_models_amortization_schedule_ids': [(5, 0, 0)], 'drapeau': True})

        if period:

            tenor = period

            principal_amount = 0
            principal_repayment = 0
            agency_default_rate_per_each_period = 0
            expected_default = 0
            previous_principal_amount = 0
            period_t = 1
            period_Tr = period_after_default_for_recovery
            recoveries_per_each_period = 0
            expected_claim_per_each_period_list = []
            pv_netloss = 0
            pv_expected_guarantees_fees = 0

            common_diff = 0
            if facility_amount:
                common_diff = facility_amount / tenor
                principal_amount = facility_amount
            valuesList = []
            treasury_rateList = []
            if sum_weighted_product_score or sum_weighted_product_score == 0:
                sum_weighted_product_score_int = round(sum_weighted_product_score)
                risk_agency_default_rates_env = self.env['risk.agency.default.rates']
                risk_agency_default_rates_results = risk_agency_default_rates_env.search(
                    [('rating', '=', sum_weighted_product_score_int)])
                for rec in risk_agency_default_rates_results:
                    valuesList.append(rec.value)

                risk_free_vectors_env = self.env['risk.free.vectors']
                risk_free_vectors_results = risk_free_vectors_env.search([])
                for rec in risk_free_vectors_results:
                    treasury_rateList.append(rec.treasury_rate)

            for p in range(period + 1):

                if len(valuesList) > p:
                    agency_default_rate_per_each_period = valuesList[p]
                else:
                    agency_default_rate_per_each_period = 0
                Probability_of_default_per_each_period = agency_default_rate_per_each_period * (
                            conversion_factor_default_rate / 100)
                expected_default = Probability_of_default_per_each_period * principal_repayment
                expected_claim_per_each_period = coverage_ratio * expected_default
                expected_claim_per_each_period_list.append(expected_claim_per_each_period)

                if period_t > period_Tr:
                    t = period_t - period_Tr
                    t_int = round(t)
                    if len(expected_claim_per_each_period_list) > t_int:
                        expected_claim_at_t = expected_claim_per_each_period_list[t_int]
                        recoveries_per_each_period = (recovery_rate / 100) * expected_claim_at_t
                else:
                    recoveries_per_each_period = 0

                net_loss = expected_claim_per_each_period - recoveries_per_each_period

                if previous_principal_amount:
                    total_principal_amount = previous_principal_amount + principal_amount
                else:
                    total_principal_amount = principal_amount

                if period_t == 1:
                    utilization_fee = coverage_ratio * total_principal_amount
                else:
                    utilization_fee = coverage_ratio * (total_principal_amount / 2)

                expected_guarantee_fee = (1 - Probability_of_default_per_each_period) * utilization_fee

                if len(treasury_rateList) > p:
                    interest_rate_d = treasury_rateList[p] + premium_d / 100
                else:
                    interest_rate_d = 0

                discount_factor_d = 1 / (1 + interest_rate_d) ** (period_t / 2)

                if tenor == 0:
                    pv_netloss = 0
                elif period_t <= tenor:
                    pv_netloss += (net_loss * discount_factor_d)
                else:
                    pv_netloss += 0

                if len(treasury_rateList) > p:
                    interest_rate_f = treasury_rateList[p] + premium_f / 100
                else:
                    interest_rate_f = 0

                discount_factor_f = 1 / (1 + interest_rate_f) ** (period_t / 2)

                if tenor == 0:
                    pv_expected_guarantees_fees = 0
                elif period_t <= tenor:
                    pv_expected_guarantees_fees += (expected_guarantee_fee * discount_factor_f)
                else:
                    pv_expected_guarantees_fees += 0

                value = {
                    'period': p + 1,
                    'principal_amount': principal_amount,
                    'principal_repayment': principal_repayment,
                    'probability_of_default': Probability_of_default_per_each_period,
                    'expected_default': expected_default,
                    'expected_claim': expected_claim_per_each_period,
                    'recoveries': recoveries_per_each_period,
                    'net_loss': net_loss,
                    'utilization_fee': utilization_fee,
                    'expected_guarantee_fee': expected_guarantee_fee,
                }
                previous_principal_amount = principal_amount
                principal_amount = principal_amount - common_diff
                principal_repayment = common_diff
                period_t = period_t + 1

                ligne_risk_models_amortization_schedule_ids.append((0, 0, value))
                present_value_of_net_loss = pv_netloss
                basis_of_present_value_of_expected_guarantee_fees = pv_expected_guarantees_fees
                if basis_of_present_value_of_expected_guarantee_fees != 0:
                    utilization_fee_required_for_fees_to_cover_claims = (
                                                                                    present_value_of_net_loss / basis_of_present_value_of_expected_guarantee_fees) * 100
                else:
                    utilization_fee_required_for_fees_to_cover_claims = 0

        # risk_models_armotization_schedule_data_dict = self.traiter_risk_models_armotization_schedule_data(period, facility_amount, sum_weighted_product_score,
        #                                                conversion_factor_default_rate, coverage_ratio, recovery_rate,
        #                                                period_after_default_for_recovery, premium_d, premium_f)
        #
        # ligne_risk_models_amortization_schedule_ids = risk_models_armotization_schedule_data_dict['risk_models_amortization_schedule_ids']
        # present_value_of_net_loss = risk_models_armotization_schedule_data_dict['present_value_of_net_loss']
        # basis_of_present_value_of_expected_guarantee_fees = risk_models_armotization_schedule_data_dict['basis_of_present_value_of_expected_guarantee_fees']
        # utilization_fee_required_for_fees_to_cover_claims = risk_models_armotization_schedule_data_dict['utilization_fee_required_for_fees_to_cover_claims']


        return {'value': {'risk_models_amortization_schedule_ids': ligne_risk_models_amortization_schedule_ids,
                          'present_value_of_net_loss': present_value_of_net_loss,
                          'basis_of_present_value_of_expected_guarantee_fees': basis_of_present_value_of_expected_guarantee_fees,
                          'utilization_fee_required_for_fees_to_cover_claims': utilization_fee_required_for_fees_to_cover_claims}}

    def traiter_risk_models_armotization_schedule_data(self, period, facility_amount, sum_weighted_product_score,
                                                       conversion_factor_default_rate, coverage_ratio, recovery_rate,
                                                       period_after_default_for_recovery, premium_d, premium_f):
        '''This action is for treatment of amortization schedule data this action is called by  recompute_risk_models_armotization_schedule_data to recalculate the amortization during update transaction'''

        # for rec in self:
        #     rec.write({'risk_models_amortization_schedule_ids': [(5, 0, 0)]})

        #risk_models_armotization_schedule_data_dict = {'risk_models_amortization_schedule_ids':[],'present_value_of_net_loss':0,'basis_of_present_value_of_expected_guarantee_fees':0, 'utilization_fee_required_for_fees_to_cover_claims':0}

        risk_models_armotization_schedule_data_dict = {}
        ligne_risk_models_amortization_schedule_ids = []

        if period:

            tenor = period

            principal_amount = 0
            principal_repayment = 0
            agency_default_rate_per_each_period = 0
            expected_default = 0
            previous_principal_amount = 0
            period_t = 1
            period_Tr = period_after_default_for_recovery
            recoveries_per_each_period = 0
            expected_claim_per_each_period_list = []
            pv_netloss = 0
            pv_expected_guarantees_fees = 0

            common_diff = 0
            if facility_amount:
                common_diff = facility_amount / tenor
                principal_amount = facility_amount
            valuesList = []
            treasury_rateList = []
            if sum_weighted_product_score or sum_weighted_product_score == 0:
                sum_weighted_product_score_int = round(sum_weighted_product_score)
                risk_agency_default_rates_env = self.env['risk.agency.default.rates']
                risk_agency_default_rates_results = risk_agency_default_rates_env.search(
                    [('rating', '=', sum_weighted_product_score_int)])
                for rec in risk_agency_default_rates_results:
                    valuesList.append(rec.value)

                risk_free_vectors_env = self.env['risk.free.vectors']
                risk_free_vectors_results = risk_free_vectors_env.search([])
                for rec in risk_free_vectors_results:
                    treasury_rateList.append(rec.treasury_rate)

            for p in range(period + 1):

                if len(valuesList) > p:
                    agency_default_rate_per_each_period = valuesList[p]
                else:
                    agency_default_rate_per_each_period = 0
                Probability_of_default_per_each_period = agency_default_rate_per_each_period * (
                        conversion_factor_default_rate / 100)
                expected_default = Probability_of_default_per_each_period * principal_repayment
                expected_claim_per_each_period = coverage_ratio * expected_default
                expected_claim_per_each_period_list.append(expected_claim_per_each_period)

                if period_t > period_Tr:
                    t = period_t - period_Tr
                    t_int = round(t)
                    if len(expected_claim_per_each_period_list) > t_int:
                        expected_claim_at_t = expected_claim_per_each_period_list[t_int]
                        recoveries_per_each_period = (recovery_rate / 100) * expected_claim_at_t
                else:
                    recoveries_per_each_period = 0

                net_loss = expected_claim_per_each_period - recoveries_per_each_period

                if previous_principal_amount:
                    total_principal_amount = previous_principal_amount + principal_amount
                else:
                    total_principal_amount = principal_amount

                if period_t == 1:
                    utilization_fee = coverage_ratio * total_principal_amount
                else:
                    utilization_fee = coverage_ratio * (total_principal_amount / 2)

                expected_guarantee_fee = (1 - Probability_of_default_per_each_period) * utilization_fee

                if len(treasury_rateList) > p:
                    interest_rate_d = treasury_rateList[p] + premium_d / 100
                else:
                    interest_rate_d = 0

                discount_factor_d = 1 / (1 + interest_rate_d) ** (period_t / 2)

                if tenor == 0:
                    pv_netloss = 0
                elif period_t <= tenor:
                    pv_netloss += (net_loss * discount_factor_d)
                else:
                    pv_netloss += 0

                if len(treasury_rateList) > p:
                    interest_rate_f = treasury_rateList[p] + premium_f / 100
                else:
                    interest_rate_f = 0

                discount_factor_f = 1 / (1 + interest_rate_f) ** (period_t / 2)

                if tenor == 0:
                    pv_expected_guarantees_fees = 0
                elif period_t <= tenor:
                    pv_expected_guarantees_fees += (expected_guarantee_fee * discount_factor_f)
                else:
                    pv_expected_guarantees_fees += 0

                value = {
                    'period': p + 1,
                    'principal_amount': principal_amount,
                    'principal_repayment': principal_repayment,
                    'probability_of_default': Probability_of_default_per_each_period,
                    'expected_default': expected_default,
                    'expected_claim': expected_claim_per_each_period,
                    'recoveries': recoveries_per_each_period,
                    'net_loss': net_loss,
                    'utilization_fee': utilization_fee,
                    'expected_guarantee_fee': expected_guarantee_fee,
                }
                previous_principal_amount = principal_amount
                principal_amount = principal_amount - common_diff
                principal_repayment = common_diff
                period_t = period_t + 1

                ligne_risk_models_amortization_schedule_ids.append((0, 0, value))
                present_value_of_net_loss = pv_netloss
                basis_of_present_value_of_expected_guarantee_fees = pv_expected_guarantees_fees
                if basis_of_present_value_of_expected_guarantee_fees != 0:
                    utilization_fee_required_for_fees_to_cover_claims = (
                                                                                present_value_of_net_loss / basis_of_present_value_of_expected_guarantee_fees) * 100
                else:
                    utilization_fee_required_for_fees_to_cover_claims = 0

                risk_models_armotization_schedule_data_dict[
                    'risk_models_amortization_schedule_ids'] = ligne_risk_models_amortization_schedule_ids
                risk_models_armotization_schedule_data_dict['present_value_of_net_loss'] = present_value_of_net_loss
                risk_models_armotization_schedule_data_dict[
                    'basis_of_present_value_of_expected_guarantee_fees'] = basis_of_present_value_of_expected_guarantee_fees
                risk_models_armotization_schedule_data_dict[
                    'utilization_fee_required_for_fees_to_cover_claims'] = utilization_fee_required_for_fees_to_cover_claims



        return   risk_models_armotization_schedule_data_dict

    premium_f = fields.Float(string='Premium F (%)', digits=(5, 2), required=False, compute='_compute_period',
                             inverse='_inverse_period', Store=True)
    premium_d = fields.Float(string='Premium D (%)', digits=(5, 2), required=False, compute='_compute_period',
                             inverse='_inverse_period', Store=True)

    @api.depends('period_id')
    def _compute_period(self):
        for rec in self:
            if rec.period_id.period:
                rec.premium_f = rec.period_id.rate
                premium_d_env = self.env['risk.premium.d.curves']
                premium_d_results = premium_d_env.search([('period', '=', rec.period_id.period)])
                for record in premium_d_results:
                    if record:
                        rec.premium_d = record.rate

    def _inverse_period(self):
        pass

    conversion_factor_default_rate = fields.Float(string='Conversion Factor Default Rate (%)', digits=(5, 2),
                                                  required=False, compute='_compute_conversion_factor_default_rate',
                                                  inverse='_inverse_conversion_factor_default_rate', Store=True)

    @api.depends('country_risk_model_id', 'lender_risk_model_id', 'borrower_risk_model_id', 'transaction_risk_model_id')
    def _compute_conversion_factor_default_rate(self):
        for rec in self:
            conversion_factor_default_rate_env = self.env['risk.pricing.model.constants']
            conversion_factor_default_rate_results = conversion_factor_default_rate_env.search([])
            for record in conversion_factor_default_rate_results:
                if record:
                    rec.conversion_factor_default_rate = record.conversion_factor_default_rate

    def _inverse_conversion_factor_default_rate(self):
        pass

    country_id = fields.Many2one('res.country', string='Country ', required=False)

    recovery_rate = fields.Float(string='Recovery Rate (%)', digits=(5, 2), required=False,
                                 compute='_compute_recovery_rate_period_after_default_for_recovery',
                                 inverse='_inverse_recovery_rate_period_after_default_for_recovery', Store=True)
    period_after_default_for_recovery = fields.Float(string='Period After Default For Recovery', digits=(5, 2),
                                                     required=False,
                                                     compute='_compute_recovery_rate_period_after_default_for_recovery',
                                                     inverse='_inverse_recovery_rate_period_after_default_for_recovery',
                                                     Store=True)

    @api.depends('country_id')
    def _compute_recovery_rate_period_after_default_for_recovery(self):
        for rec in self:
            if rec.country_id:
                risk_recovery_rate_env = self.env['risk.recovery.rate']
                risk_period_after_default_for_recovery_env = self.env['risk.period.after.default.for.recovery']
                risk_recovery_rate_results = risk_recovery_rate_env.search([('country_id', '=', rec.country_id.id)])
                risk_period_after_default_for_recovery_results = risk_period_after_default_for_recovery_env.search(
                    [('country_id', '=', rec.country_id.id)])

                for risk_recovery_rate_result in risk_recovery_rate_results:
                    if risk_recovery_rate_result:
                        rec.recovery_rate = risk_recovery_rate_result.rate

                for risk_period_after_default_for_recovery_result in risk_period_after_default_for_recovery_results:
                    if risk_period_after_default_for_recovery_result:
                        rec.period_after_default_for_recovery = risk_period_after_default_for_recovery_result.period

    coverage_ratio = fields.Float(string='Coverage Ratio', digits=(5, 2), required=False, Store=True)
    facility_currency = fields.Many2one('res.currency', string='Facility Currency ', required=False)
    facility_amount = fields.Float(string='Facility Amount', digits=(5, 2), required=False, Store=True)

    def _inverse_recovery_rate_period_after_default_for_recovery(self):
        pass

    @api.depends('country_risk_model_id')
    def _compute_weighted_score_total(self):
        total = sum(item.weighted_score for item in self.risk_models_simulation_models_model_factor_ids)
        self.weighted_score_total = total

    def _inverse_weighted_score_total(self):
        pass

    @api.depends('lender_risk_model_id')
    def _compute_weighted_score_total_lender(self):
        total = sum(item.weighted_score for item in self.lender_risk_models_simulation_models_model_factor_ids)
        self.weighted_score_total_lender = total

    def _inverse_weighted_score_total_lender(self):
        pass

    @api.depends('borrower_risk_model_id')
    def _compute_weighted_score_total_borrower(self):
        total = sum(item.weighted_score for item in self.borrower_risk_models_simulation_models_model_factor_ids)
        self.weighted_score_total_borrower = total

    def _inverse_weighted_score_total_borrower(self):
        pass

    @api.depends('transaction_risk_model_id')
    def _compute_weighted_score_total_transaction(self):
        total = sum(item.weighted_score for item in self.transaction_risk_models_simulation_models_model_factor_ids)
        self.weighted_score_total_transaction = total

    def _inverse_weighted_score_total_transaction(self):
        pass

    def init_risk_score_and_weighted_score(self, risk_models_simulation_models_model_factor_value, populated):
        '''This action is used to update  risk_score and weighted_score in model factor table. it's called for create value'''
        total = sum(item[2]['score'] for item in populated)
        risk_models_simulation_models_model_factor_value["risk_score"] = total
        risk_models_simulation_models_model_factor_value["weighted_score"] = total * \
                                                                             risk_models_simulation_models_model_factor_value[
                                                                                 "factor_weight"] / 100

    def init_risk_score_and_weighted_score_write(self, risk_models_simulation_models_model_factor_value, populated):

        '''This action is used to update  risk_score and weighted_score in model factor table. it's called for create may be update value'''
        total = sum(item[2]['score'] for item in populated)

        risk_models_simulation_models_model_factor_value.risk_score = total
        risk_models_simulation_models_model_factor_value.weighted_score = total * \
                                                                          risk_models_simulation_models_model_factor_value.factor_weight / 100

    def init_risk_score_and_weighted_score_write_no_update(self, risk_models_simulation_models_model_factor_value, populated):

        '''This action is used to update  risk_score and weighted_score in model factor table. it's called for update value'''

        total = sum(item.score for item in populated)

        risk_models_simulation_models_model_factor_value.risk_score = total
        risk_models_simulation_models_model_factor_value.weighted_score = total * \
                                                                          risk_models_simulation_models_model_factor_value.factor_weight / 100

    # def init_risk_score_and_weighted_score_write(self, risk_models_simulation_models_model_factor_value, populated):
    #     print(populated)
    #     total = sum(item[2]['score'] for item in populated)
    #     print(total)
    #     risk_models_simulation_models_model_factor_value["risk_score"] = total
    #     risk_models_simulation_models_model_factor_value["weighted_score"] = total * \
    #                                                                          risk_models_simulation_models_model_factor_value[
    #                                                                              "factor_weight"] / 100

    risk_models_amortization_schedule_ids = fields.One2many('risk.models.amortization.schedule',
                                                            'risk_models_simulation_id', required=False
                                                            )

    present_value_of_net_loss = fields.Float(string='Present Value of Net Loss', digits=(12, 6), required=False,
                                             Store=True, default=0)
    basis_of_present_value_of_expected_guarantee_fees = fields.Float(
        string='Basis of Present Value of Expected Guarantee Fees ', digits=(12, 6), required=False, Store=True,
        default=0)
    utilization_fee_required_for_fees_to_cover_claims = fields.Float(
        string='Utilization Fee Required for Fees to Cover Claims (%)', digits=(12, 6), required=False, Store=True,
        default=0)

    drapeau = fields.Boolean(Store=False)



    def recompute_risk_models_armotization_schedule_data(self,vals) :

        '''This action is called at any transaction to recompute amortization table'''

        period = 0
        if "period_id" in vals.keys():
            period_id = vals['period_id']
            result = self.env['risk.premium.f.curves'].browse(period_id)
            if result:
                period = result.period
        else:
            period_id = self.period_id
            if period_id :
                period = period_id.period

        if "facility_amount" in vals.keys():
            facility_amount = vals['facility_amount']
        else:
            facility_amount = self.facility_amount

        if "sum_weighted_product_score" in vals.keys():
            sum_weighted_product_score = vals['sum_weighted_product_score']
        else:
            sum_weighted_product_score = self.sum_weighted_product_score

        if "conversion_factor_default_rate" in vals.keys():
            conversion_factor_default_rate = vals['conversion_factor_default_rate']
        else:
            conversion_factor_default_rate = self.conversion_factor_default_rate

        if "coverage_ratio" in vals.keys():
            coverage_ratio = vals['coverage_ratio']
        else:
            coverage_ratio = self.coverage_ratio

        if "recovery_rate" in vals.keys():
            recovery_rate = vals['recovery_rate']
        else:
            recovery_rate = self.recovery_rate

        if "period_after_default_for_recovery" in vals.keys():
            period_after_default_for_recovery = vals['period_after_default_for_recovery']
        else:
            period_after_default_for_recovery = self.period_after_default_for_recovery

        if "premium_d" in vals.keys():
            premium_d = vals['premium_d']
        else:
            premium_d = self.premium_d

        if "premium_f" in vals.keys():
            premium_f = vals['premium_f']
        else:
            premium_f = self.premium_f

        if self.risk_models_amortization_schedule_ids:
            for rec in self.risk_models_amortization_schedule_ids:
                if rec and rec.id :
                    results_amortization = self.env['risk.models.amortization.schedule'].search([('id', '=', rec.id)])
                    if results_amortization:
                        results_amortization.unlink()

        risk_models_armotization_schedule_data_dict = self.traiter_risk_models_armotization_schedule_data(period,facility_amount,sum_weighted_product_score,conversion_factor_default_rate,coverage_ratio,recovery_rate,period_after_default_for_recovery,premium_d, premium_f)

        # if self.risk_models_amortization_schedule_ids:
        #     for rec in self.risk_models_amortization_schedule_ids:
        #         results_amortization = self.env['risk.models.amortization.schedule'].search([('id', '=', rec.id)])
        #         if results_amortization:
        #             results_amortization.unlink()


        if risk_models_armotization_schedule_data_dict :

            vals['risk_models_amortization_schedule_ids'] =  risk_models_armotization_schedule_data_dict['risk_models_amortization_schedule_ids']

            vals['present_value_of_net_loss'] = risk_models_armotization_schedule_data_dict['present_value_of_net_loss']

            vals['basis_of_present_value_of_expected_guarantee_fees'] = risk_models_armotization_schedule_data_dict['basis_of_present_value_of_expected_guarantee_fees']

            vals['utilization_fee_required_for_fees_to_cover_claims'] = risk_models_armotization_schedule_data_dict['utilization_fee_required_for_fees_to_cover_claims']

            # if "risk_models_amortization_schedule_ids" in vals.keys() :
            #     vals['risk_models_amortization_schedule_ids'] =  risk_models_armotization_schedule_data_dict['risk_models_amortization_schedule_ids']
            # if "present_value_of_net_loss" in vals.keys():
            #     vals['present_value_of_net_loss'] = risk_models_armotization_schedule_data_dict['present_value_of_net_loss']
            # if "basis_of_present_value_of_expected_guarantee_fees" in vals.keys():
            #     vals['basis_of_present_value_of_expected_guarantee_fees'] = risk_models_armotization_schedule_data_dict['basis_of_present_value_of_expected_guarantee_fees']
            # if "utilization_fee_required_for_fees_to_cover_claims" in vals.keys():
            #     vals['utilization_fee_required_for_fees_to_cover_claims'] = risk_models_armotization_schedule_data_dict['utilization_fee_required_for_fees_to_cover_claims']
    @api.model
    def create(self, vals):

        '''This action is used to create Simulation transaction in the database.'''

        weighted_score_total = 0
        weighted_score_total_lender = 0
        weighted_score_total_borrower = 0
        weighted_score_total_transaction = 0

        if "risk_models_simulation_models_model_factor_ids" in vals.keys():
            weighted_score_total = 0
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
                    weighted_score_total += risk_models_simulation_models_model_factor_value["weighted_score"]

        if "lender_risk_models_simulation_models_model_factor_ids" in vals.keys():
            weighted_score_total_lender = 0
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
                    weighted_score_total_lender += risk_models_simulation_models_model_factor_value["weighted_score"]

        if "borrower_risk_models_simulation_models_model_factor_ids" in vals.keys():
            weighted_score_total_borrower= 0
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
                    weighted_score_total_borrower += risk_models_simulation_models_model_factor_value["weighted_score"]

        if "transaction_risk_models_simulation_models_model_factor_ids" in vals.keys():

            weighted_score_total_transaction = 0
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
                    weighted_score_total_transaction += risk_models_simulation_models_model_factor_value["weighted_score"]

        sum_weighted_product_score = 0
        if "product_id" in vals.keys():
            id = vals['product_id']
            product_id = self.env['risk.warf.weight.matrices'].browse(id)
        else:
            product_id = self.product_id.id
        if product_id:
            if weighted_score_total:
                weighted_product_score = product_id.country_weight * weighted_score_total / 100
                sum_weighted_product_score += weighted_product_score
            if weighted_score_total_lender:
                weighted_product_score_lender = product_id.lender_weight * weighted_score_total_lender / 100
                sum_weighted_product_score += weighted_product_score_lender
            if weighted_score_total_borrower:
                weighted_product_score_borrower = product_id.borrower_weight * weighted_score_total_borrower / 100
                sum_weighted_product_score += weighted_product_score_borrower
            if weighted_score_total_transaction:
                weighted_product_score_transaction = product_id.transaction_weight * weighted_score_total_transaction / 100
                sum_weighted_product_score += weighted_product_score_transaction
            vals['sum_weighted_product_score'] = sum_weighted_product_score


        self.recompute_risk_models_armotization_schedule_data(vals)



        riskModelsSimulation = super(RiskModelsSimulation, self).create(vals)
        return riskModelsSimulation

    def init_risk_model_factor_id_key(self, risk_models_simulation_models_model_sub_factor_ids, subfactor_model):
        for risk_models_simulation_models_model_sub_factor_id in risk_models_simulation_models_model_sub_factor_ids:
            if isinstance(risk_models_simulation_models_model_sub_factor_id[1], int) :
                result = self.env[subfactor_model].browse(risk_models_simulation_models_model_sub_factor_id[1])
                if not risk_models_simulation_models_model_sub_factor_id[2]:
                    risk_models_simulation_models_model_sub_factor_id[2] = {}

                risk_models_simulation_models_model_sub_factor_id[2][
                    "risk_model_factor_id"] = result.risk_model_factor_id.id
                if not "score" in risk_models_simulation_models_model_sub_factor_id[2].keys():
                    risk_models_simulation_models_model_sub_factor_id[2]["score"] = result.answer.point

    def init_risk_model_factor_id_key_write(self, risk_models_simulation_models_model_sub_factor_ids, subfactor_model):
        for risk_models_simulation_models_model_sub_factor_id in risk_models_simulation_models_model_sub_factor_ids:
            result = self.env[subfactor_model].browse(risk_models_simulation_models_model_sub_factor_id.id)
            if result :
                risk_models_simulation_models_model_sub_factor_id.risk_model_factor_id = result.risk_model_factor_id
                risk_models_simulation_models_model_sub_factor_id.score = result.answer.point


    def write(self, vals):
        '''This action is used to update Simulation transaction in the database.'''
        weighted_score_total = 0
        weighted_score_total_lender = 0
        weighted_score_total_borrower = 0
        weighted_score_total_transaction = 0

        if not "drapeau"  in vals.keys():
            if self.risk_models_simulation_models_model_factor_ids:
                weighted_score_total = 0
                for risk_models_simulation_models_model_factor_id in self.risk_models_simulation_models_model_factor_ids:
                    risk_models_simulation_models_model_factor_value = risk_models_simulation_models_model_factor_id
                    if "risk_models_simulation_models_model_sub_factor_ids" in vals.keys():
                        risk_models_simulation_models_model_sub_factor_ids = vals['risk_models_simulation_models_model_sub_factor_ids']
                        self.init_risk_model_factor_id_key(risk_models_simulation_models_model_sub_factor_ids,  'risk.models.simulation.models.model.sub.factor')
                        populated = list(filter(
                            lambda c: c[2] and (c[2][
                                                    "risk_model_factor_id"] == risk_models_simulation_models_model_factor_value.risk_model_factor_id.id),
                            risk_models_simulation_models_model_sub_factor_ids))
                        self.init_risk_score_and_weighted_score_write(risk_models_simulation_models_model_factor_value,
                                                                      populated)
                    else :
                        risk_models_simulation_models_model_sub_factor_ids = self.risk_models_simulation_models_model_sub_factor_ids
                        self.init_risk_model_factor_id_key_write(risk_models_simulation_models_model_sub_factor_ids,
                                                                 'risk.models.simulation.models.model.sub.factor')
                        populated = list(filter(
                            lambda c: c and (c.risk_model_factor_id.id == risk_models_simulation_models_model_factor_value.risk_model_factor_id.id), risk_models_simulation_models_model_sub_factor_ids))

                        self.init_risk_score_and_weighted_score_write_no_update(risk_models_simulation_models_model_factor_value,
                                                                      populated)

                    weighted_score_total += risk_models_simulation_models_model_factor_value.weighted_score

            if self.lender_risk_models_simulation_models_model_factor_ids:
                weighted_score_total_lender = 0
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
                    else :
                        risk_models_simulation_models_model_sub_factor_ids = self.lender_risk_models_simulation_models_model_sub_factor_ids
                        self.init_risk_model_factor_id_key_write(risk_models_simulation_models_model_sub_factor_ids,
                                                                 'risk.models.simulation.models.model.sub.factor.lender')
                        populated = list(filter(
                            lambda c: c and (
                                        c.risk_model_factor_id.id == risk_models_simulation_models_model_factor_value.risk_model_factor_id.id),
                            risk_models_simulation_models_model_sub_factor_ids))

                        self.init_risk_score_and_weighted_score_write_no_update(
                            risk_models_simulation_models_model_factor_value,
                            populated)



                    weighted_score_total_lender += risk_models_simulation_models_model_factor_value.weighted_score

            if self.borrower_risk_models_simulation_models_model_factor_ids:
                weighted_score_total_borrower = 0
                for risk_models_simulation_models_model_factor_id in self.borrower_risk_models_simulation_models_model_factor_ids:
                    risk_models_simulation_models_model_factor_value = risk_models_simulation_models_model_factor_id
                    if "borrower_risk_models_simulation_models_model_sub_factor_ids" in vals.keys():
                        risk_models_simulation_models_model_sub_factor_ids = vals['borrower_risk_models_simulation_models_model_sub_factor_ids']
                        self.init_risk_model_factor_id_key(risk_models_simulation_models_model_sub_factor_ids,
                                                           'risk.models.simulation.models.model.sub.factor.borrower')
                        populated = list(filter(
                            lambda c: c[2] and (c[2][
                                                    "risk_model_factor_id"] == risk_models_simulation_models_model_factor_value.risk_model_factor_id.id),
                            risk_models_simulation_models_model_sub_factor_ids))

                        self.init_risk_score_and_weighted_score_write(risk_models_simulation_models_model_factor_value,
                                                                      populated)
                    else:
                        risk_models_simulation_models_model_sub_factor_ids = self.borrower_risk_models_simulation_models_model_sub_factor_ids
                        self.init_risk_model_factor_id_key_write(risk_models_simulation_models_model_sub_factor_ids,
                                                                 'risk.models.simulation.models.model.sub.factor.borrower')
                        populated = list(filter(
                            lambda c: c and (
                                        c.risk_model_factor_id.id == risk_models_simulation_models_model_factor_value.risk_model_factor_id.id),
                            risk_models_simulation_models_model_sub_factor_ids))
                        self.init_risk_score_and_weighted_score_write_no_update(
                            risk_models_simulation_models_model_factor_value,
                            populated)

                    weighted_score_total_borrower += risk_models_simulation_models_model_factor_value.weighted_score

            if self.transaction_risk_models_simulation_models_model_factor_ids:
                weighted_score_total_transaction = 0
                for risk_models_simulation_models_model_factor_id in self.transaction_risk_models_simulation_models_model_factor_ids:
                    risk_models_simulation_models_model_factor_value = risk_models_simulation_models_model_factor_id
                    if "transaction_risk_models_simulation_models_model_sub_factor_ids" in vals.keys():
                        risk_models_simulation_models_model_sub_factor_ids = vals['transaction_risk_models_simulation_models_model_sub_factor_ids']
                        self.init_risk_model_factor_id_key(risk_models_simulation_models_model_sub_factor_ids,
                                                           'risk.models.simulation.models.model.sub.factor.transact')
                        populated = list(filter(
                            lambda c: c[2] and (c[2][
                                                    "risk_model_factor_id"] == risk_models_simulation_models_model_factor_value.risk_model_factor_id.id),
                            risk_models_simulation_models_model_sub_factor_ids))

                        self.init_risk_score_and_weighted_score_write(risk_models_simulation_models_model_factor_value,
                                                                      populated)

                    else :
                        risk_models_simulation_models_model_sub_factor_ids = self.transaction_risk_models_simulation_models_model_sub_factor_ids
                        self.init_risk_model_factor_id_key_write(risk_models_simulation_models_model_sub_factor_ids,
                                                           'risk.models.simulation.models.model.sub.factor.transact')
                        populated = list(filter(
                            lambda c: c and (
                                        c.risk_model_factor_id.id == risk_models_simulation_models_model_factor_value.risk_model_factor_id.id),
                            risk_models_simulation_models_model_sub_factor_ids))

                        self.init_risk_score_and_weighted_score_write_no_update(
                            risk_models_simulation_models_model_factor_value,
                            populated)


                    weighted_score_total_transaction += risk_models_simulation_models_model_factor_value.weighted_score

            sum_weighted_product_score = 0
            if "product_id" in vals.keys():
                id = vals['product_id']
                product_id = self.env['risk.warf.weight.matrices'].browse(id)
            else :
                product_id = self.product_id
            if product_id:
                if weighted_score_total:
                    weighted_product_score = product_id.country_weight * weighted_score_total / 100
                    sum_weighted_product_score += weighted_product_score
                if weighted_score_total_lender:
                    weighted_product_score_lender = product_id.lender_weight * weighted_score_total_lender / 100
                    sum_weighted_product_score += weighted_product_score_lender
                if weighted_score_total_borrower:
                    weighted_product_score_borrower = product_id.borrower_weight * weighted_score_total_borrower / 100
                    sum_weighted_product_score += weighted_product_score_borrower
                if weighted_score_total_transaction:
                    weighted_product_score_transaction = product_id.transaction_weight * weighted_score_total_transaction / 100
                    sum_weighted_product_score += weighted_product_score_transaction
                vals['sum_weighted_product_score'] = sum_weighted_product_score

            self.recompute_risk_models_armotization_schedule_data(vals)

        riskModelsSimulation = super(RiskModelsSimulation, self).write(vals)

        return riskModelsSimulation

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        '''Search action.'''


        args += [('risk_model_workflow_id', '=', False)]

        return super(RiskModelsSimulation, self)._search(args, offset, limit, order, count=count,
                                                      access_rights_uid=access_rights_uid)

    # def recompute_factor_and_subfactor(self, factor_ids, sub_factor_ids):
    #
    #     if factor_ids:
    #         for risk_models_simulation_models_model_factor_id in self.factor_ids:
    #             risk_models_simulation_models_model_factor_value = risk_models_simulation_models_model_factor_id
    #             if "transaction_risk_models_simulation_models_model_sub_factor_ids" in vals.keys():
    #                 risk_models_simulation_models_model_sub_factor_ids = vals[
    #                     'transaction_risk_models_simulation_models_model_sub_factor_ids']
    #                 self.init_risk_model_factor_id_key(risk_models_simulation_models_model_sub_factor_ids,
    #                                                    'risk.models.simulation.models.model.sub.factor.transact')
    #                 populated = list(filter(
    #                     lambda c: c[2] and (c[2][
    #                                             "risk_model_factor_id"] == risk_models_simulation_models_model_factor_value.risk_model_factor_id.id),
    #                     risk_models_simulation_models_model_sub_factor_ids))
    #                 self.init_risk_score_and_weighted_score_write(risk_models_simulation_models_model_factor_value,
    #                                                               populated)
    #

    def init_risk_models_simulation_data(self, risk_models_id):
        '''This action is used to inialize a  risk model factor and subfactor of particular risk_models_id '''

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

        '''This action is used to inialize a  risk model factor and subfactor of particular risk_models_id passing risk_models_simulation_models_model_factor_ids and   risk_models_simulation_models_model_sub_factor_ids. is a generic method'''

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

        '''This action will be used if we need to initialize multiple risk models by specifies simultaneously the list of risk model id'''



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





    risk_model_workflow_id = fields.Many2one('risk.model.workflow', string="Workflow", required=False)




    #------------------------------validate and dreft action
    def button_validate(self):
        self.write({
            'status': '2',
         })

    def button_draft(self):
        self.write({
            'status': '1',
         })

# ----------------------------------------MANAGE OF COUNTRY RISK-------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------
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

    status = fields.Selection("Status", related='risk_models_simulation_id.status')


    # weighted_score_total = fields.Float(string='Weighted Score', required=False)

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

    status = fields.Selection("Status", related='risk_models_simulation_id.status')
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
    status = fields.Selection("Status", related='risk_models_simulation_id.status')

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
    status = fields.Selection("Status", related='risk_models_simulation_id.status')

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
    status = fields.Selection("Status", related='risk_models_simulation_id.status')

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
    status = fields.Selection("Status", related='risk_models_simulation_id.status')

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
    status = fields.Selection("Status", related='risk_models_simulation_id.status')

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
    status = fields.Selection("Status", related='risk_models_simulation_id.status')

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


class RiskModelsAmortizationSchedule(models.Model):
    '''This class is for simulation of Risk Amortization Schedule '''

    _name = 'risk.models.amortization.schedule'
    _description = 'This applies to  risk amortization'
    _rec_name = 'period'

    risk_models_simulation_id = fields.Many2one('risk.models.simulation', string='Simulation', required=False)
    period = fields.Integer(string='Period', required=True)
    principal_amount = fields.Float(string='Principal Amount', required=True, default=0, digits=(12, 6))
    principal_repayment = fields.Float(string='Principal Repayment', required=True, default=0, digits=(12, 6))
    probability_of_default = fields.Float(string='Probability of Default', required=True, default=0, digits=(12, 6))
    expected_default = fields.Float(string='Expected Default', required=True, default=0, digits=(12, 6))
    expected_claim = fields.Float(string='Expected Claim', required=True, default=0, digits=(12, 6))
    recoveries = fields.Float(string='Recoveries', required=True, default=0, digits=(12, 6))
    net_loss = fields.Float(string='Net Loss', required=True, default=0, digits=(12, 6))
    utilization_fee = fields.Float(string='Utilization Fee', required=True, default=0, digits=(12, 6))
    expected_guarantee_fee = fields.Float(string='Expected Guarantee Fee', required=True, default=0, digits=(12, 6))
