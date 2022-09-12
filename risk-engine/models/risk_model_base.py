# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api, _
from datetime import datetime
from odoo.osv import expression

from datetime import datetime

_logger = logging.getLogger(__name__)




class RiskCompter(models.Model):
    _name = 'risk.compter'
    _description = 'The Compter'
    _rec_name = 'compter'

    service = fields.Many2one('hr.department', string="Department" , required=False )
    description = fields.Text(string='Description', required=False , translate=True)
    compter = fields.Integer(string='Counter' , required=True)


class RiskApplication(models.Model):
    """ Workflow model description.
    """
    _name = "risk.application"
    _description = "RISK APPLICATION"
    _rec_name = 'name'
    _order = "id"

    name = fields.Char('Application Name', required=True, translate=True)
    description = fields.Char('Description', required=False , translate=True)
    status = fields.Selection([('1', 'Active'), ('2', 'Inactive')], required=True, default='1')



class RiskWorkflow(models.Model):
    """ Workflow model description.
    """
    _name = "risk.workflow"
    _description = "RISK WORKFLOW"
    _rec_name = 'name'
    _order = "id"

    name = fields.Char('Workflow Name', required=True, translate=True)
    code = fields.Char('Workflow Code', required=True)
    status = fields.Selection([('1', 'Active'), ('2', 'Inactive')], required=True, default='1')
    risk_application_id = fields.Many2one('risk.application', string="Application")

    def get_workflow(self, code):
        workflow = None
        risk_workflow_env = self.env['risk.workflow']
        risk_workflow_results= risk_workflow_env.search([('code', '=', code)], limit=1)
        if risk_workflow_results :
            for risk_workflow_result in risk_workflow_results :
                 workflow = risk_workflow_result
        return workflow





class RiskStage(models.Model):
    """ Model for case stages. This models the main stages of a document
        management flow. Main RISK objects will now use only stages, instead of state and stages.
        Stages are for example used to display the kanban view of records.
    """
    _name = "risk.stage"
    _description = "RISK Stages"
    _rec_name = 'name'
    _order = "sequence, name, id"

    name = fields.Char('Status Name', required=True, translate=True)  # name or status
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    fold = fields.Boolean('Folded in Pipeline',
                          help='This stage is folded in the kanban view when there are no records in that stage to display.')

    code = fields.Char('Code', required=True)
    tracking_status = fields.Char('Status Display Name', required=False, translate=True)
    action = fields.Char('Action', required=False, translate=True)
    final_status = fields.Char('Final status', required=False, translate=True)
    type_workflow = fields.Char('Type Workflow', required=False, translate=True)
    risk_workflow_id = fields.Many2one('risk.workflow', string="Workflow")





