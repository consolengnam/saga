# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools, SUPERUSER_ID



class agfScreening(models.Model):
    _name = 'agf.screening.task'
    _description = 'E&S Screening Task'


    name = fields.Char('Task')
