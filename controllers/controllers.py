# -*- coding: utf-8 -*-
# from odoo import http


# class KzmClientMonitoring(http.Controller):
#     @http.route('/kzm_client_monitoring/kzm_client_monitoring/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/kzm_client_monitoring/kzm_client_monitoring/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('kzm_client_monitoring.listing', {
#             'root': '/kzm_client_monitoring/kzm_client_monitoring',
#             'objects': http.request.env['kzm_client_monitoring.kzm_client_monitoring'].search([]),
#         })

#     @http.route('/kzm_client_monitoring/kzm_client_monitoring/objects/<model("kzm_client_monitoring.kzm_client_monitoring"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('kzm_client_monitoring.object', {
#             'object': obj
#         })
