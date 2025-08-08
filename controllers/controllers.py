# -*- coding: utf-8 -*-
# from odoo import http


# class MachineryMaintenance(http.Controller):
#     @http.route('/machinery_maintenance/machinery_maintenance', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/machinery_maintenance/machinery_maintenance/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('machinery_maintenance.listing', {
#             'root': '/machinery_maintenance/machinery_maintenance',
#             'objects': http.request.env['machinery_maintenance.machinery_maintenance'].search([]),
#         })

#     @http.route('/machinery_maintenance/machinery_maintenance/objects/<model("machinery_maintenance.machinery_maintenance"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('machinery_maintenance.object', {
#             'object': obj
#         })

