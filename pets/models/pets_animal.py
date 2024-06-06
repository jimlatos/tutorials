from odoo import models, fields, api, exceptions

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
    unique_name = fields.Char(compute="_compute_unique_name", store=True, unique=True)

    
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

    @api.depends('name', 'owner_id')
    def _compute_unique_name(self):
        for record in self:
            if record.name and record.owner_id:
                record.unique_name = f'{record.name}-{record.owner_id.id}'
            else:
                record.unique_name = ''

    @api.constrains('unique_name')
    def _check_unique_name(self):
        for record in self:
            if record.unique_name and not self.env['pets.animal'].search([['unique_name', '=', record.unique_name]]):
                raise exceptions.ValidationError("This name is already taken by another pet of this owner.")
            elif not record.unique_name and record.name and record.owner_id:
                raise exceptions.ValidationError("The unique name field must be set for records with a name and an owner.")