import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class RiskWarfWeightMatrices(models.Model):
    _name = 'risk.warf.weight.matrices'
    _description = 'No description at the moment'

    product_name = fields.Char(string='Product Name', required=True)
    country_weight = fields.Float(string='Country Weight', digits=(5, 2), required=True)
    lender_weight = fields.Float(string='Lender Weight', digits=(5, 2), required=True)
    borrower_weight = fields.Float(string='Borrower Weight', digits=(5, 2), required=True)
    transaction_weight = fields.Float(string='Transaction Weight', digits=(5, 2), required=True)
    status = fields.Selection([('1', 'Active'), ('2', 'Inactive')], required=True, default='1')


class RiskGuaranteeProducts(models.Model):
    _name = 'risk.guarantee.products'
    _description = 'No description at the moment'

    product_name = fields.Char(string='Product Name', required=True)
    product_desc = fields.Char(string='Product Desc', required=True)
