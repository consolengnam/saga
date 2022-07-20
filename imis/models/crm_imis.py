# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools, SUPERUSER_ID
from odoo.tools.translate import _
from odoo.exceptions import UserError, AccessError

CRM_LEAD_FIELDS_TO_MERGE = [
    'name',
    'partner_id',
    'campaign_id',
    'company_id',
    'agfcountry_id',
    'region',
    'sub_region',
    'team_id',
    'stage_id',
    'medium_id',
    'source_id',
    'user_id',
    'title',
    'city',
    'contact_name',
    'description',
    'mobile',
    'partner_name',
    'phone',
    'probability',
    'planned_revenue',
    'street',
    'create_date',
    'date_action_last',
    'email_from',
    'email_cc',
    'website',
    'partner_name']

class imis_crm(models.Model):

    _inherit = 'crm.lead'

    product_types = fields.Many2many('crm.imis.product.type', string='Product Types')
    requested_amount = fields.Float('Requested Amount (in LoR)', tracking=True)
    expected_guarantee_amount = fields.Float('Expected Guarantee Amount', tracking=True)
    #fields redefinition
    planned_revenue = fields.Float('Considered Amount USD', tracking=True)
    #-------------------
    considered_amount = fields.Float('Considered Amount LC(AGF)')
    lor_received_date = fields.Date('LOR Received Date', tracking=True)
    its_date = fields.Date('ITS Date', tracking=True)
    user_assigned_on = fields.Date()
    signed_date = fields.Date('Signed Date')
    country_risk = fields.Float('Country Risk', tracking=True)
    borrow_risk = fields.Float('Borrow Risk', tracking=True)
    transaction_risk = fields.Char('Transaction', tracking=True)
    lender_risk = fields.Float('Lender Risk', tracking=True)
    guarantee_tenor = fields.Char('Guarantee Tenor', tracking=True)
    warf = fields.Char('WARF', tracking=True)
    agfdoc_ids = fields.One2many('agf.documentation', 'structuring_id', string='Document', tracking=True)
    risk_currency = fields.Char('Risk Currency', tracking=True)

    # field regarding the prospect
    lead_type = fields.Selection([
        ('commercial_bank', 'Commercial Bank'),
        ('non_bank_financial_institution', 'Non Bank Financial Institution'),
        ('dfi', 'DFI'),
        ('micro_finance institution', 'Micro Finance Institution'),
        ('other', 'Other')])
    lead_reco = fields.Many2one('res.users', string='Originator', index=True, tracking=True,
                                default=lambda self: self.env.user)
    lead_source = fields.Selection([
        ('cold_call', 'Cold Call'),
        ('existing_customer', 'Existing Customer'),
        ('self_generated', 'Self Generated'),
        ('employee', 'Employee'),
        ('partner', 'Partner'),
        ('public_relations', 'Public Relations'),
        ('direct_mail', 'Direct Mail'),
        ('conference', 'Conference'),
        ('trade_show', 'Trade Show'),
        ('web_site', 'Web Site'),
        ('word_of_mouth', 'Word of Mouth'),
        ('other', 'Other')])
    lead_status = fields.Selection([
        ('new', 'New'),
        ('loig', 'LOIG Sent'),
        ('nda_sent', 'NDA sent'),
        ('nda_reviewing', 'NDA reviewing'),
        ('lor_received', 'LoR received'),
        ('lost', 'Lost')])
    date_open = fields.Datetime('Created On', readonly=True, default=fields.Datetime.now)
    lead_receipt_date = fields.Date('Lead Receipt Date')
    response_deadline_date = fields.Date('Response Deadline', store=True)
    assigned_to = fields.Many2one('res.users', string='Assigned To', tracking=True, index=True,
                                  default=lambda self: self.env.user)
    agfcountry_id = fields.Many2one('agf.country', string='Country/Region', index=True)
    region = fields.Char('Region')
    sub_region = fields.Char('Sub-Region')
    guarantee_product = fields.Many2one('crm.imis.product',
                                         string='Guarantee Product')

    # specific structuring fields
    timeline_signing = fields.Selection([
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December'),
        ('FY 2020', 'FY 2020'),
        ('Dropped', 'Dropped')])
    timeline_approval = fields.Selection([
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December'),
        ('FY 2020', 'FY 2020'),
        ('Dropped', 'Dropped')])
    product = fields.Selection([('LIG', 'LIG'), ('LPG', 'LPG'), ('EG', 'EG'), ('BFRG', 'BFRG')])
    types = fields.Selection([('Green', 'Green'), ('Brown', 'Brown')])
    classification = fields.Selection([('Billable', 'Billable'), ('Not Billable', 'Not Billable')])
    smi = fields.Char('SMI')
    next_step = fields.Char('Next Step')
    campaign_source = fields.Selection(
        [('Sources 1', 'Sources 1'), ('Sources 2', 'Sources 2'), ('Sources 3', 'Sources 3'),
         ('Sources 4', 'Sources 4')])
    agreement_number = fields.Char('Agreement Number')
    technology = fields.Selection(
        [('sustainable energy', 'Sustainable Energy'), ('cleaner production', 'Cleaner Production')])
    agfcurrency = fields.Many2one('agf.usdrate', string='Currency')
    rate = fields.Float(related='agfcurrency.rate', string="Rate")
