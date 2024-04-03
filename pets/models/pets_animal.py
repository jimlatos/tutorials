from odoo import fields, models

class PetsAnimal(models.Model):
    _name = "pets.animal"
    _description = "Animals"

    name = fields.Char(required=True)
    birth_date = fields.Date()
    age = fields.Integer(compute="_compute_age", store=False)
    image = fields.Binary()
    species_id = fields.Many2one("pets.species", string="Species")
    species_name = fields.Char(related="species_id.name")
    owner_id = fields.Many2one("res.users", string="Owner")
    owner_name = fields.Char(related="owner_id.name")
    weight_ids = fields.One2many("pets.weight", "animal_id", string="Weights")
    weight = fields.Float(compute="_compute_weight")
    notes = fields.Text()
    active = fields.Boolean(default=True)

    concatenated_name = fields.Char(compute="_compute_concatenated_name")

    
    def action_show_feeding_records(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Feeding Records",
            "res_model": "pets.feeding",
            "views": [[False, "tree"], [False, "form"]],
            "domain": [["animal_id", "=", self.id]],
        }
    
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                record.age = (fields.Date.today() - record.birth_date).days // 365
            else:
                record.age = 0

    def _compute_weight(self):
        for record in self:
            weight_record = record.weight_ids.sorted(key=lambda r: r.date, reverse=True)
            record.weight = weight_record[0].weight if weight_record else 0

    @api.constraints("species_id")
    def _check_species_id(self):
        if not self.species_id:
            raise ValidationError("Species is required")
        
    @api.depends('name', 'owner_id')
    def _compute_concatenated_name(self):
        for record in self:
            record.concatenated_name = f"{record.name}-{record.owner_id.name}"