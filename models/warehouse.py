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
    temperature_device_ids = fields.One2many(comodel_name='temperature.device', inverse_name='location_id', string='Device data',
                                      required=False)
    latest_temp = fields.Float(string='Latest Temperature', compute='_compute_latest_temperature')
    temperature_data_ids = fields.One2many(comodel_name='location.temp.data', inverse_name='location_id',
                                             string='Temperature data',
                                             required=False)

    @api.depends('temperature_device_ids.sensor_data_ids.temperature',
                 'temperature_device_ids.sensor_data_ids.rtc_datetime')
    def _compute_latest_temperature(self):
        for location in self:
            temperatures = []
            for device in location.temperature_device_ids:
                # Get the latest sensor data record for the device based on rtc_datetime
                latest_data = device.sensor_data_ids.sorted(
                    key=lambda r: r.rtc_datetime or fields.Datetime.from_string('1970-01-01 00:00:00'), reverse=True)
                if latest_data:
                    latest_temp = latest_data[0].temperature
                    if latest_temp is not None:
                        temperatures.append(latest_temp)
            if temperatures:
                # Calculate the average of the latest temperatures
                location.latest_temp = sum(temperatures) / len(temperatures)
            else:
                location.latest_temp = 0.0  # Or set to False if you prefer
                
class LocationTemperatureData(models.Model):
    _name = 'location.temp.data'
    _description = 'Location Temperature Data'

    location_id = fields.Many2one(
        comodel_name='stock.location',
        string='Location_id',
        required=False)
    date_time = fields.Datetime(
        string='Date and time', 
        required=False)
    temperature = fields.Float(
        string='Temperature', 
        required=False)

    @api.model
    def compute_and_store_latest_temperatures(self):
        """Compute latest temperatures for warehouse locations and store/update in location.temp.data."""
        warehouse_locations = self.env['stock.location'].search([('is_warehouse', '=', True)])
        for location in warehouse_locations:
            latest_temp = location.latest_temp
            if latest_temp is not None:
                # Search for an existing record for this location
                temp_data = self.search([('location_id', '=', location.id)], limit=1)
                if temp_data:
                    # Update existing record
                    temp_data.write({
                        'temperature': latest_temp,
                        'date_time': fields.Datetime.now(),
                    })
                else:
                    # Create a new record
                    self.create({
                        'temperature': latest_temp,
                        'date_time': fields.Datetime.now(),
                        'location_id': location.id,
                    })
    



