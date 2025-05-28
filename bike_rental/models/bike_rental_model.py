from odoo import models, fields, api, exceptions
from dateutil.relativedelta import relativedelta

class BikeRental(models.Model):
    _name = 'bike.rental'
    _description = 'The model for bike rental module'

    user_id = fields.Many2one('res.users', string="Utilisateur", required=True)
    bike_id = fields.Many2one('bike.bike', string="Vélo", required=True)
    date_start = fields.Datetime(string="Début", required=True)
    date_end = fields.Datetime(string="Fin", required=True)
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('confirmed', 'Confirmée'),
        ('ongoing', 'En cours'),
        ('done', 'Terminée'),
        ('cancelled', 'Annulée'),
    ], default='draft', required=True)

    @api.constrains('bike_id', 'date_start', 'date_end', 'state')
    def _check_bike_availability(self):
        for rec in self:
            if rec.bike_id.state == 'maintenance':
                raise exceptions.ValidationError("Ce vélo est en maintenance et ne peut pas être réservé.")
            overlapping = self.search([
                ('bike_id', '=', rec.bike_id.id),
                ('id', '!=', rec.id),
                ('state', 'in', ['confirmed', 'ongoing']),
                ('date_start', '<', rec.date_end),
                ('date_end', '>', rec.date_start),
            ])
            if overlapping:
                raise exceptions.ValidationError("Ce vélo est déjà réservé sur cette période.")