#    amount_lc = fields.Float(string="Amount(LC)")

    # tiering compute
    final_tier = fields.Char("Final Tier", compute='_compute_final_tier')
    p_lig = fields.Char("LIG", compute='_compute_p_lig')
    p_lpg = fields.Char("LPG", compute='_compute_p_lpg')
    p_bfrg = fields.Char("BFRG", compute='_compute_p_bfrg')

    raac_validation = fields.Char(string='RAAC validation by Risk', default='N/A', tracking=True)
    dd_validation = fields.Char(string='Credit Paper Validation By Risk', default='N/A', tracking=True)
    officer_email = fields.Char(compute='_compute_officer_mail', store=True)

    # E&S Screening page fields
    screening_ids = fields.One2many('agf.screening', 'opportinuty_id', string='ES screening Activities')
#    name_of_borrower = fields.Char("Name of the Borrower")
#    guarantee_identifier = fields.Char("Guarantee Identifier")
#    types_of_institution = fields.Selection([('financial_institution','Financial Institution'),('sme','SME'),('corporate','Corporate')])
#    co_guarantor = fields.Char("Co-Guarantor")
#    executed_by = fields.Many2one('res.users', string='Salesperson', index=True, tracking=True, default=lambda self: self.env.user)
#    es_country = fields.Many2one('agf.country')
#    es_date = fields.Date('Date')
#    es_activities = fields.Selection([('yes','Yes'),('no','No')])
#    es_activities_reason = fields.Text()


    def _onchange_partner_id_values(self, partner_id):
        """ returns the new values when partner_id has changed """
        if partner_id:
            partner = self.env['res.partner'].browse(partner_id)

            partner_name = partner.parent_id.name
            if not partner_name and partner.is_company:
                partner_name = partner.name

            return {
                'partner_name': partner_name,
                'contact_name': partner.name if not partner.is_company else False,
                'title': partner.title.id,
                'street': partner.street,
                'city': partner.city,
                'agfcountry_id': partner.agfcountry_id.id,
                'region': partner.region,
                'sub_region': partner.sub_region,
                'email_from': partner.email,
                'phone': partner.phone,
                'mobile': partner.mobile,
                'function': partner.function,
                'website': partner.website,
            }
        return {}

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        values = self._onchange_partner_id_values(self.partner_id.id if self.partner_id else False)
        self.update(values)

