# -*- coding: utf-8 -*-

from odoo import models, fields, api
import re


class esDDReport(models.TransientModel):
    _name = 'agf.es.dd.report'
    _description = 'Screening Reports'

    name = fields.Char(string="Reference")
    version = fields.Integer(string="Version")
    report_type = fields.Selection([('DD Report','ES Due Diligence Report'),('IC Information Note','Investment Committee ES Information Note')], default='DD Report', string='Report Type')
    questionnaire_id = fields.Many2one('agf.questionnaire', string='Questionnaire', domain="[('questionnaire_type', '=', 'Indirect')]")
    mc_gaps = fields.Text('Gaps')
    mspolicy_gaps = fields.Text('Gaps')
    msprocedure_gaps = fields.Text('Gaps')
    mscrr_gaps = fields.Text('Gaps')
    msmr_gaps = fields.Text('Gaps')
    cc_gaps = fields.Text('Gaps')
    rr_gaps = fields.Text('Gaps')
    remarks = fields.Text('Remarks')
    mc_ai = fields.Text('Assessment Indicator')
    mspolicy_ai = fields.Text('Assessment Indicator')
    msprocedure_ai = fields.Text('Assessment Indicator')
    mscrr_ai = fields.Text('Assessment Indicator')
    msmr_ai = fields.Text('Assessment Indicator')
    cc_ai = fields.Text('Assessment Indicator')
    rr_ai = fields.Text('Assessment Indicator')
    other_ai = fields.Text('Assessment Indicator')
    introduction_background = fields.Text('Background')
    aims_and_objective = fields.Text('Aims and Objectives')
    description = fields.Text('Description')
    conclusion = fields.Text('Conclusion')
    screening_questionnaire = fields.Boolean('ES Screening Questionnaire')
    ddreportsumary = fields.Boolean('Due Diligence report summary')
    internalddquestionnalire = fields.Boolean('Internal ES DD questionnaire')
    es_actionplan = fields.Boolean('ES Action Plan (ESAP)')

    screening_questionnaire_hr = fields.Selection([('Required','Required'),('Not required','Not required')], string="High E.S Risks")
    screening_questionnaire_mr = fields.Selection([('Required','Required'),('Not required','Not required')], string="Medium E.S Risks")
    screening_questionnaire_lr = fields.Selection([('Required','Required'),('Not required','Not required')], string="Low E.S Risks")

    ddreportsumary_hr = fields.Selection([('Required', 'Required'), ('Not required', 'Not required')], string="High E.S Risks")
    ddreportsumary_mr = fields.Selection([('Required', 'Required'), ('Not required', 'Not required')], string="Medium E.S Risks")
    ddreportsumary_lr = fields.Selection([('Required', 'Required'), ('Not required', 'Not required')], string="Low E.S Risks")

    internalddquestionnalire_hr = fields.Selection([('Required', 'Required'), ('Not required', 'Not required')], string="High E.S Risks")
    internalddquestionnalire_mr = fields.Selection([('Required', 'Required'), ('Not required', 'Not required')], string="Medium E.S Risks")
    internalddquestionnalire_lr = fields.Selection([('Required', 'Required'), ('Not required', 'Not required')], string="Low E.S Risks")

    es_actionplan_hr = fields.Selection([('Required', 'Required'), ('Not required', 'Not required')], string="High E.S Risks")
    es_actionplan_mr = fields.Selection([('Required', 'Required'), ('Not required', 'Not required')], string="Medium E.S Risks")
    es_actionplan_lr = fields.Selection([('Required', 'Required'), ('Not required', 'Not required')], string="Low E.S Risks")

    main_identified_es_risk_1 = fields.Selection([('Sufficient','Sufficient'),('Insufficient, ESAP','Insufficient, ESAP')], string='Status')
    main_identified_es_risk_2 = fields.Selection([('Sufficient','Sufficient'),('Insufficient, ESAP','Insufficient, ESAP')], string='Status')
    main_identified_es_risk_3 = fields.Selection([('Sufficient','Sufficient'),('Insufficient, ESAP','Insufficient, ESAP')], string='Status')
    main_identified_es_risk_4 = fields.Selection([('Sufficient','Sufficient'),('Insufficient, ESAP','Insufficient, ESAP')], string='Status')
    main_identified_es_risk_1_text = fields.Char('Main identified ES risk 1')
    main_identified_es_risk_2_text = fields.Char('Main identified ES risk 2')
    main_identified_es_risk_3_text = fields.Char('Main identified ES risk 3')
    main_identified_es_risk_4_text = fields.Char('Main identified ES risk 4')
    standards_clauses = fields.Boolean('ES Standards Clauses')
    modification_standard_clauses = fields.Boolean('Modification of the standard clauses')
    favorable = fields.Boolean('Favourable')
    additional_comments = fields.Text('Additional Comments')


