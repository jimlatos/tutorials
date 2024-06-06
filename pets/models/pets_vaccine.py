from odoo import models, fields

class PetsVaccine(models.Model):
    _name = "pets.vaccine"
    _description = "Vaccines"

    name = fields.Char(required=True)
    animal_id = fields.Many2one("pets.animal", string="Animal", required=True)
    date = fields.Date(required=True)
    expiration_date = fields.Date()
    notes = fields.Text()
    status = fields.Text(compute="_compute_status")

    def _compute_status(self):
        for record in self:
            if record.expiration_date:
                if record.expiration_date < fields.Date.today():
                    record.status = "Expired"
                else:
                    record.status = "Valid"
            else:
                record.status = "Valid"