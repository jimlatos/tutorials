from odoo import fields, models

class PetsWeight(models.Model):
    _name = "pets.weight"
    _description = "Weight records"

    date = fields.Date(required=True)
    animal_id = fields.Many2one("pets.animal", string="Animal", required=True)
    weight = fields.Float(required=True)