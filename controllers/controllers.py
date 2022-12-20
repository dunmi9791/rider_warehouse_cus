# -*- coding: utf-8 -*-
# from odoo import http


# class RidersWarehouseCustom(http.Controller):
#     @http.route('/riders_warehouse_custom/riders_warehouse_custom', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/riders_warehouse_custom/riders_warehouse_custom/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('riders_warehouse_custom.listing', {
#             'root': '/riders_warehouse_custom/riders_warehouse_custom',
#             'objects': http.request.env['riders_warehouse_custom.riders_warehouse_custom'].search([]),
#         })

#     @http.route('/riders_warehouse_custom/riders_warehouse_custom/objects/<model("riders_warehouse_custom.riders_warehouse_custom"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('riders_warehouse_custom.object', {
#             'object': obj
#         })
