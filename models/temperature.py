from odoo import fields, models, api
from datetime import datetime


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

    temp_devices = fields.One2many(
        comodel_name='temperature.device',
        inverse_name='location_id',
        string='Temperature Sensors',
        required=False)


class TemperatureLog(models.Model):
    _name = 'temperature.device'
    _description = 'Temperature devices'

    device_name = fields.Char(
       string='Device name',
       required=False)
    device_id = fields.Char(string='Device ID', required=False)
    serial_no = fields.Char(string='Serial Number', required=False)
    location_id = fields.Many2one(comodel_name='stock.location', string='Location', required=False)
    sensor_data_ids = fields.One2many(comodel_name='sensor.data',inverse_name='device_id', string='Sensor data',
                                      required=False)


class SensorData(models.Model):
    _name = 'sensor.data'
    _description = 'Sensor Data'

    device_id = fields.Many2one(comodel_name='temperature.device', string='Device', required=False)
    temperature = fields.Float(string='Temperature')
    temperature1 = fields.Float(string='Temperature1', required=False)
    humidity = fields.Float(string='Humidity', required=False)
    humidity1 = fields.Float(string='Humidity1', required=False)
    light = fields.Float(string='Light', required=False)
    vibration = fields.Float(string='Vibration', required=False)
    voltage = fields.Float(string='Voltage')
    battery = fields.Integer(string='Battery')
    rssi = fields.Integer(string='RSSI')
    lat_lng = fields.Char(string='LatLng')
    base_station = fields.Char(string='Base Station', required=False)
    io = fields.Char(string='IO')
    rtc = fields.Integer(string='RTC')
    rtc_datetime = fields.Datetime(string='RTC Datetime', compute='_compute_rtc_datetime', store=True)
    create_time = fields.Integer(string='Create Time')
    create_time_datetime = fields.Datetime(string='Create Time Datetime', compute='_compute_create_time_datetime', store=True)

    @api.depends('rtc')
    def _compute_rtc_datetime(self):
        for record in self:
            record.rtc_datetime = datetime.utcfromtimestamp(record.rtc) if record.rtc else False

    @api.depends('create_time')
    def _compute_create_time_datetime(self):
        for record in self:
            record.create_time_datetime = datetime.utcfromtimestamp(record.create_time) if record.create_time else False

    @api.model
    def create(self, vals):
        if 'rtc' in vals:
            vals['rtc_datetime'] = datetime.utcfromtimestamp(vals['rtc'])
        if 'create_time' in vals:
            vals['create_time_datetime'] = datetime.utcfromtimestamp(vals['create_time'])
        return super(SensorData, self).create(vals)

    def write(self, vals):
        if 'rtc' in vals:
            vals['rtc_datetime'] = datetime.utcfromtimestamp(vals['rtc'])
        if 'create_time' in vals:
            vals['create_time_datetime'] = datetime.utcfromtimestamp(vals['create_time'])
        return super(SensorData, self).write(vals)