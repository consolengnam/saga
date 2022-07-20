# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools

class agfInternalDDQuestionnaire(models.Model):
    _name = 'agf.questionnaire'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin', 'format.address.mixin']
    _description = 'Internal DD Questionnaire, direct or indirect'

    name = fields.Char('Name of the borrower', related='screening_id.name', readonly=True)
    name_of_lender = fields.Char('Name of the lender')
    guarantee_identifier = fields.Char('Guarantee Identifier', related='screening_id.guarantee_identifier', readonly=True)
    executed_by = fields.Char('Executed By')
    es_date = fields.Date(string='Date')
    screening_id = fields.Many2one('agf.screening')
    sector = fields.Char('Sector')
    sub_sector = fields.Char('Sub-Sector')
    tenor = fields.Char('Tenor', related='screening_id.opportinuty_id.guarantee_tenor', readonly=True)
    product_type = fields.Char('Product type', related='screening_id.opportinuty_id.guarantee_product.name', readonly=True)
    tiering = fields.Selection([('Tier I','Tier I'),('Tier II','Tier II'),('Tier III','Tier III')], string='Tiering')
    country = fields.Char(related='screening_id.es_country.name.name', string='Country', readonly=True)


