import logging
from typing import List, Tuple

from odoo import _, models, fields, api
from datetime import datetime
from odoo.osv import expression

from odoo.exceptions import except_orm, Warning, RedirectWarning, ValidationError


_logger = logging.getLogger(__name__)


IN_PFI_DOCUMENT_UPLOADED_STATE = '10000'      #'In Assessment Initiation'
NON_APPLICABLE = 'N/A'
APPLICATION_PREFIXE_NUMBER = 'AGF'
LEFT_PADDING_CHARACTER = '0'
TOTAL_CHARACTER = 4


class RiskModelWorkflow(models.Model):
    _name = 'risk.model.workflow'
    _description = 'Risk Engine Workflow '
    _rec_name = 'model_application_number'
    _order = 'id desc'

    _inherit = ['mail.thread.cc',
                'mail.thread.blacklist',
                'mail.activity.mixin',
                'format.address.mixin',
                ]

    _primary_email = 'email_from'

    _sql_constraints = [
        ('model_name_uniq', 'UNIQUE(model_application_name,risk_workflow_id)', 'This application number already exist. Please contact your administrator')
    ]

    model_application_number = fields.Char(string='Application N°', required=True , default='1')
    model_workflow_description = fields.Text(string='Model Workflow Description')
    status = fields.Selection([('1', 'Active'), ('2', 'Inactive')], required=True, default='1')

    email_from = fields.Char(
        'Email', tracking=40, index=True, readonly=False, store=True)

    # email_from = fields.Char(
    #     'Email', tracking=40, index=True,
    #     compute='_compute_email_from', inverse='_inverse_email_from', readonly=False, store=True)
    #
    # @api.depends('partner_id.email')
    # def _compute_email_from(self):
    #     for lead in self:
    #         if lead.partner_id.email and lead._get_partner_email_update():
    #             lead.email_from = lead.partner_id.email
    #
    # def _inverse_email_from(self):
    #     for lead in self:
    #         if lead._get_partner_email_update():
    #             lead.partner_id.email = lead.email_from

    phone = fields.Char('Phone', tracking=50 , readonly=False, store=True)

    # phone = fields.Char(
    #     'Phone', tracking=50,
    #     compute='_compute_phone', inverse='_inverse_phone', readonly=False, store=True)
    #
    # @api.depends('partner_id.phone')
    # def _compute_phone(self):
    #     for lead in self:
    #         if lead.partner_id.phone and lead._get_partner_phone_update():
    #             lead.phone = lead.partner_id.phone
    #
    # def _inverse_phone(self):
    #     for lead in self:
    #         if lead._get_partner_phone_update():
    #             lead.partner_id.phone = lead.phone



    def _default_stage_id(self):
        default_risk_workflow = self._context.get('default_type_workflow')
        risk_workflow_approval_structure_env = self.env['risk.workflow.approval.structure']
        return risk_workflow_approval_structure_env.get_start_event(default_risk_workflow)

    @api.model
    def _group_expand_stages(self, stages, domain, order):
        return stages.search([], order=order)

    stage_id = fields.Many2one(
        'risk.stage', string='Status', index=True, readonly=True,
        store=True, copy=False,
        default=_default_stage_id,
        group_expand='_group_expand_stages'
    )


    def _default_risk_workflow_id(self):
        default_risk_workflow = self._context.get('default_type_workflow')
        risk_workflow_env = self.env['risk.workflow']
        return risk_workflow_env.get_workflow(default_risk_workflow)

    risk_workflow_id = fields.Many2one('risk.workflow', string="Workflow",  default=_default_risk_workflow_id)

    # type_workflow = fields.Selection([
    #     ('WF001', 'Managment of risk'),], string='Type Workflow', required=True, default='WF001')

    type_workflow = fields.Char(string='Type workflow', related='risk_workflow_id.code', Store=True)

    movement_ids = fields.One2many('risk.movement', 'risk_model_workflow_id' , string='Action Log')
    last_movement_id = fields.Many2one('risk.movement', string="Last movement")

    position_id = fields.Many2one('hr.job', string="Current position")

    check_position = fields.Boolean(compute='_compute_check_position')

    @api.depends('check_position')
    def _compute_check_position(self):
        risk_workflow_approval_structure = self.env['risk.workflow.approval.structure']
        for rec in self:
            rec.check_position = self.get_position(self) and not risk_workflow_approval_structure.is_end_event(self.stage_id.id, self.risk_workflow_id.id)

    def get_position(self, risk_model_workflow):

        position = False
        employee_id = self.env.user.employee_id
        for rec in risk_model_workflow:
            position = (employee_id.job_id.id == rec.position_id.id)
        return position

    check_cancel_position = fields.Boolean(compute='_compute_check_cancel_position')

    @api.depends('check_cancel_position')
    def _compute_check_cancel_position(self):
        risk_workflow_approval_structure = self.env['risk.workflow.approval.structure']
        for rec in self:
            rec.check_cancel_position = self.get_cancel_position(self) and not risk_workflow_approval_structure.is_end_event(self.stage_id.id, self.risk_workflow_id.id)

    def get_cancel_position(self, risk_model_workflow):

        position = False
        employee_id = self.env.user.employee_id
        for rec in risk_model_workflow:
            movementModel = self.env['risk.movement']
            results_movement = movementModel.search([('id', '=', rec.last_movement_id.id)])
            position = (employee_id.job_id.id != rec.position_id.id) and (
                        employee_id.job_id.id == results_movement.job_transmitter_id.id) and (
                                   rec.date_last_modif == results_movement.date_last_modif)
        return position

    check_return_position = fields.Boolean(compute='_compute_check_return_position')

    @api.depends('check_return_position')
    def _compute_check_return_position(self):
        risk_workflow_approval_structure = self.env['risk.workflow.approval.structure']
        for rec in self:
            rec.check_return_position = self.get_position(self) and not risk_workflow_approval_structure.is_end_event(
                self.stage_id.id, self.risk_workflow_id.id) and not risk_workflow_approval_structure.is_start_event(
                self.stage_id.id, self.risk_workflow_id.id)



    def _default_department_id(self):
        employee_id = self.env.user.employee_id
        return employee_id.department_id.id

    department_id = fields.Many2one('hr.department', string="Department", default=_default_department_id)

    def _default_role_id(self):
        employee_id = self.env.user.employee_id
        return employee_id.job_id.id
    role_id = fields.Many2one('hr.job', string="Role",
                                         domain="[('department_id', '=', department_id)]",
                                         default=_default_role_id)

    tracking_status = fields.Char(string='Tracking Status', related='stage_id.tracking_status')
    process = fields.Char(string='Process', related='risk_workflow_id.name')
    owner_role = fields.Char(string='Owned By', related='role_id.code')

    date_last_modif = fields.Datetime()

    counter = fields.Integer(string='Counter', required=True)
    year = fields.Integer(string='Counter', required=True)
    month = fields.Integer(string='Counter', required=True)





    def get_current_employee(self):
        '''get current employee.'''
        employee = self.env.user.employee_id
        return employee

    def get_application_number(self,new_counter, vals):
        current_time = datetime.now()
        year = current_time.year
        month = current_time.month
        vals['year'] = year
        vals['month'] = month
        return APPLICATION_PREFIXE_NUMBER+str(year).rjust(4, LEFT_PADDING_CHARACTER)+str(month).rjust(2, LEFT_PADDING_CHARACTER)+str(new_counter).rjust(TOTAL_CHARACTER, LEFT_PADDING_CHARACTER)

    @api.model
    def create(self, vals):

        '''Create Action.'''
        employee = self.get_current_employee()
        vals['position_id'] = employee.job_id.id

        counter_model = self.env['risk.counter']

        counter = counter_model.get_current_counter(vals['risk_workflow_id'])

        if  counter:
            new_counter =  counter[1] + 1
            vals['counter'] = new_counter
            vals['model_application_number'] = self.get_application_number(new_counter, vals)




            risk_model_workflow = super(RiskModelWorkflow, self).create(vals)
            department_id = employee.department_id.id

            stage_id = self._default_stage_id()

            if risk_model_workflow:
                id = risk_model_workflow.id
                movement_values = {
                    'risk_model_workflow_id': id,
                    'transmitter_id': department_id,
                    'recipient_id': department_id,
                    'job_transmitter_id': vals['position_id'],
                    'job_recipient_id': vals['position_id'],
                    'comments': NON_APPLICABLE,
                    'user_transmitter_id': False,
                    'date_transmitter': False,
                    'action_name': False,
                    'stage_id': stage_id.id ,
                    'next_stage_id': stage_id.id,
                    'final_status': '1',

                }
                risk_model_workflows_movement_id = self.env['risk.movement'].sudo().create(
                    movement_values
                )

                counter = counter_model.update_current_counter( counter[0] , new_counter)


        else:
            raise ValidationError(_('Unable to create: Please contact your administrator.'))

        return risk_model_workflow

    def write(self, vals):
        '''Update action.'''
        # vals['stage_id'] = self._default_in_process_stage_id()
        if not "date_last_modif" in vals.keys():
            now = datetime.now()
            vals['date_last_modif'] = now
        risk_model_workflow = super(RiskModelWorkflow, self).write(vals)
        return risk_model_workflow

    # def get_last_insert_transaction(self,workflow_id, counter):
    #     results_risk_mode_workflow= self.env['risk.model.workflow'].search(['&', ('workflow_id', '=', workflow_id) , ('counter', '=', counter)] , order='date desc', limit=1)
    #     for result_risk_mode_workflow in results_risk_mode_workflow :
    #         return result_risk_mode_workflow

    def get_last_insert_transaction(self,workflow_id):
        results_risk_mode_workflow= self.env['risk.model.workflow'].search([ ('risk_workflow_id', '=', workflow_id)] , order='id desc', limit=1)
        for result_risk_mode_workflow in results_risk_mode_workflow :
            return result_risk_mode_workflow


    def can_unlink(self):
        check=False
        risk_workflow_approval_structure = self.env['risk.workflow.approval.structure']
        risk_movement= self.env['risk.movement']
        for rec in self:
            #check = rec.get_position(self) and  risk_workflow_approval_structure.is_start_event(rec.stage_id.id, rec.risk_workflow_id.id) and risk_movement.is_delete_movement(rec.id)
            check = rec.get_position(self) and risk_workflow_approval_structure.is_start_event(rec.stage_id.id,  rec.risk_workflow_id.id)
        return check


    def unlink(self):

        '''Delete action'''
        risk_workflow_id = False

        for rec in self:
            risk_workflow_id = rec.risk_workflow_id.id

        result = self.get_last_insert_transaction(risk_workflow_id)
        if result and result.model_application_number == self.model_application_number:
            new_counter = self.counter - 1
            counter_model = self.env['risk.counter']
            counter = counter_model.get_current_counter_id(risk_workflow_id)
            result = counter_model.update_current_counter(counter[0], new_counter)


        for rec in self:
            #if rec.stage_id.code != IN_PFI_DOCUMENT_UPLOADED_STATE:
            if not rec.can_unlink():
                raise ValidationError(_('Unable to delete: Please contact your administrator.'))
            else:
                results_movement = self.env['risk.movement'].search([('risk_model_workflow_id', '=', rec.id)])
                if results_movement:
                    results_movement.unlink()
                results_movement_cancelled = self.env['risk.movement.cancelled'].search(
                    [('risk_model_workflow_id', '=', rec.id)])
                if results_movement_cancelled:
                    results_movement_cancelled.unlink()
        risk_model_workflow = super(RiskModelWorkflow, self).unlink()
        return risk_model_workflow

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        '''Search action.'''

        employee = self.get_current_employee()
        depatments_ids = []
        depatments_ids.append(employee.department_id.id)

        job_ids = []
        job_ids.append(employee.job_id.id)

        args += ['|', ('movement_ids.job_transmitter_id.id', 'in', job_ids),
                 ('movement_ids.job_recipient_id.id', 'in', job_ids)]

        return super(RiskModelWorkflow, self)._search(args, offset, limit, order, count=count,
                                                      access_rights_uid=access_rights_uid)

