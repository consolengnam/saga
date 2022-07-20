# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools
from odoo.tools import ustr
from odoo.tools.translate import _


class guarantee_approval(models.Model):

    _name = 'agf.approval'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin', 'format.address.mixin']

    name = fields.Char(string='Guarantee Approval', tracking=True)
    stage = fields.Selection([('LGC','LGC'),('GC','GC'),('Board','Board')], string='Stage', tracking=True, default='LGC')
    structuring = fields.Many2one('crm.lead', string='Structuring', tracking=True)
    guarantee_party = fields.Char(compute='_compute_approval_fields', string='Guarantee Party', store=True)
    country = fields.Char(compute='_compute_approval_fields', store=True, string='Country')
    guarantee_product = fields.Char(compute='_compute_approval_fields', store=True, string='Guarantee Product')
    currency = fields.Char(compute='_compute_approval_fields', store=True, string='Currency of Exposure')
    risk_currency = fields.Char('Risk Currency')
    guarantee_amount = fields.Float(compute='_compute_approval_fields', store=True, string='Guarantee Amount')
    guarantee_amount_usd = fields.Float(compute='_compute_approval_fields', store=True, string='Guarantee Amount USD')
    rate = fields.Float(compute='_compute_approval_fields', store=True, string='Rate')
    guarantee_tenor = fields.Char('Guarantee Tenor', tracking=True)
    warf = fields.Char(compute='_compute_approval_fields', store=True, string='WARF', tracking=True)
    executive_summary = fields.Html('Executive Summary', tracking=True)
    approval_files = fields.Many2many('ir.attachment', string='Approval Files', tracking=True)
    lgc_started_on = fields.Date('Date', tracking=True)
    gc_started_on = fields.Date('Date', tracking=True)
    board_started_on = fields.Date('Date', tracking=True)
    lgc_final_status = fields.Selection([('approved','Approved'),('aproved_with_comment','Approved with comments'),('recommended','Recommended for next stage'),('rejected','Rejected')], string='Final Status', tracking=True)
    gc_final_status = fields.Selection([('approved','Approved'),('aproved_with_comment','Approved with comments'),('recommended','Recommended for next stage'),('rejected','Rejected')], string='Final Status', tracking=True)
    board_final_status = fields.Selection([('approved','Approved'),('aproved_with_comment','Approved with comments'),('recommended','Recommended for next stage'),('rejected','Rejected')], string='Final Status', tracking=True)
    approver_gc_ids = fields.One2many('agf.approber', 'gc_approval_id', string='Approber', tracking=True)
    approver_board_ids = fields.One2many('agf.approber', 'board_approval_id', string='Approber', tracking=True)
    minutes_lgc = fields.Binary('Minutes of LGC', tracking=True)
    smi = fields.Char(compute='_compute_approval_fields', store=True, string='SMI')
#    list_gc_voters = fields.Many2many('res.users')

    @api.depends('structuring')
    def _compute_approval_fields(self):
        for record in self:
            if record.structuring:
                record.guarantee_party = record.structuring.partner_id.name
                record.country = record.structuring.partner_id.agfcountry_id.name.name
                record.guarantee_product = record.structuring.guarantee_product.name
                record.currency = record.structuring.agfcurrency.name
                record.rate = record.structuring.rate
                record.guarantee_amount = record.structuring.considered_amount
                record.guarantee_amount_usd = record.structuring.planned_revenue
                record.smi = record.structuring.smi
                record.warf = record.structuring.warf

    def _onchange_structuring_values(self, structuring):
        if structuring:
            opportunity = self.env['crm.lead'].browse(structuring)
            stage_name = dict(self._fields['stage'].selection).get(self.stage)
            structuring_name = opportunity.name
            name = 'Approval for "' + ustr(structuring_name or '') + '"'
            return {
                'name': name,
            }
        return {}

    @api.onchange('structuring')
    def _onchange_structuring(self):
        values = self._onchange_structuring_values(self.structuring.id if self.structuring else False)
        self.update(values)

    #----------------------------------------------------------
    #                List of voters ids/stage
    #----------------------------------------------------------
#    @api.multi
#    def _get_voters_list(self):
#        for approval in self:
#            self.list_gc_voters = vote.approver.id
#            approval.approver_gc_ids = [(0,0, vote.id)]
#
#
#        vote_gc = self.env['agf.approber'].search([('gc_approval_id', '=', self.id)])

#@api multi
    def open_vote(self):
        vote = []
        if self.stage == 'GC':
            vote = self.env['agf.approber'].search([('gc_approval_id', '=', self.id),('approver', '=', self.env.uid)])
            if vote:
                return {
                    'name': _('Vote'),
                    'res_model': 'agf.approber',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_id': vote.id,
                    'views': [(False, 'form'), ],
                    'type': 'ir.actions.act_window',
                    'target': 'new',
                    'context': {'default_gc_approval_id': self.id}
                }
            else:
                return {
                    'name': _('Vote'),
                    'res_model': 'agf.approber',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'views': [(False, 'form'), ],
                    'type': 'ir.actions.act_window',
                    'target': 'new',
                    'context': {'default_gc_approval_id': self.id}
                }
        elif self.stage == 'Board':
            vote = self.env['agf.approber'].search(
                [('board_approval_id', '=', self.id), ('approver', '=', self.env.uid)])
            if vote:
                return {
                    'name': _('Vote'),
                    'res_model': 'agf.approber',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_id': vote.id,
                    'views': [(False, 'form'), ],
                    'type': 'ir.actions.act_window',
                    'target': 'new',
                    'context': {'default_board_approval_id': self.id}
                }
            else:
                return {
                    'name': _('Vote'),
                    'res_model': 'agf.approber',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'views': [(False, 'form'), ],
                    'type': 'ir.actions.act_window',
                    'target': 'new',
                    'context': {'default_board_approval_id': self.id}
                }
        else:
            return False