#@api multi
    def get_report(self):
        """Call when button 'Get Report' clicked.
                """
        data1 = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'name': self.name,
                'version': self.version,
                'questionnaire_id': self.questionnaire_id.id,
                'remarks': self.remarks,
                'background': self.introduction_background,
                'aao': self.aims_and_objective,
                'description': self.description,
                'conclusion': self.conclusion,
                'mc_gaps': self.mc_gaps,
                'mspolicy_gaps': self.mspolicy_gaps,
                'msprocedure_gaps': self.msprocedure_gaps,
                'mscrr_gaps': self.mscrr_gaps,
                'msmr_gaps': self.msmr_gaps,
                'cc_gaps': self.cc_gaps,
                'rr_gaps': self.rr_gaps,
                'mc_ai': self.mc_ai,
                'mspolicy_ai': self.mspolicy_ai,
                'msprocedure_ai': self.msprocedure_ai,
                'mscrr_ai': self.mscrr_ai,
                'msmr_ai': self.msmr_ai,
                'cc_ai': self.cc_ai,
                'rr_ai': self.rr_ai,
                'other_ai': self.other_ai,
            },
        }

        data2 = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'name': self.name,
                'version': self.version,
                'questionnaire_id': self.questionnaire_id.id,
                'screening_questionnaire': self.screening_questionnaire,
                'ddreportsumary': self.ddreportsumary,
                'internalddquestionnalire': self.internalddquestionnalire,
                'es_actionplan': self.es_actionplan,
                'screening_questionnaire_hr': self.screening_questionnaire_hr,
                'screening_questionnaire_mr': self.screening_questionnaire_mr,
                'screening_questionnaire_lr': self.screening_questionnaire_lr,
                'ddreportsumary_hr': self.ddreportsumary_hr,
                'ddreportsumary_mr': self.ddreportsumary_mr,
                'ddreportsumary_lr': self.ddreportsumary_lr,
                'internalddquestionnalire_hr': self.internalddquestionnalire_hr,
                'internalddquestionnalire_mr': self.internalddquestionnalire_mr,
                'internalddquestionnalire_lr': self.internalddquestionnalire_lr,
                'es_actionplan_hr': self.es_actionplan_hr,
                'es_actionplan_mr': self.es_actionplan_mr,
                'es_actionplan_lr': self.es_actionplan_lr,
                'main_identified_es_risk_1': self.main_identified_es_risk_1,
                'main_identified_es_risk_2': self.main_identified_es_risk_2,
                'main_identified_es_risk_3': self.main_identified_es_risk_3,
                'main_identified_es_risk_4': self.main_identified_es_risk_4,
                'main_identified_es_risk_1_text': self.main_identified_es_risk_1_text,
                'main_identified_es_risk_2_text': self.main_identified_es_risk_2_text,
                'main_identified_es_risk_3_text': self.main_identified_es_risk_3_text,
                'main_identified_es_risk_4_text': self.main_identified_es_risk_4_text,
                'standards_clauses': self.standards_clauses,
                'modification_standard_clauses': self.modification_standard_clauses,
                'favorable': self.favorable,
                'additional_comments': self.additional_comments,
            },
        }

        # use `module_name.report_id` as reference.
        # `report_action()` will call `get_report_values()` and pass `data` automatically.
        if self.report_type == 'IC Information Note':
            return self.env.ref('agf.internal_note').report_action(self, data=data2)
        else:
            return self.env.ref('agf.dd_report').report_action(self, data=data1)



