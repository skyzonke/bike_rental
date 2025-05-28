from odoo import models, fields, api, exceptions


class StationModel(models.Model):
    _name = 'bike.station'
    _description = 'The model for the station model'
    _order = 'name desc'

    name = fields.Char(required=True)
    address = fields.Char()
    technician_id = fields.Many2one('res.users', string="Technicien responsable")
    capacity = fields.Integer(string="Capacité maximale", default=10)
    bike_ids = fields.One2many('bike.bike', 'station_id', string="Vélos")
    available_bike_count = fields.Integer(string="Vélos disponibles", compute='_compute_bike_counts')
    rented_bike_count = fields.Integer(string="Vélos loués", compute='_compute_bike_counts')
    maintenance_bike_count = fields.Integer(string="Vélos en maintenance", compute='_compute_bike_counts')

    @api.depends('bike_ids.state')
    def _compute_bike_counts(self):
        for station in self:
            station.available_bike_count = len(station.bike_ids.filtered(lambda b: b.state == 'available'))
            station.rented_bike_count = len(station.bike_ids.filtered(lambda b: b.state == 'rented'))
            station.maintenance_bike_count = len(station.bike_ids.filtered(lambda b: b.state == 'maintenance'))

    @api.constrains('bike_ids', 'capacity')
    def _check_capacity(self):
        for station in self:
            if len(station.bike_ids) > station.capacity:
                raise exceptions.ValidationError("La station a dépassé sa capacité maximale.")
