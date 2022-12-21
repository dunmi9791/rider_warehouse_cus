from odoo import fields, models, api


class TemperatureHistory(models.Model):
    _name = 'temperature.history'
    _description = 'Temperature history of warehouse location'

    date_time = fields.Datetime(
        string='Date and time',
        required=False)
    temperature = fields.Float(
        string='Temperature',
        required=False)
    location_id = fields.Many2one(
        comodel_name='stock.location',
        string='Location',
        required=False)
    temp_diff = fields.Float(
        string='Temperature difference',
        required=False)
    latest_temp = fields.Float(
        string='Latest temperature',
        required=False)


class AccountAsset(models.Model):
    _inherit = 'stock.location'

    temp_history = fields.One2many(
        comodel_name='temperature.history',
        inverse_name='location_id',
        string='Temperature history',
        required=False)