class RiskWorkflowApprovalStructure(models.Model):
    """ Workflow Approval Structure
    """
    _name = "risk.workflow.approval.structure"
    _description = "RISK WORKFLOW APPROVAL STRUCTURE"
    _rec_name = 'action_name'
    _order = "id"


    risk_workflow_id = fields.Many2one('risk.workflow', string="Workflow" , required=True)
    risk_current_stage_id = fields.Many2one('risk.stage', string="Workflow Current Status", required=True)
    #action_name = fields.Char('Action Name', required=True, translate=True)
    action_name = fields.Many2one('risk.workflow.action.list', string="Action Name", required=True, default=1, domain="[('status', '=', '1')]")
    risk_next_stage_id = fields.Many2one('risk.stage', string="Workflow Next Status", required=True)
    department_id = fields.Many2one('hr.department', string="Department", required=True)
    job_id = fields.Many2one('hr.job', string="Role Name", required=True,   domain="[('department_id', '=', department_id)]")
    type_event = fields.Selection([('1', 'Start Event'), ('2', 'Intermediate Event'),  ('3', 'End Event')], required=True, default='2')

    _sql_constraints = [('risk_workflow_id_risk_current_stage_id_action_name_uniq', 'unique (risk_workflow_id,risk_current_stage_id, action_name)', _("stage and action name for this workflow already exists !"))]

    def get_start_event(self,code):
        stage = None
        risk_workflow = None
        risk_workflow_env = self.env['risk.workflow']
        risk_workflow_results = risk_workflow_env.get_workflow(code)
        for risk_workflow_result in risk_workflow_results :
             risk_workflow = risk_workflow_result

        if risk_workflow :
            risk_workflow_approval_structure_env = self.env['risk.workflow.approval.structure']
            risk_workflow_approval_structure_results= risk_workflow_approval_structure_env.search(['&', ('type_event', '=', '1'),('risk_workflow_id', '=', risk_workflow.id)], limit=1)
            for risk_workflow_approval_structure_result in risk_workflow_approval_structure_results :
                 stage = risk_workflow_approval_structure_result.risk_current_stage_id
        return stage

    def get_start_event_list(self, risk_workflow_id):
        start_events = []
        if risk_workflow_id:
            risk_workflow_approval_structure_env = self.env['risk.workflow.approval.structure']
            risk_workflow_approval_structure_results = risk_workflow_approval_structure_env.search(
                ['&', ('type_event', '=', '1'), ('risk_workflow_id', '=', risk_workflow_id)])
            for risk_workflow_approval_structure_result in risk_workflow_approval_structure_results:
                stage = risk_workflow_approval_structure_result.risk_current_stage_id
                start_events.append(stage.id)
        return start_events

    def get_end_event(self,risk_workflow_id):
        end_events = []
        if risk_workflow_id :
            risk_workflow_approval_structure_env = self.env['risk.workflow.approval.structure']
            risk_workflow_approval_structure_results= risk_workflow_approval_structure_env.search(['&', ('type_event', '=', '3'),('risk_workflow_id', '=', risk_workflow_id)])
            for risk_workflow_approval_structure_result in risk_workflow_approval_structure_results :
                 stage = risk_workflow_approval_structure_result.risk_next_stage_id
                 end_events.append(stage.id)
        return end_events

    def is_end_event(self, stage_event_id, risk_workflow_id):
        return stage_event_id in self.get_end_event(risk_workflow_id)

    def is_start_event(self, stage_event_id, risk_workflow_id):
        return stage_event_id in self.get_start_event_list(risk_workflow_id)







    def get_action_list(self,current_workflow, current_status):
        action_name_ids = []
        if current_workflow and  current_status :
            risk_workflow_approval_structure_env = self.env['risk.workflow.approval.structure']
            risk_workflow_approval_structure_results= risk_workflow_approval_structure_env.search(['&', ('risk_current_stage_id', '=', current_status),('risk_workflow_id', '=', current_workflow)])
            for risk_workflow_approval_structure_result in risk_workflow_approval_structure_results :
                 action_name_ids.append(risk_workflow_approval_structure_result.action_name.id)
        return action_name_ids

    def get_next_status_event(self, current_workflow, current_status, current_action) :

        next_stage = None
        if current_workflow and current_status and current_action:
            risk_workflow_approval_structure_env = self.env['risk.workflow.approval.structure']
            risk_workflow_approval_structure_results = risk_workflow_approval_structure_env.search(
                ['&',  ('risk_workflow_id', '=', current_workflow) ,  ('risk_current_stage_id', '=', current_status),  ('action_name', '=', current_action)], limit=1)
            for risk_workflow_approval_structure_result in risk_workflow_approval_structure_results:
                next_stage = risk_workflow_approval_structure_result.risk_next_stage_id
        return next_stage


    def get_next_role_event(self, current_workflow, next_status) :

        next_role = None
        if current_workflow and next_status :
            risk_workflow_approval_structure_env = self.env['risk.workflow.approval.structure']
            risk_workflow_approval_structure_results = risk_workflow_approval_structure_env.search(
                ['&',  ('risk_workflow_id', '=', current_workflow) ,  ('risk_current_stage_id', '=', next_status)], limit=1)
            for risk_workflow_approval_structure_result in risk_workflow_approval_structure_results:
                next_role = risk_workflow_approval_structure_result.job_id
        return next_role

    def get_current_approval(self, current_workflow, next_status) :
        current_approval = None
        if current_workflow and next_status :
            risk_workflow_approval_structure_env = self.env['risk.workflow.approval.structure']
            risk_workflow_approval_structure_results = risk_workflow_approval_structure_env.search( ['&',  ('risk_workflow_id', '=', current_workflow) ,  ('risk_next_stage_id', '=', next_status)], limit=1)
            for risk_workflow_approval_structure_result in risk_workflow_approval_structure_results:
                current_approval = risk_workflow_approval_structure_result
        return current_approval



