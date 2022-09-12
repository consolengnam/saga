# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools, SUPERUSER_ID
from odoo.tools.translate import _
from odoo.exceptions import UserError, AccessError


class agfScreening(models.Model):
    _inherit = 'agf.screening'

    categorization_id = fields.Many2one('agf.categorization', string='Categorization')

    @api.model
    def create(self, values):
        # Override the original create function for the res.partner model
        record = super(agfScreening, self).create(values)
        cat_values = {
            'name': record.name,
            'guarantee_party': record.guarantee_party,
            'types_of_institution': record.types_of_institution,
            'es_country': record.es_country.id
        }
        categorization = self.env['agf.categorization'].sudo().create(cat_values)
        record.categorization_id = categorization.id
        return record
