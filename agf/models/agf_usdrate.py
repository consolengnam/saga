# -*- coding: utf-8 -*-

from odoo import models, fields, api

class agf_year_rate(models.Model):
    _name = 'agf.usdrate'

    name = fields.Char('Local Currency')
    rate = fields.Float('USD Rate')


