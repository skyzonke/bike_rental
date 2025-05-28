from odoo import models, fields, api, exceptions
from dateutil.relativedelta import relativedelta

class BikeRental(models.Model):
    _name = 'bike.bike'
    _description = 'The model for bike module'

    name = fields.Char(required=True)
    state = fields.Selection([
        ('available', 'Disponible'),
        ('rented', 'Loué'),
        ('maintenance', 'En maintenance'),
    ], default='available', required=True)
    station_id = fields.Many2one('bike.station', string="Station de rattachement")
    rental_ids = fields.One2many('bike.rental', 'bike_id', string="Locations")

    def action_set_maintenance(self):
        for bike in self:
            bike.state = 'maintenance'
            # Annuler les locations futures
            future_rentals = bike.rental_ids.filtered(
                lambda r: r.date_start > fields.Datetime.now() and r.state == 'confirmed')
            for rental in future_rentals:
                rental.state = 'cancelled'

