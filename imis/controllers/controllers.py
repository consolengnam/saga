# -*- coding: utf-8 -*-
from odoo import http

# class AgfLocation(http.Controller):
#     @http.route('/agf_location/agf_location/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/agf_location/agf_location/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('agf_location.listing', {
#             'root': '/agf_location/agf_location',
#             'objects': http.request.env['agf_location.agf_location'].search([]),
#         })

#     @http.route('/agf_location/agf_location/objects/<model("agf_location.agf_location"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('agf_location.object', {
#             'object': obj
#         })