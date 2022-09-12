# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools
from odoo.tools import ustr


class GuaranteeIssuance(models.Model):

    _name = 'agf.issuance'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin', 'format.address.mixin']

    name = fields.Char('Name')
    stage_id = fields.Many2one('agf.issuance.stage', string='Stage', default=lambda self: self._default_stage_id())
    approval_id = fields.Many2one('agf.approval', string='Approved Guarantee')
    guarantee_party = fields.Char('Guarantee Party')
    country = fields.Char(string='Country')
    guarantee_product = fields.Char(string='Guarantee Product')
    smi = fields.Char('SMI')
    currency = fields.Char(string='Currency of Exposure')
    guarantee_amount = fields.Float('Guarantee Amount (LC)')
    guarantee_amount_usd = fields.Float('Guarantee Amount (USD)')
    guarantee_tenor = fields.Char('Guarantee Tenor', tracking=True)
    welcome_letter = fields.Binary('Welcome Letter')
    draft_gaf = fields.Many2many('ir.attachment')
    final_gaf = fields.Binary('Final Guarantee Agreement File')

    def _onchange_approval_values(self, approval_id):
        if approval_id:
            approval = self.env['agf.approval'].browse(approval_id)
            stage = self.env['agf.issuance.stage'].browse(self.stage_id)
            approval_name = approval.name
            stage_name = 'Issuance for'
            name = ustr(stage_name or '') + ' - ' + ustr(approval_name or '')
            guarantee_party = approval.guarantee_party
            country = approval.country
            guarantee_tenor = approval.guarantee_tenor
            guarantee_product = approval.guarantee_product
            currency = approval.currency
            guarantee_amount = approval.guarantee_amount
            guarantee_amount_usd = approval.guarantee_amount_usd
            smi = approval.smi
            return {
                'name': name,
                'guarantee_party': guarantee_party,
                'currency': currency,
                'country': country,
                'guarantee_tenor': guarantee_tenor,
                'guarantee_product': guarantee_product,
                'guarantee_amount': guarantee_amount,
                'guarantee_amount_usd': guarantee_amount_usd,
                'smi': smi,
            }
        return {}

    @api.onchange('approval_id')
    def _onchange_approval(self):
        values = self._onchange_approval_values(self.approval_id.id if self.approval_id.id else False)
        self.update(values)

    def _default_stage_id(self):
        return self._stage_find(domain=[('fold', '=', False)]).id

    # ----------------------------------------
    # Business Methods
    # ----------------------------------------

    def _stage_find(self, team_id=False, domain=None, order='sequence'):
        """ Determine the stage of the current lead with its teams, the given domain and the given team_id
            :param team_id
            :param domain : base search domain for stage
            :returns crm.stage recordset
        """
        # collect all team_ids by adding given one, and the ones related to the current leads
        search_domain = [('team_id', '=', False)]
        # AND with the domain in parameter
        if domain:
            search_domain += list(domain)
        # perform search, return the first found
        return self.env['crm.stage'].search(search_domain, order=order, limit=1)



class ApprovalStage(models.Model):

    _name = 'agf.issuance.stage'
    _order = 'sequence, id'

    name = fields.Char('Name')
    sequence = fields.Integer('Sequence', default=10)
    team_id = fields.Many2one('crm.team', string='Team')
    fold = fields.Boolean('Folded in Pipeline', help='This stage is folded in the kanban view when there are no records in that stage to display.')

    @api.model
    def default_get(self, fields):
        """ Hack :  when going from the pipeline, creating a stage with a sales team in
            context should not create a stage for the current sales channel only
        """
        ctx = dict(self.env.context)
        if ctx.get('default_team_id') and not ctx.get('crm_team_mono'):
            ctx.pop('default_team_id')
        return super(ApprovalStage, self.with_context(ctx)).default_get(fields)



