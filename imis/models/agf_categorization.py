# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools, SUPERUSER_ID
from odoo.tools.translate import _
from odoo.exceptions import UserError, AccessError


class agfScreening(models.Model):
    _name = 'agf.categorization'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin', 'format.address.mixin']
    _description = 'E&S Categorization'


    name = fields.Char(string="Name of the Borrower", tracking=True)
    screening_ids = fields.One2many('agf.screening', 'categorization_id')
    #screening related fields
    guarantee_party = fields.Char(string='Guarantee Party', tracking=True)
    types_of_institution = fields.Char(string='Type of institution', tracking=True)
    es_country = fields.Many2one('agf.country', string='country', tracking=True)
    #risk response
    executed_by = fields.Char("Excuted by (Risk Manager)", tracking=True)
    executed_date = fields.Char("Executed on (Risk Manager)", tracking=True)
    product_type = fields.Char("Product Type", tracking=True)
    category = fields.Char("Category", tracking=True)
    es_category = fields.Char("ES Category", tracking=True)
    es_due_dilligence = fields.Char("Due Dilligence", tracking=True)
    summary_of_tasks = fields.Char()
    summary_tasks = fields.Many2many('agf.screening.task', compute='_compute_summary_of_tasks', string='Summary of task', tracking=True)
    comments = fields.Text("Comments", tracking=True)

    @api.depends('summary_of_tasks')
    def _compute_summary_of_tasks(self):
        for rec in self:
            if rec.summary_of_tasks:
                values = []
                list_task = rec.summary_of_tasks.split(',')
                for task in list_task:
                    search_domain = [('name', '=', task)]
                    task_obj = self.env['agf.screening.task'].search(search_domain, order='id', limit=1)
                    if not task_obj:
                        task_obj = self.env['agf.screening.task'].sudo().create({
                            'name': task
                        })
                    values.append(task_obj.id)
                rec.summary_tasks = [(6, 0, values)]

