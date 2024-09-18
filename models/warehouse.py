from odoo import models, fields, api
import math
from dateutil import relativedelta
from datetime import datetime
from datetime import date
from odoo.tools.translate import _
from odoo.exceptions import UserError, ValidationError


class AccountAsset(models.Model):
    _inherit = 'stock.picking'

    delivery_driver = fields.Char(
        string='Delivery driver',
        required=False)
    company_3pl = fields.Char(
        string='3PL Company',
        required=False)
    temp_at_pick = fields.Float(
        string='Temperature at pick up',
        required=False)
    phone_3pl = fields.Char(
        string='Contact Phone',
        required=False)
    vehicle_reg = fields.Char(
        string='Vehicle registration',
        required=False)
    assigned_picker = fields.Many2one(comodel_name='res.users', string='Assigned Picker', required=False)


class StockLocation(models.Model):
    _inherit = 'stock.location'

    is_warehouse = fields.Boolean(
        string='Is Warehouse',
        required=False)
    min_temp = fields.Float(string='Minimum Temperature')
    max_temp = fields.Float(string='Maximum Temperature')

