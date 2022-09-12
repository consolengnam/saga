# -*- coding: utf-8 -*-
import logging
from odoo import _, models, fields, api
from datetime import datetime
from odoo.osv import expression
from odoo.exceptions import except_orm, Warning, RedirectWarning, ValidationError

IN_RECEIVED_STATE = '10003'      #'In Received'
IN_PROCESS_STATE = '10004'      #'In process'
IN_COMMITTEE_STATE = '10005'  # 'In committee'
IN_APPROVED_STATE = '10006'      #'In Approved'
IN_REJECTED_STATE = '10007'      #'In Rejected'

FINAL_STATUS= [
    ('1', 'N/A'),
    ('2', 'Opened'),
    ('3', 'Closed'),
    ('4', 'Follow-up'),
]

_logger = logging.getLogger(__name__)


class RiskMovement(models.Model):
    _name = 'risk.movement'
    risk_model_workflow_id = fields.Many2one('risk.model.workflow', required=True)
    transmitter_id = fields.Many2one('hr.department', string="Transmitter", required=True)
    recipient_id = fields.Many2one('hr.department', string="Recipient", required=True)
    job_transmitter_id = fields.Many2one('hr.job', string="Transmitter", required=True,
                                         domain="[('department_id', '=', transmitter_id)]")
    job_recipient_id = fields.Many2one('hr.job', string="Recipient", required=True,
                                       domain="[('department_id', '=', recipient_id)]")

    comments = fields.Text('Comments')
    reason_for_cancelled = fields.Text('Reason For Cancelled')

    user_transmitter_id = fields.Integer('res.users')
    date_transmitter = fields.Datetime()

    date_last_modif = fields.Datetime()


    action_name = fields.Many2one('risk.workflow.action.list', string="Action Name", required=False,      domain="[('status', '=', '1')]")

    stage_id = fields.Many2one(
        'risk.stage', string='Current Status'
    )

    next_stage_id = fields.Many2one(
        'risk.stage', string='Next Stage'
    )
    final_status=fields.Selection(FINAL_STATUS,  default='1',store=True, string='Final status')
    date_last_modif = fields.Datetime()

    def _default_fullname(self):
        employee_id = self.env.user.employee_id
        return employee_id.name

    # @api.depends('create_uid')
    # def _compute_fullname(self):
    #     """ compute the new values when create_uid has changed """
    #     for movement in self:
    #         fullname = self.create_uid.employee_id.name
    #         movement.fullname = fullname

    fullname = fields.Char('Comments',  related='create_uid.employee_id.name', default=_default_fullname,  store=False)

    def is_delete_movement(self, workflow_id):
        risk_movement = self.env['risk.movement']
        results_movement = risk_movement.search([('risk_model_workflow_id', '=', workflow_id)])
        is_delete = len(results_movement)==1
        for rec in results_movement :
            is_delete = is_delete and  rec.job_transmitter_id ==  rec.job_recipient_id

        return is_delete







class RiskMovementCancelled(models.Model):
    _name = 'risk.movement.cancelled'
    risk_model_workflow_id = fields.Many2one('risk.model.workflow', required=True)
    transmitter_id = fields.Many2one('hr.department', string="Transmitter", required=True)
    recipient_id = fields.Many2one('hr.department', string="Recipient", required=True)
    job_transmitter_id = fields.Many2one('hr.job', string="Transmitter", required=True,
                                         domain="[('department_id', '=', transmitter_id)]")
    job_recipient_id = fields.Many2one('hr.job', string="Recipient", required=True,
                                       domain="[('department_id', '=', recipient_id)]")
    comments = fields.Text('comments')
    reason_for_cancelled = fields.Text('Reason For Cancelled')

    user_transmitter_id = fields.Integer('res.users')
    date_transmitter = fields.Datetime()

    user_cancel_transmitter = fields.Integer('res.users')
    date_cancel_transmitter = fields.Datetime()


