# -*- coding: utf-8 -*-
{
    'name': "risk-engine",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base' ,  'mail', 'hr', 'crm' , 'agf'
      ],

    # always loaded
    'data': [
        'security/risk_engine_security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/risk_view_risk_models.xml',
        'views/risk_view_risk-engine_premium_d.xml',
        'views/risk_view_risk-engine_premium_f.xml',
        'views/risk_view_risk-engine_warf_weight_matrix.xml',
        'views/risk_view_risk-engine_pricing_model_constants.xml',
        'views/risk_view_risk-engine_recovery_rate.xml',
        'views/risk_view_risk-engine_period_after_default_for_recovery.xml',
        'views/risk_view_risk_model_simulation.xml',
        'views/risk_view_risk_model_workflow_movement.xml',
        'views/risk_view_risk_model_workflow.xml',

        'views/risk_view_risk_model_base.xml',

        'views/risk_menu.xml',
        'data/risk_agency_default_rates.xml',
        'data/risk_free_vectors.xml',
        'data/risk_stage.xml',

        'data/risk_param_acceptance_term.xml',
        'data/risk_param_raac_memo_review.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
