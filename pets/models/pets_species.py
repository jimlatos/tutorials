from odoo import fields, models

class PetsSpecies(models.Model):
    _name = "pets.species"
    _description = "Species"

    name = fields.Char(required=True)
    image = fields.Binary()
    description = fields.Text()
    animal_ids = fields.One2many("pets.animal", "species_id", string="Animals")
    animal_count = fields.Integer(compute="_compute_animal_count")

    def _compute_animal_count(self):
        for record in self:
            record.animal_count = len(record.animal_ids)