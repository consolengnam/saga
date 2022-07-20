# -*- coding: utf-8 -*-
{
    'name': "AGF Modules",

    'summary': """
        Group of Guarantee Fund modules""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Opensys Technologies",
    'website': "http://www.opensystechnologies.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Guarantee Origination',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'contacts',
                'crm',
                ],

    # always loaded
    'data': [
        'security/agf_security.xml',
        'security/ir.model.access.csv',
        'views/agf_country_views.xml',
        'views/agf_usdrate_views.xml',
        'views/agf_pfi_views.xml',
        'views/agf_documentation_views.xml',
        'views/imis_crm_views.xml',
        'views/agf_screening.xml',
        'views/agf_categorization_views.xml',
        'views/agf_approber_views.xml',
        'views/agf_approval_views.xml',
        'views/agf_issuance_views.xml',
        'views/agf_internal_questionnaire_views.xml',
        'views/agf_template_questions_views.xml',
        'views/action_plan_views.xml',
        'data/mail_template_data.xml',
        'views/menu_view.xml',
        'wizard/es_dd_report_views.xml',
        'wizard/es_dd_report_template.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    # customise user menu
    'qweb': [
        'static/src/xml/template.xml'
    ],
}
