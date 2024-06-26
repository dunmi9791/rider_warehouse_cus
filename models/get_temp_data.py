import requests
from datetime import datetime, timedelta
from odoo import models, fields, api
import logging


class SensorDataImport(models.Model):
    _name = 'sensor.data.import'
    _description = 'Sensor Data Import'

    @api.model
    def fetch_and_import_data(self):
        logger = logging.getLogger(__name__)
        token = 'VXNlci0yNTA3O2Q0MmFlNGViNzI3OTQ2MzU4ZmExN2ZlZDQwMzAxOTRk'
        # auth_url = 'https://i.cloud.tzonedigital.cn/Identity'
        # auth_params = {
        #     'appId': '5c1169a48591411eac78dc528155f40e',
        #     'appKey': 'User-2507',
        #     'appSecret': 'NGYxZDQ2MWIwZWViNDFjMmEzMzUxMzIxNTQ4MzBmNDQ='
        # }
        # auth_response = requests.post(auth_url, json=auth_params)
        #
        # if auth_response.status_code != 200:
        #     raise Exception('Failed to authenticate to china cloud server')
        #
        # token = auth_response.json().get('token')
        # if not token:
        #     raise Exception('Token not found in authentication response')

        headers = {'Authorization': f'Bearer {token}'}

        end_time = int(datetime.utcnow().timestamp())
        start_time = end_time - 360000

        device_ids = self.env['temperature.device'].search([]).mapped('serial_no')
        logger.info(f'Starting data fetch at {datetime.utcnow()}')

        for device_id in device_ids:
            url = f'https://i.cloud.tzonedigital.cn/Data/HistoryData/{device_id}'
            params = {
                'pageIndex': 1,
                'pageSize': 10,
                'begin': start_time,
                'end': end_time
            }
            response = requests.get(url, headers=headers, params=params)

            if response.status_code != 200:
                logger.error(f'Failed to fetch data for device {device_id} at {datetime.utcnow()}')
                raise Exception(f'Failed to fetch data for device {device_id}')

            data = response.json()
            logger.info(f'Response for device {device_id}: {data}')
            sensor_data_model = self.env['sensor.data']
            temperature_device_model = self.env['temperature.device']

            for item in data.get('body', {}).get('dataList', []):
                device_record = temperature_device_model.search([('serial_no', '=', device_id)], limit=1)
                if device_record:
                    sensor_data_model.create({
                        'device_id': device_record.id,
                        'temperature': item.get('temperature'),
                        'temperature1': item.get('temperature1'),
                        'humidity': item.get('humidity'),
                        'humidity1': item.get('humidity1'),
                        'light': item.get('light'),
                        'vibration': item.get('vibration'),
                        'voltage': item.get('voltage'),
                        'battery': item.get('battery'),
                        'rssi': item.get('rssi'),
                        'lat_lng': item.get('latLng'),
                        'base_station': item.get('baseStation'),
                        'io': item.get('io'),
                        'rtc': item.get('rtc'),
                        'create_time': item.get('createTime'),
                    })

        logger.info(f'Finished data fetch at {datetime.utcnow()}')