#@api multi
    def _create_lead_partner_data(self, name, is_company, parent_id=False):
        """ extract data from lead to create a partner
            :param name : furtur name of the partner
            :param is_company : True if the partner is a company
            :param parent_id : id of the parent partner (False if no parent)
            :returns res.partner record
        """
        email_split = tools.email_split(self.email_from)
        return {
            'name': name,
            'user_id': self.env.context.get('default_user_id') or self.user_id.id,
            'comment': self.description,
            'team_id': self.team_id.id,
            'parent_id': parent_id,
            'phone': self.phone,
            'mobile': self.mobile,
            'email': email_split[0] if email_split else False,
            'title': self.title.id,
            'function': self.function,
            'street': self.street,
            'city': self.city,
            'agfcountry_id': self.agfcountry_id.id,
            'region': self.region,
            'sub_region': self.sub_region,
            'website': self.website,
            'is_company': is_company,
            'type': 'contact',
        }

    # ----------------------------------------
    # AGF country/region redefinition
    # ----------------------------------------

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

    # ----------------------------------------
    # Convert amount into local amount
    # ----------------------------------------

    def _convert_local_currency(self, considered_amount, rate):
        if considered_amount and rate != 0.00:
            planned_revenue = self.considered_amount / self.rate
            return {
                'planned_revenue': planned_revenue
            }
        return {}

    @api.onchange('considered_amount', 'rate')
    def _onchange_amount(self):
        values = self._convert_local_currency(self.considered_amount if self.considered_amount else False, self.rate if self.rate != 0 else False)
        self.update(values)


    def _change_currency_id(self, agfcurrency):
        if agfcurrency:
            agf_currency = self.env['agf.usdrate'].browse(agfcurrency)
            rate = agf_currency.rate
            return {
                'rate': rate,
            }
        return {}

    @api.depends('agfcurrency')
    def _onchange_currency(self):
        values = self._change_currency_id(self.agfcurrency.id if self.agfcurrency else False)
        self.update(values)

    @api.depends('partner_id')
    def _compute_final_tier(self):
        for lead in self:
            lead.final_tier = lead.partner_id.final_tier

    @api.depends('partner_id')
    def _compute_p_lig(self):
        for lead in self:
            lead.p_lig = lead.partner_id.p_lig

    @api.depends('partner_id')
    def _compute_p_lpg(self):
        for lead in self:
            lead.p_lpg = lead.partner_id.p_lpg

    @api.depends('partner_id')
    def _compute_p_bfrg(self):
        for lead in self:
            lead.p_bfrg = lead.partner_id.p_bfrg

    @api.depends('user_id')
    def _compute_officer_mail(self):
        for officer in self:
            officer.officer_email = officer.user_id.email


#@api multi
    def _merge_notify(self, opportunities):
        """ Create a message gathering merged leads/opps informations. Using message_post, send a
            message explaining which fields has been merged and their new value. `self` is the
            resulting merge crm.lead record.
            :param opportunities : recordset of merged crm.lead
            :returns mail.message posted on resulting crm.lead
        """
        # TODO JEM: mail template should be used instead of fix body, subject text
        self.ensure_one()
        # mail message's subject
        result_type = opportunities._merge_get_result_type()
        merge_message = _('Merged leads') if result_type == 'lead' else _('Merged opportunities')
        subject = merge_message + ": " + ", ".join(opportunities.mapped('name'))
        # message bodies
        message_bodies = opportunities._mail_body(list(CRM_LEAD_FIELDS_TO_MERGE))
        message_body = "\n\n".join(message_bodies)
        return self.message_post(body=message_body, subject=subject)

#@api multi
    def _merge_opportunity_history(self, opportunities):
        """ Move mail.message from the given opportunities to the current one. `self` is the
            crm.lead record destination for message of `opportunities`.
            :param opportunities : recordset of crm.lead to move the messages
        """
        self.ensure_one()
        for opportunity in opportunities:
            for message in opportunity.message_ids:
                message.write({
                    'res_id': self.id,
                    'subject': _("From %s : %s") % (opportunity.name, message.subject)
                })
        return True

#@api multi
    def _merge_opportunity_attachments(self, opportunities):
        """ Move attachments of given opportunities to the current one `self`, and rename
            the attachments having same name than native ones.
            :param opportunities : recordset of merged crm.lead
        """
        self.ensure_one()

        # return attachments of opportunity
        def _get_attachments(opportunity_id):
            return self.env['ir.attachment'].search([('res_model', '=', self._name), ('res_id', '=', opportunity_id)])

        first_attachments = _get_attachments(self.id)
        # counter of all attachments to move. Used to make sure the name is different for all attachments
        count = 1
        for opportunity in opportunities:
            attachments = _get_attachments(opportunity.id)
            for attachment in attachments:
                values = {'res_id': self.id}
                for attachment_in_first in first_attachments:
                    if attachment.name == attachment_in_first.name:
                        values['name'] = "%s (%s)" % (attachment.name, count)
                count += 1
                attachment.write(values)
        return True

#@api multi
    def merge_dependences(self, opportunities):
        """ Merge dependences (messages, attachments, ...). These dependences will be
            transfered to `self`, the most important lead.
            :param opportunities : recordset of opportunities to transfert. Does
                not include `self`.
        """
        self.ensure_one()
        self._merge_notify(opportunities)
        self._merge_opportunity_history(opportunities)
        self._merge_opportunity_attachments(opportunities)

