# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools, SUPERUSER_ID
from odoo.tools.translate import _
from odoo.exceptions import UserError, AccessError
import datetime


class agfScreening(models.Model):
    _name = 'agf.screening'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin', 'format.address.mixin']
    _description = 'E&S Screening'


    name = fields.Char("Name of the Borrower")
    opportinuty_id = fields.Many2one('crm.lead', domain="[('stage_id', '=', 3),('screening_ids', '=', False)]", required=True)
    guarantee_party = fields.Char(string='Guarantee Party', related='opportinuty_id.partner_id.name', readonly=True)
    guarantee_identifier = fields.Char(compute="_compute_identifier", string="Guarantee Identifier", store=True)
    types_of_institution = fields.Selection(
        [('Financial Institution', 'Financial Institution'), ('SME', 'SME'), ('Corporate', 'Corporate')])
    co_guarantor = fields.Char("Co-Guarantor")
    executed_by = fields.Char(string='Executed by')
    es_country = fields.Many2one('agf.country')
    es_date = fields.Date('Date')
    es_activities = fields.Selection([('yes', 'Yes'), ('no', 'No')])
    es_activities_reason_yes = fields.Text(default='NA')
    es_activities_reason_no = fields.Text(default='NA')
    create_date = fields.Datetime(readonly=True)
    number_in_month = fields.Integer(compute="_compute_number_in_month", store=True)

    @api.depends('number_in_month')
    def _compute_identifier(self):
        """ Compute create_date to match identifier patterns """
        today = datetime.datetime.now()
        es_year = today.year
        es_month = today.month
        day = 1
        first_date = datetime.datetime(es_year, es_month, day)
        first_date = str(first_date)
        print(first_date)
        search_domain = [('create_date','>=',first_date)]
        order = 'create_date DESC'
        p_record = self.env['agf.screening'].search(search_domain, order=order, limit=1)
        print(p_record)
        if p_record.exists():
            x = p_record.number_in_month
        else:
            x = 1
        x = "{:02d}".format(x)
        str_es_year = str(es_year)[-2:]
        str_es_month = str(today.strftime("%m"))
        print(x)
        print(str_es_month)
        print(str_es_year)
        for es in self:
            es.guarantee_identifier = 'E&S/'+str_es_year+'-'+str_es_month+'/'+x
            print(es.guarantee_identifier)

    @api.depends('create_date')
    def _compute_number_in_month(self):
        """ keep number of month in case of delete previous record"""
        today = datetime.datetime.now()
        es_year = today.year
        es_month = today.month
        day = 1
        first_date = datetime.datetime(es_year, es_month, day)
        first_date = str(first_date)
        search_domain = [('create_date', '>=', first_date)]
        order = 'create_date DESC'
        c_record = self.env['agf.screening'].search(search_domain, order=order, limit=1)
        l_record = self.env['agf.screening'].search(search_domain, order=order, limit=2)
        record = l_record - c_record
        for es in self:
            if record.exists():
                es.number_in_month = record.number_in_month + 1
            else:
                es.number_in_month = 1