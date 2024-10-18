from odoo import http
from odoo.http import request

class PortalQuant(http.Controller):

    @http.route(['/my/consignment_products'], type='http', auth='user', website=True)
    def my_consignment_products(self, **kw):
        # Get the current logged-in user
        user = request.env.user

        # Retrieve stock quants owned by the partner associated with the logged-in user
        quants = request.env['stock.quant'].sudo().search([('owner_id', '=', user.partner_id.id), ('quantity', '>', 0)])


        # Render the template and pass the quant data
        return request.render('rider_warehouse_cus.portal_my_consignment_products', {'quants': quants})
