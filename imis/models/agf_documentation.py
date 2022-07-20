# -*- coding: utf-8 -*-

import base64
from odoo import models, fields, api
from odoo.tools.translate import _

# class agfdoc(models.Model):
#     _name = 'agfdoc.agfdoc'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

class AgfDocumentation(models.Model):

	_name = 'agf.documentation'

	name = fields.Char('Document')
#	description = fields.Text()
#	nature = fields.Selection([('hard','Hard'), ('soft','Soft')], string="Nature")
#	pfi_relation = fields.Selection([('PFI','PFI'),('Lead/Structuring','Lead/Structuring')], string="Document Master")
#	pfi_list = fields.Many2one('res.partner', domain="[('company_type', '!=', 'company')]", string="select a PFI")
	structuring_id = fields.Many2one('crm.lead', string='Opportunities')
#	status = fields.Selection([('received','Received'), ('delayed','Delayed'), ('missing','Missing')], string="Status")
	stage = fields.Selection([('raac','RAAC'),('pre raac','Pre RAAC'),('dd','DD'),('rm','RM'),('raac and dd','RAAC and DD'),('cao','CAO'),('finance','Finance'),('post agreement','Post Agreement Signing'),('ut','UT'),('claim','Claim')], string="Stage")
#	version = fields.Float('Version')
#	document_code = fields.Char('code')
	attachment_ids = fields.Many2many('ir.attachment', string="Attachments")
	section_subfolder_ids = fields.Many2one('agf.documentation.section.subfolder')
	section_content_ids = fields.Many2one('agf.documentation.sections')
	timing = fields.Selection([('Pre Obligation','Pre Obligation'),('Post Obligation','Post Obligation')], string="Timing")
	comment = fields.Selection([('PLI Document','PLI Document'),('AGF Document','AGF Document')], string='Comment')

#	@api.onchange('doc_master')
#	def _initialize_value(self):
#		self.pfi_list = None
#		self.structuring_list = None



class doc_section(models.Model):
	_name = 'agf.documentation.sections'
	_order = 'section, section_contents'
	_rec_name = 'section_contents'

	section = fields.Many2one('agf.documentation.section.subfolder')
	section_contents = fields.Many2one('agf.documentation.section.contents')

class sectioncontents(models.Model):
	_name = 'agf.documentation.section.subfolder'

	name = fields.Char('Section / Subfolder')

class sectioncontents(models.Model):
	_name = 'agf.documentation.section.contents'

	name = fields.Char('Section Contents')