class RiskMovementWizard(models.TransientModel):
    _name = 'risk.movement.wizard'

    def _default_model_workflow(self):
        if self._context.get('active_model') == 'risk.model.workflow':
            return self._context.get('active_id', False)

    risk_model_workflow_id = fields.Many2one('risk.model.workflow', default=_default_model_workflow)

    # risk_model_workflow_id = fields.Many2one('risk.model.workflow')

    def _default_Transmitter(self):
        user_id = self._uid;
        req = self.env['hr.employee']
        employee_id = req.search([('user_id', '=', user_id)])
        return employee_id.department_id.id

    transmitter_id = fields.Many2one('hr.department', string="Transmitter department", default=_default_Transmitter,
                                     readonly=True)

    # recipient_id = fields.Many2one('hr.department', string="Receiving department", domain="[('id', '!=', transmitter_id)]")

    @api.model
    def _get_recipient_id(self):
        default_type = self._context.get('default_type_action')
        recipient_ids = []
        departments = []
        risk_model_workflow_env = self.env['risk.model.workflow']

        if default_type == "1":
            departments = risk_model_workflow_env.get_parent_hierarchie_departments_list()
        elif default_type == "2":
            departments = risk_model_workflow_env.get_child_hierarchie_departments_list()
        else:
            departments = self.env['hr.department'].search([])

        for rec in departments:
            recipient_ids.append(rec.id)
        return [('id', 'in', recipient_ids)]

    recipient_id = fields.Many2one('hr.department', string="Receiving department", domain=_get_recipient_id)

    def _default_job_Transmitter(self):
        user_id = self._uid;
        req = self.env['hr.employee']
        employee_id = req.search([('user_id', '=', user_id)])
        return employee_id.job_id.id

    # job_transmitter_id = fields.Many2one('hr.job', string="Transmitter station", domain="[('department_id', '=', transmitter_id)]" , default=_default_job_Transmitter,  compute='_compute_job_transmitter_id')

    job_transmitter_id = fields.Many2one('hr.job', string="Transmitter station",
                                         domain="[('department_id', '=', transmitter_id)]",
                                         default=_default_job_Transmitter, readonly=True)
    job_recipient_id = fields.Many2one('hr.job', string="Receiver station",
                                       domain="['&',('department_id', '=', recipient_id),('id', '!=', job_transmitter_id)]",
                                       compute='_compute_job_recipient_id', readonly=False, store=True)
    # job_recipient_id = fields.Many2one('hr.job', string="Receiver station", domain="[('department_id', '=', recipient_id)]" ,  compute='_compute_job_recipient_id' , readonly=False, store=True)
    # job_recipient_id = fields.Many2one('hr.job', string="Receiver station",domain="[('department_id', '=', recipient_id)]" )
    comments = fields.Text('comments/Remarks')
    reason_for_cancelled = fields.Text('Reason For Cancelled')

    user_transmitter_id = fields.Integer('res.users')
    date_transmitter = fields.Datetime()
    user_cancel_transmitter = fields.Integer('res.users')
    date_cancel_transmitter = fields.Datetime()

    def _default_stage_id(self):
        risk_model_workflow_id = None
        if self._context.get('active_model') == 'risk.model.workflow':
            risk_model_workflow_id = self._context.get('active_id', False)
        default_stage_id = None
        if risk_model_workflow_id:
            risk_model_workflow = self.env['risk.model.workflow'].browse(risk_model_workflow_id)
            default_stage_id = risk_model_workflow.stage_id.id

        self.next_stage_id = default_stage_id
        return default_stage_id


    stage_id = fields.Many2one(
        'risk.stage', string='Current Status',default=_default_stage_id
    )

    next_stage_id = fields.Many2one(
        'risk.stage', string='Next Stage'
    )

    final_status = fields.Selection(FINAL_STATUS, default='1', store=True, string='Final status')



    @api.model
    def _get_action_name_list(self):

        risk_model_workflow_id = None
        if self._context.get('active_model') == 'risk.model.workflow':
            risk_model_workflow_id = self._context.get('active_id', False)
        action_name_ids = []
        if risk_model_workflow_id :
            risk_model_workflow = self.env['risk.model.workflow'].browse(risk_model_workflow_id)
            risk_workflow_approval_structure = self.env['risk.workflow.approval.structure']
            action_name_ids =  risk_workflow_approval_structure.get_action_list(risk_model_workflow.risk_workflow_id.id, risk_model_workflow.stage_id.id)
        return [('id', 'in', action_name_ids)]

    action_name = fields.Many2one('risk.workflow.action.list', string="Select Action", required=False, domain=_get_action_name_list)

    @api.onchange('stage_id', 'action_name')
    def stage_id_or_action_name_or_next_stage_id_onchange(self):


        risk_model_workflow_id = None
        risk_workflow_id = None
        if self._context.get('active_model') == 'risk.model.workflow':
            risk_model_workflow_id = self._context.get('active_id', False)
        if risk_model_workflow_id:
            risk_model_workflow = self.env['risk.model.workflow'].browse(risk_model_workflow_id)
            risk_workflow_id = risk_model_workflow.risk_workflow_id.id
            stage_id = risk_model_workflow.stage_id.id
        if  risk_workflow_id and stage_id:
            risk_workflow_approval_structure = self.env['risk.workflow.approval.structure']
            if not self.action_name:
                action_name_ids = risk_workflow_approval_structure.get_action_list(risk_workflow_id,stage_id)
                if action_name_ids and action_name_ids[0]:
                    self.action_name =  self.env['risk.workflow.action.list'].browse(action_name_ids[0])
            risk_workflow_approval_structure_results = risk_workflow_approval_structure.get_next_status_event(risk_workflow_id,stage_id ,self.action_name.id )
            if  risk_workflow_approval_structure_results :
                for risk_workflow_approval_structure_result in risk_workflow_approval_structure_results:
                    self.next_stage_id=risk_workflow_approval_structure_result.id
                    if risk_workflow_approval_structure.is_end_event(risk_workflow_approval_structure_result.id, risk_workflow_id):
                        self.recipient_id = self.transmitter_id
                        self.job_recipient_id = self.job_transmitter_id
                    else:
                        risk_workflow_approval_structure_roles_results = risk_workflow_approval_structure.get_next_role_event( risk_workflow_id, risk_workflow_approval_structure_result.id)
                        if risk_workflow_approval_structure_roles_results:
                            for risk_workflow_approval_structure_roles_result in risk_workflow_approval_structure_roles_results:
                                self.recipient_id = risk_workflow_approval_structure_roles_result.department_id.id
                                self.job_recipient_id = risk_workflow_approval_structure_roles_result.id

    def add_risk_movement(self):
        '''Transmission action'''

        current_time = datetime.now()

        movementModel = self.env['risk.movement']
        workflowModel = self.env['risk.model.workflow']
        for movement in self:
            results_workflow = workflowModel.search([('id', '=', movement.risk_model_workflow_id.id)])

            check_position = workflowModel.get_position(results_workflow)

            if check_position == False:
                raise ValidationError(_('Transmission not possible: Please contact your administrator.'))
            newmovement = movementModel.create({
                'risk_model_workflow_id': movement.risk_model_workflow_id.id,
                'transmitter_id': movement.transmitter_id.id,
                'recipient_id': movement.recipient_id.id,
                'job_transmitter_id': movement.job_transmitter_id.id,
                'job_recipient_id': movement.job_recipient_id.id,
                'comments': movement.comments,
                'user_transmitter_id': self._uid,
                'date_transmitter': current_time,
                'date_last_modif': current_time,
                'action_name': movement.action_name.id,
                'stage_id': movement.stage_id.id,
                'next_stage_id': movement.next_stage_id.id,
                'final_status':  movement.final_status,

            })



            if newmovement:

                results_workflow.write({
                    'last_movement_id': newmovement.id,
                    'stage_id': movement.next_stage_id.id,
                    'position_id': movement.job_recipient_id.id,
                    'date_last_modif': current_time,
                    'role_id': movement.job_recipient_id.id,
                })

        message = _("Submission completed successfully")

        message_id = self.env['message.wizard'].create({'message': message})
        return {
            'name': _('Successfull'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'message.wizard',
            # pass the id
            'res_id': message_id.id,
            'target': 'new'
        }

    def reset_risk_movement(self):
        '''Action to reset movement.'''

        now = datetime.now()

        movementModel = self.env['risk.movement']
        movementAnnulModel = self.env['risk.movement.cancelled']
        workflowModel = self.env['risk.model.workflow']
        for movement in self:

            results_workflow = workflowModel.search([('id', '=', movement.risk_model_workflow_id.id)])

            check_position = workflowModel.get_cancel_position(results_workflow)

            if check_position == False:
                raise ValidationError(_('Cancel Emission not possible: Please contact your administrator.'))

            if results_workflow:
                results_movement = movementModel.search([('id', '=', results_workflow.last_movement_id.id)])
                if results_movement:
                    newmovement = movementAnnulModel.create({
                        'risk_model_workflow_id': results_movement.risk_model_workflow_id.id,
                        'transmitter_id': results_movement.transmitter_id.id,
                        'recipient_id': results_movement.recipient_id.id,
                        'job_transmitter_id': results_movement.job_transmitter_id.id,
                        'job_recipient_id': results_movement.job_recipient_id.id,
                        'comments': results_movement.comments,
                        'user_transmitter_id': self._uid,
                        'date_transmitter': datetime.now(),
                        'user_cancel_transmitter': self._uid,
                        'date_cancel_transmitter': now,
                        'reason_for_cancelled': movement.reason_for_cancelled,
                    })

                    results_workflow.write({
                        'stage_id': results_movement.stage_id.id,
                        'position_id': movement.job_transmitter_id.id,
                        'date_last_modif': now,
                        'role_id': movement.job_transmitter_id.id,
                    })
                    results_movement.unlink()

    def return_risk_movement(self):
        '''Return action'''

        current_time = datetime.now()

        movementModel = self.env['risk.movement']
        workflowModel = self.env['risk.model.workflow']
        for movement in self:
            results_workflow = workflowModel.search([('id', '=', movement.risk_model_workflow_id.id)])

            check_position = workflowModel.get_position(results_workflow)

            if check_position == False:
                raise ValidationError(_('Transmission not possible: Please contact your administrator.'))

            if results_workflow :
                for rec in results_workflow:
                    stage_id = rec.stage_id.id
                    risk_workflow_id = rec.risk_workflow_id.id

                    risk_workflow_approval_structure = self.env['risk.workflow.approval.structure']

                    current_approval=risk_workflow_approval_structure.get_current_approval(risk_workflow_id, stage_id)

                    newmovement = movementModel.create({
                        'risk_model_workflow_id': rec.id,
                        'transmitter_id': movement.transmitter_id.id,
                        'recipient_id': current_approval.department_id.id,
                        'job_transmitter_id': movement.job_transmitter_id.id,
                        'job_recipient_id': current_approval.job_id.id,
                        'comments': movement.comments,
                        'user_transmitter_id': self._uid,
                        'date_transmitter': current_time,
                        'date_last_modif': current_time,
                        #'action_name': movement.action_name.id,
                        'stage_id':  stage_id ,
                        'next_stage_id': current_approval.risk_current_stage_id.id,
                        'final_status': movement.final_status,

                    })

                    if newmovement:
                        results_workflow.write({
                            'last_movement_id': newmovement.id,
                            'stage_id': current_approval.risk_current_stage_id.id,
                            'position_id': current_approval.job_id.id,
                            'date_last_modif': current_time,
                            'role_id': current_approval.job_id.id,
                        })

                message = _("Submission completed successfully")

                message_id = self.env['message.wizard'].create({'message': message})
                return {
                    'name': _('Successfull'),
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_model': 'message.wizard',
                    # pass the id
                    'res_id': message_id.id,
                    'target': 'new'
                }


    @api.depends('recipient_id')
    def _compute_job_recipient_id(self):
        """ compute the new values when recipient_id has changed """
        for movement in self:
            if self.recipient_id.id:
                res = self.env['hr.job'].search(
                    ['&', ('department_id', '=', self.recipient_id.id), ('id', '!=', self.job_transmitter_id.id)],
                    limit=1)
                if res and res[0]:
                    movement.job_recipient_id = res[0]
                else:
                    movement.job_recipient_id = False

    def _get_default_stage_id(self):
        Stage = self.env['risk.stage']
        return Stage.search([('code', '=', IN_PROCESS_STATE)], limit=1)