class ReportESDD(models.AbstractModel):
    """Abstract Model for report template.
    for `_name` model, please use `report.` as prefix then add `module_name.report_name`.
    """

    _name = 'report.agf.dd_report_view'

    @api.model
    def get_report_values(self, docids, data=None):
        name = data['form']['name']
        version = data['form']['version']
        questionnaire_id = data['form']['questionnaire_id']
        remarks = data['form']['remarks']
        background = data['form']['background']
        aao = data['form']['aao']
        description = data['form']['description']
        conclusion = data['form']['conclusion']
        mc_gaps = data['form']['mc_gaps']
        mspolicy_gaps = data['form']['mspolicy_gaps']
        msprocedure_gaps = data['form']['msprocedure_gaps']
        mscrr_gaps = data['form']['mscrr_gaps']
        msmr_gaps = data['form']['msmr_gaps']
        cc_gaps = data['form']['cc_gaps']
        rr_gaps = data['form']['rr_gaps']
        mc_ai = data['form']['mc_ai']
        mspolicy_ai = data['form']['mspolicy_ai']
        msprocedure_ai = data['form']['msprocedure_ai']
        mscrr_ai = data['form']['mscrr_ai']
        msmr_ai = data['form']['msmr_ai']
        cc_ai = data['form']['cc_ai']
        rr_ai = data['form']['rr_ai']
        other_ai = data['form']['other_ai']
        questionnaire = self.env['agf.questionnaire'].browse(questionnaire_id)
        institution_type = questionnaire.institution_type
        tiering = questionnaire.tiering
        category = questionnaire.category_fi_sme_id.name
        tenor = questionnaire.tenor
        product_type = questionnaire.product_type
        screening = questionnaire.screening_id.name
        es_date = questionnaire.es_date
        country = questionnaire.country
        executed_by = questionnaire.executed_by
        co_guarantor = questionnaire.screening_id.co_guarantor
        guarantee_identifier = questionnaire.guarantee_identifier
        borrower = questionnaire.name
        lender = questionnaire.name_of_lender

        questions = []
        question_ids = questionnaire.questions_ids
        cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        for question_id in question_ids:
            question = question_id.question
            question = re.sub(cleanr, '', question)
            questions.append({
                'id': question_id.name,
                'assessment_criteria': question_id.assessment_criteria,
                'assessment_indicator': question,
                'findings': question_id.findings_comment,
            })
        action_plans = []
        action_plan_ids = questionnaire.action_plan_ids
        for action_plan_id in action_plan_ids:
            action_plans.append({
                'id': action_plan_id.q,
                'assessment_criteria': action_plan_id.topic,
                'es_risk': action_plan_id.name,
                'corrective_action': action_plan_id.corrective_action,
                'timeline': action_plan_id.timeline,
                'duration': action_plan_id.duration,
            })
        return {
            'name': name,
            'version': version,
            'tiering': tiering,
            'category': category,
            'tenor': tenor,
            'institution_type': institution_type,
            'product_type': product_type,
            'screening': screening,
            'es_date': es_date,
            'country': country,
            'executed_by': executed_by,
            'co_guarantor': co_guarantor,
            'guarantee_identifier': guarantee_identifier,
            'borrower': borrower,
            'lender': lender,
            'background': background,
            'aao': aao,
            'description': description,
            'conclusion': conclusion,
            'mc_gaps': mc_gaps,
            'mspolicy_gaps': mspolicy_gaps,
            'msprocedure_gaps': msprocedure_gaps,
            'mscrr_gaps': mscrr_gaps,
            'msmr_gaps': msmr_gaps,
            'cc_gaps': cc_gaps,
            'rr_gaps': rr_gaps,
            'remarks': remarks,
            'mc_ai': mc_ai,
            'mspolicy_ai': mspolicy_ai,
            'msprocedure_ai': msprocedure_ai,
            'mscrr_ai': mscrr_ai,
            'msmr_ai': msmr_ai,
            'cc_ai': cc_ai,
            'rr_ai': rr_ai,
            'other_ai': other_ai,
            'questions': questions,
            'action_plans': action_plans,
        }


