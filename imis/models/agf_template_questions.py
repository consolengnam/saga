# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools


class agfTemplateQuestions(models.Model):
    _name = 'agf.template.questions'
    _description = 'Template Questions'

    name = fields.Char('Questions Number')
    assessment_criteria = fields.Text('Assessment Criteria')
    standards = fields.Text('Standards')
    question = fields.Text('Question')
    wta = fields.Text(string='What To Ask/To Look For')
    findings_yes_no = fields.Selection([('NA','NA'),('Yes','Yes'),('No','No')], default='NA')
    findings_comment = fields.Text('Comment')
    gaps = fields.Text(string='Example of Gaps')
    action_required_yes = fields.Selection([('NA','NA'),('Yes','Yes'),('No','No')], default='NA')
    action_required_comment = fields.Text('Action Comment')
    questionnaire_id = fields.Many2one('agf.questionnaire', ondelete='cascade')

