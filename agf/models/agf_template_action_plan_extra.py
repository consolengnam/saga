# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools

class agfTemplateActionplanExtra(models.Model):
    _name = 'agf.template.actionplan.extra'
    _description = 'Template action plan extra'

    name = fields.Char('Based on the information obtained, which main E&S risks are not appropriately managed by the Guarantee?')
    q = fields.Integer('#')
    es_risk_capacity = fields.Selection([('Yes','Yes'),('No','No')], string='Does the Guarantee lack the capacity to manage those risks (action plan, dedicated resources, etc.)?')
    es_risk_of_default = fields.Selection([('Yes','Yes'),('No','No')], string='Is there a risk of default on guarantee facilities associated with this risk ?')
    es_risk_of_reputation = fields.Selection([('Yes','Yes'),('No','No')], string='Is there a reputational risk for the African Guarantee Fund?')
    questionnaire_id = fields.Many2one('agf.questionnaire', ondelete='cascade')