class ReportICESIN(models.AbstractModel):
    """Abstract Model for report template.
    for `_name` model, please use `report.` as prefix then add `module_name.report_name`.
    """

    _name = 'report.agf.icesin_report_view'

    @api.model
    def get_report_values(self, docids, data=None):
        name = data['form']['name']
        version = data['form']['version']
        questionnaire_id = data['form']['questionnaire_id']
        questionnaire = self.env['agf.questionnaire'].browse(questionnaire_id)
        institution_type = questionnaire.institution_type
        tiering = questionnaire.tiering
        category = questionnaire.category_fi_sme_id.name
        tenor = questionnaire.tenor
        product_type = questionnaire.product_type
        screening = questionnaire.screening_id.name
        es_date = questionnaire.es_date
        country = questionnaire.country
        executed_by = questionnaire.executed_by
        co_guarantor = questionnaire.screening_id.co_guarantor
        guarantee_identifier = questionnaire.guarantee_identifier
        borrower = questionnaire.name
        lender = questionnaire.name_of_lender
        guarantee_party = questionnaire.screening_id.guarantee_party
        es_category = questionnaire.screening_id.categorization_id.es_category
        screening_questionnaire = data['form']['screening_questionnaire']
        ddreportsumary = data['form']['ddreportsumary']
        internalddquestionnalire = data['form']['internalddquestionnalire']
        es_actionplan = data['form']['es_actionplan']
        screening_questionnaire_hr = data['form']['screening_questionnaire_hr']
        screening_questionnaire_mr = data['form']['screening_questionnaire_mr']
        screening_questionnaire_lr = data['form']['screening_questionnaire_lr']
        ddreportsumary_hr = data['form']['ddreportsumary_hr']
        ddreportsumary_mr = data['form']['ddreportsumary_mr']
        ddreportsumary_lr = data['form']['ddreportsumary_lr']
        internalddquestionnalire_hr = data['form']['internalddquestionnalire_hr']
        internalddquestionnalire_mr = data['form']['internalddquestionnalire_mr']
        internalddquestionnalire_lr = data['form']['internalddquestionnalire_lr']
        es_actionplan_hr = data['form']['es_actionplan_hr']
        es_actionplan_mr = data['form']['es_actionplan_mr']
        es_actionplan_lr = data['form']['es_actionplan_lr']
        main_identified_es_risk_1 = data['form']['main_identified_es_risk_1']
        main_identified_es_risk_2 = data['form']['main_identified_es_risk_2']
        main_identified_es_risk_3 = data['form']['main_identified_es_risk_3']
        main_identified_es_risk_4 = data['form']['main_identified_es_risk_4']
        main_identified_es_risk_1_text = data['form']['main_identified_es_risk_1_text']
        main_identified_es_risk_2_text = data['form']['main_identified_es_risk_2_text']
        main_identified_es_risk_3_text = data['form']['main_identified_es_risk_3_text']
        main_identified_es_risk_4_text = data['form']['main_identified_es_risk_4_text']
        standards_clauses = data['form']['standards_clauses']
        modification_standard_clauses = data['form']['modification_standard_clauses']
        favorable = data['form']['favorable']
        additional_comments = data['form']['additional_comments']

        summary_tasks = []
        summary_task_ids = questionnaire.screening_id.categorization_id.summary_tasks
        for summary_task_id in summary_task_ids:
            summary_tasks.append({
                'name': summary_task_id.name,
            })

        return {
            'name': name,
            'version': version,
            'tiering': tiering,
            'category': category,
            'tenor': tenor,
            'institution_type': institution_type,
            'product_type': product_type,
            'screening': screening,
            'es_date': es_date,
            'country': country,
            'executed_by': executed_by,
            'co_guarantor': co_guarantor,
            'guarantee_identifier': guarantee_identifier,
            'borrower': borrower,
            'lender': lender,
            'guarantee_party': guarantee_party,
            'es_category': es_category,
            'screening_questionnaire': screening_questionnaire,
            'ddreportsumary': ddreportsumary,
            'internalddquestionnalire': internalddquestionnalire,
            'es_actionplan': es_actionplan,
            'screening_questionnaire_hr': screening_questionnaire_hr,
            'screening_questionnaire_mr': screening_questionnaire_mr,
            'screening_questionnaire_lr': screening_questionnaire_lr,
            'ddreportsumary_hr': ddreportsumary_hr,
            'ddreportsumary_mr': ddreportsumary_mr,
            'ddreportsumary_lr': ddreportsumary_lr,
            'internalddquestionnalire_hr': internalddquestionnalire_hr,
            'internalddquestionnalire_mr': internalddquestionnalire_mr,
            'internalddquestionnalire_lr': internalddquestionnalire_lr,
            'es_actionplan_hr': es_actionplan_hr,
            'es_actionplan_mr': es_actionplan_mr,
            'es_actionplan_lr': es_actionplan_lr,
            'main_identified_es_risk_1': main_identified_es_risk_1,
            'main_identified_es_risk_2': main_identified_es_risk_2,
            'main_identified_es_risk_3': main_identified_es_risk_3,
            'main_identified_es_risk_4': main_identified_es_risk_4,
            'main_identified_es_risk_1_text': main_identified_es_risk_1_text,
            'main_identified_es_risk_2_text': main_identified_es_risk_2_text,
            'main_identified_es_risk_3_text': main_identified_es_risk_3_text,
            'main_identified_es_risk_4_text': main_identified_es_risk_4_text,
            'summary_tasks': summary_tasks,
            'standards_clauses': standards_clauses,
            'modification_standard_clauses': modification_standard_clauses,
            'favorable': favorable,
            'additional_comments': additional_comments,
        }

