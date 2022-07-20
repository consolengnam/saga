# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class agf_location(models.Model):
#     _name = 'agf_location.agf_location'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#     self.value2 = float(self.value) / 100

class AgfCountry(models.Model):
    _name = 'agf.country'

    name = fields.Many2one('res.country', string='Country')
    region = fields.Selection([('CAN','CAN'),('EA','EA'),('SA','SA'),('WA','WA')], string='Region')
    sub_region = fields.Selection([('Central Africa','Central Africa'),('North Africa','North Africa'),('East Africa','East Africa'),('Southern Africa','Southern Africa'),('Zone 1','Zone 1'),('Zone 2','Zone 2'),('Zone 3','Zone 3')], string='Sub-Region')
    description = fields.Text()

