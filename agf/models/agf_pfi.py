# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.translate import _


class PFI(models.Model):

    _inherit = 'res.partner'

    pfi_type = fields.Selection(
        [('Commercial Bank', 'Commercial Bank'), ('Non-Bank Financial Institution', 'Non-Bank Financial Institution')])
#    status = fields.Selection([('Live', 'Live'), ('Expired', 'Expired'), ('Prospecting', 'Prospecting')])
    agfcountry_id = fields.Many2one('agf.country', tracking=True ,string='Country/Region', index=True)
    region = fields.Char('Region')
    sub_region = fields.Char('Sub-Region')
    description = fields.Text()
#    structuring_list = fields.One2many('crm.lead', 'partner_id', string = 'Structuring', domain=[('type', '=', 'opportunity')])
#    user_id = fields.Many2one('res.users', string='Assigned To', tracking=True, index=True)
    affiliation_level = fields.Selection([('Group', 'Group'), ('Affiliate', 'Affiliate'), ('Autonomous', 'Autonomous')], string='Affiliation Level')
#    expiration_date = fields.Date('Expiration Date', tracking=True)
#    signature_date = fields.Date('Signature Date')
#   structurable = fields.Boolean('Structurable', default=False, tracking=True)
#    agfdoc = fields.One2many('agfdoc.mydoc', 'pfi_list')
    structuring_ids = fields.One2many('crm.lead', 'partner_id', string='Opportunities', domain=[('type', '=', 'opportunity')])
    prospecting_ids = fields.One2many('crm.lead', 'partner_id', string='Lead', domain=[('type', '=', 'lead')])
    final_tier = fields.Char('Final Tier')
    p_lig = fields.Char('LIG')
    p_lpg = fields.Char('LPG')
    p_bfrg = fields.Char('BFRG')


    def _onchange_agfcountry_id_values(self, agfcountry_id):
        if agfcountry_id:
            agfcountry = self.env['agf.country'].browse(agfcountry_id)
            region = agfcountry.region
            sub_region = agfcountry.sub_region
            return {
                'region': region,
                'sub_region': sub_region,
            }
        return {}


    @api.onchange('agfcountry_id')
    def _onchange_agfcountry_id(self):
        values = self._onchange_agfcountry_id_values(self.agfcountry_id.id if self.agfcountry_id else False)
        self.update(values)

#@api multi
    def _compute_company_type(self):
        for record in self:
            res = super(PFI, record)._compute_company_type()
            record.company_type = "company"
            record.is_company = True
            return res