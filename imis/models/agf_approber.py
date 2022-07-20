# -*- coding: utf-8 -*-

from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)


class AgfApprober(models.Model):

    _name = 'agf.approber'
    _description = 'Approval approbation'

    approbation = fields.Selection([('yes', 'YES'), ('no', 'NO')])
    review_note = fields.Html('Review note')
    approver = fields.Many2one('res.users', string='Approber', index=True, tracking=True,
                               default=lambda self: self.env.user)
    gc_approval_id = fields.Many2one('agf.approval', 'GC', tracking=True)
    board_approval_id = fields.Many2one('agf.approval', 'Board', tracking=True)

# @api multi
    def action_vote_apply(self, values):
        self.write(values)
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
