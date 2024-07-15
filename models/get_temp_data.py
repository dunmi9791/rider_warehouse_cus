import requests
from datetime import datetime, timedelta
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class SensorDataImport(models.Model):
    _name = 'sensor.data.import'
    _description = 'Sensor Data Import'

    @api.model
    def fetch_and_import_data(self):
        proxy_auth_url = 'http://10.10.0.1:3000/proxy/identity'
        proxy_history_url = 'http://10.10.0.1:3000/proxy/history'

        try:
            # Authenticate and get token
            auth_response = requests.get(proxy_auth_url)
            auth_response.raise_for_status()  # Raise HTTPError for bad responses
            auth_data = auth_response.json()

            if auth_data['status'] != 1 or 'body' not in auth_data or 'token' not in auth_data['body']:
                raise Exception('Failed to authenticate: Invalid response format')

            token = auth_data['body']['token']
        except requests.RequestException as e:
            _logger.error(f"Failed to authenticate: {e}")
            raise

        headers = {'Authorization': f'Bearer {token}'}

        # Calculate time range for the data fetch
        end_time = int(datetime.utcnow().timestamp())
        start_time = end_time - 3600  # Last 1 hour

        device_ids = self.env['temperature.device'].search([]).mapped('serial_no')

        for device_id in device_ids:
            try:
                # Fetch data for each device
                response = requests.get(f'{proxy_history_url}/{device_id}', headers=headers, params={
                    'token': token,
                    'start_time': start_time,
                    'end_time': end_time
                })
                response.raise_for_status()
                data = response.json()

                # Log the actual response
                _logger.info(f"Response for device {device_id}: {data}")

                if 'body' not in data or 'dataList' not in data['body']:
                    _logger.error(f'Invalid response format for device {device_id}: {data}')
                    continue  # Skip to the next device

                sensor_data_model = self.env['sensor.data']
                temperature_device_model = self.env['temperature.device']

                for item in data['body']['dataList']:
                    device_record = temperature_device_model.search([('device_id', '=', device_id)], limit=1)
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
            except requests.RequestException as e:
                _logger.error(f"Failed to fetch data for device {device_id}: {e}")
                raise