#@api multi
    def merge_opportunity(self, user_id=False, team_id=False):
        """ Merge opportunities in one. Different cases of merge:
                - merge leads together = 1 new lead
                - merge at least 1 opp with anything else (lead or opp) = 1 new opp
            The resulting lead/opportunity will be the most important one (based on its confidence level)
            updated with values from other opportunities to merge.
            :param user_id : the id of the saleperson. If not given, will be determined by `_merge_data`.
            :param team : the id of the sales channel. If not given, will be determined by `_merge_data`.
            :return crm.lead record resulting of th merge
        """
        if len(self.ids) <= 1:
            raise UserError(_('Please select more than one element (lead or opportunity) from the list view.'))

        # Sorting the leads/opps according to the confidence level of its stage, which relates to the probability of winning it
        # The confidence level increases with the stage sequence, except when the stage probability is 0.0 (Lost cases)
        # An Opportunity always has higher confidence level than a lead, unless its stage probability is 0.0
        def opps_key(opportunity):
            sequence = -1
            if opportunity.stage_id.on_change:
                sequence = opportunity.stage_id.sequence
            return (sequence != -1 and opportunity.type == 'opportunity'), sequence, -opportunity.id
        opportunities = self.sorted(key=opps_key, reverse=True)

        # get SORTED recordset of head and tail, and complete list
        opportunities_head = opportunities[0]
        opportunities_tail = opportunities[1:]

        # merge all the sorted opportunity. This means the value of
        # the first (head opp) will be a priority.
        merged_data = opportunities._merge_data(list(CRM_LEAD_FIELDS_TO_MERGE))

        # force value for saleperson and sales channel
        if user_id:
            merged_data['user_id'] = user_id
        if team_id:
            merged_data['team_id'] = team_id

        # merge other data (mail.message, attachments, ...) from tail into head
        opportunities_head.merge_dependences(opportunities_tail)

        # check if the stage is in the stages of the sales channel. If not, assign the stage with the lowest sequence
        if merged_data.get('team_id'):
            team_stage_ids = self.env['crm.stage'].search(['|', ('team_id', '=', merged_data['team_id']), ('team_id', '=', False)], order='sequence')
            if merged_data.get('stage_id') not in team_stage_ids.ids:
                merged_data['stage_id'] = team_stage_ids[0].id if team_stage_ids else False

        # write merged data into first opportunity
        opportunities_head.write(merged_data)

        # delete tail opportunities
        # we use the SUPERUSER to avoid access rights issues because as the user had the rights to see the records it should be safe to do so
        opportunities_tail.sudo().unlink()

        return opportunities_head


    # -----------------------------------------------------------
    #         Redefining Convertion Function
    # -----------------------------------------------------------
#@api multi
    def _convert_opportunity_data(self, customer, team_id=False):
        """ Extract the data from a lead to create the opportunity
            :param customer : res.partner record
            :param team_id : identifier of the sales channel to determine the stage
        """
        if not team_id:
            team_id = self.team_id.id if self.team_id else False
        value = {
            'probability': self.probability,
            'name': self.name,
            'partner_id': customer.id if customer else False,
            'type': 'opportunity',
            'date_open': fields.Datetime.now(),
            'email_from': customer and customer.email or self.email_from,
            'phone': customer and customer.phone or self.phone,
            'date_conversion': fields.Datetime.now(),
        }
        if not self.stage_id:
            stage = self._stage_find(team_id=team_id)
            value['stage_id'] = stage.id
            if stage:
                value['probability'] = stage.probability
        return value

    # -----------------------------------------------------------
    #         Stage Button Action
    # -----------------------------------------------------------
# @api multi
    def action_go_to_dropped(self):
        for lead in self:
            lead.write({'stage_id': 2})
        return True

#@api multi
    def action_go_to_raac(self):
        for lead in self:
            lead.write({'stage_id': 3})
        return True

#@api multi
    def action_go_to_dd(self):
        for lead in self:
            lead.write({'stage_id': 4})
        return True

#@api multi
    def action_go_to_approval(self):
        for lead in self:
            lead.write({'stage_id': 5})
        return True

#@api multi
    def action_go_to_ayts(self):
        for lead in self:
            lead.write({'stage_id': 6})
        return True

#@api multi
    def action_go_to_as(self):
        for lead in self:
            lead.write({'stage_id': 7})
        return True

    #--------------------------------------------------------------
    #              Notify Risk
    #--------------------------------------------------------------
#@api multi
    def action_notify_risk(self):
        '''
        This function opens a window to compose an email, with the edi sale template message loaded by default
        '''
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('agf', 'mail_template_agf_notification_risk')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = {
            'default_model': 'crm.lead',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }