# -*- coding: utf-8 -*-
# from odoo import http


# class Risk-engine(http.Controller):
#     @http.route('/risk-engine/risk-engine', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/risk-engine/risk-engine/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('risk-engine.listing', {
#             'root': '/risk-engine/risk-engine',
#             'objects': http.request.env['risk-engine.risk-engine'].search([]),
#         })

#     @http.route('/risk-engine/risk-engine/objects/<model("risk-engine.risk-engine"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('risk-engine.object', {
#             'object': obj
#         })