class RiskWorkflowActionList(models.Model):
    """ Workflow model action list.
    """
    _name = "risk.workflow.action.list"
    _description = "RISK WORKFLOW ACTION LIST"
    _rec_name = 'name'
    _order = "id"

    name = fields.Char('Action Name', required=True, translate=True)
    description = fields.Char('Description', required=False , translate=True)
    status = fields.Selection([('1', 'Active'), ('2', 'Inactive')], required=True, default='1')

    _sql_constraints = [('name_uniq', 'unique (name)', _("Action name already exists !"))]




class RiskHrDepartment(models.Model):
    _inherit = 'hr.department'
    _description = 'Department Managment'
    code = fields.Char(string='Code', required=False )

class RiskHrJob(models.Model):
    _inherit = 'hr.job'
    _description = 'Job Managment'
    code = fields.Char(string='Code', required=False  )



class MessageWizard(models.TransientModel):
    """ Workflow show message.
       """

    _name = 'message.wizard'

    message = fields.Text('Message', required=True)

    def action_ok(self):
        """ close wizard"""
        return {'type': 'ir.actions.act_window_close'}



class RiskCounter(models.Model):
    _name = 'risk.counter'
    _description = 'The Counter'
    _rec_name = 'counter'
    _order = 'id desc'

    risk_workflow_id = fields.Many2one('risk.workflow', string="Worflow Number" , required=True )
    year = fields.Integer(required=True)
    month = fields.Integer(required=True)
    counter = fields.Integer(string='Counter', required=True)


    def get_current_counter(self,risk_workflow_id):

            current_time = datetime.now()
            year = current_time.year
            month = current_time.month

            self._cr.execute(
                'SELECT id, counter FROM risk_counter WHERE risk_workflow_id = %s and year = %s and month= %s LIMIT 1 FOR NO KEY UPDATE ', (risk_workflow_id,year,month))
            result = self._cr.fetchall()
            if result:
                for compter in result:
                    return compter
            else :
                counterModel = self.env['risk.counter']
                newCounter = counterModel.create({
                    'risk_workflow_id': risk_workflow_id,
                    'year': year,
                    'month': month,
                    'counter': 0,

                })
                if newCounter :
                    self._cr.execute(
                        'SELECT id, counter FROM risk_counter WHERE risk_workflow_id = %s and year = %s and month= %s LIMIT 1 FOR NO KEY UPDATE ',
                        (risk_workflow_id, year, month))
                    result = self._cr.fetchall()
                    if result:
                        for compter in result:
                            return compter


    def update_current_counter(self, counter_id, new_counter):

        results_counter = self.env['risk.counter'].search([('id', '=', counter_id)])
        if results_counter:
            results_counter.write({
                'counter': new_counter,
            })

    def get_current_counter_id(self,risk_workflow_id):

            self._cr.execute(
                'SELECT id, counter FROM risk_counter WHERE risk_workflow_id = %s order by id desc LIMIT 1 FOR NO KEY UPDATE ', (risk_workflow_id,))
            result = self._cr.fetchall()
            if result:
                for compter in result:
                    return compter