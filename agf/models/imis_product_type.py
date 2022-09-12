# -*- coding: utf-8 -*-

from odoo import models, fields, api

class imis_crm_product_type(models.Model):

    _name = 'crm.imis.product.type'
    _order = 'sequence, id'

    name = fields.Char('Product Types')
    sequence = fields.Integer('Sequence', default=10)

class imis_crm_product(models.Model):

    _name = 'crm.imis.product'
    _order = 'sequence, id'

    name = fields.Char('Name', required=True, translate=True)
    product_type_id = fields.Many2one('crm.imis.product.type', string='Product Types')
    sequence = fields.Integer('Sequence', default=10)

