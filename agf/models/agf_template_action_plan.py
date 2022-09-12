# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools

class agfTemplateActionplan(models.Model):
    _name = 'agf.template.actionplan'
    _description = 'Template action plan'

    name = fields.Char('ENVIRONMENTAL & SOCIAL RISK')
    q = fields.Integer('#')
#    es_risk = fields.Char()
    corrective_action = fields.Char('CORRECTIVE ACTION')
    timeline = fields.Date('Start On')
    duration = fields.Char('Duration')
    responsible_person = fields.Char('RESPONSIBLE PERSON')
    status = fields.Selection([('Insufficient information','Insufficient information'),('Insufficient progress','Insufficient progress'),('In progress','In progress'),('Major breach','Major breach'),('Closed ','Closed ')], string='STATUS')
    further_action_required_yes = fields.Selection([('Yes','Yes'),('No','No')], string='FURTHER ACTION REQUIRED?')
    further_action_required_comment = fields.Text('Comment')
    topic = fields.Selection([('NA','NA'), ('General','General'), ('Management Commitment','Management Commitment'), ('Management System','Management System'), ('Management System - Policy','Management System - Policy'),('Management System - Procedures','Management System - Procedures'),('Management System - Credit E&S risk Review','Management System - Credit E&S risk Review'),('Management System - Monitoring and Reporting','Management System - Monitoring and Reporting'), ('Labour Conditions, Occupational Health & Safety','Labour Conditions, Occupational Health & Safety'), ('Capacity & Competency','Capacity & Competency'),('Pollution Prevention and Control','Pollution Prevention and Control'),('Reputational Risk Review','Reputational Risk Review'),('Community Health & Safety','Community Health & Safety'),('Value Add','Value Add'),('Other','Other')], compute='_compute_topic', store='True', default='NA', string='Topic')
    questionnaire_id = fields.Many2one('agf.questionnaire', ondelete='cascade')

    @api.depends('q')
    def _compute_topic(self):
        topic = 'NA'
        print('je suis dedans')
        for ap in self:
            print(ap.questionnaire_id.questionnaire_type)
            if ap.questionnaire_id.questionnaire_type == 'Direct':
                if ap.q > 0 and ap.q < 10:
                    topic = 'General'
                if ap.q > 9 and ap.q < 13:
                    topic = 'Management System'
                if ap.q > 12 and ap.q < 17:
                    topic = 'Labour Conditions, Occupational Health & Safety'
                if ap.q > 16 and ap.q < 20:
                    topic = 'Pollution Prevention and Control'
                if ap.q > 19 and ap.q < 23:
                    topic = 'Community Health & Safety'
                if ap.q > 22 and ap.q < 26:
                    topic = 'Reputational Risk Review'
                if ap.q == 26:
                    topic = 'Other'
            if ap.questionnaire_id.questionnaire_type == 'Indirect':
                if ap.q > 0 and ap.q < 4:
                    topic = 'Management Commitment'
                if ap.q > 3 and ap.q < 7:
                    topic = 'Management System - Policy'
                if ap.q > 6 and ap.q < 9:
                    topic = 'Management System - Procedures'
                if ap.q > 8 and ap.q < 12:
                    topic = 'Management System - Credit E&S risk Review'
                if ap.q > 11 and ap.q < 15:
                    topic = 'Management System - Monitoring and Reporting'
                if ap.q > 14 and ap.q < 17:
                    topic = 'Capacity & Competency'
                if ap.q > 16 and ap.q < 20:
                    topic = 'Reputational Risk Review'
                if ap.q == 20:
                    topic = 'Value Add'
            ap.topic = topic
