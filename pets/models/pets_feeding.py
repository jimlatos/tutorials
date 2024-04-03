from odoo import fields, models

class PetsFeeding(models.Model):
    _name = "pets.feeding"
    _description = "Feeding records"

    date = fields.Date(required=True, default=fields.Date.today)
    time = fields.Datetime(default=fields.Datetime.now)
    animal_id = fields.Many2one("pets.animal", string="Animal", required=True)
    #animal_name = fields.Char(related="animal_id.name")
    meal = fields.Selection([
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner')
    ], required=True)
    notes = fields.Text()