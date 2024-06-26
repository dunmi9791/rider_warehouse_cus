from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    app_id = fields.Char(string='App ID')
    app_key = fields.Char('App Key')
    app_secret = fields.Char('App Secret')

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            app_id=self.env['ir.config_parameter'].sudo().get_param('sensor_data_import.app_id'),
            app_key=self.env['ir.config_parameter'].sudo().get_param('sensor_data_import.app_key'),
            app_secret=self.env['ir.config_parameter'].sudo().get_param('sensor_data_import.app_secret'),
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('sensor_data_import.app_id', self.app_id)
        self.env['ir.config_parameter'].sudo().set_param('sensor_data_import.app_key', self.app_key)
        self.env['ir.config_parameter'].sudo().set_param('sensor_data_import.app_secret', self.app_secret)
