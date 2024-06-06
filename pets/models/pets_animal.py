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
    vaccine_ids = fields.One2many("pets.vaccine", "animal_id", string="Vaccines")
    # unique_name = fields.Char(compute="_compute_unique_name", store=True, unique=True)

    
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

    # @api.depends('name', 'owner_id')
    # def _compute_unique_name(self):
    #     for record in self:
    #         if record.name and record.owner_id:
    #             record.unique_name = f'{record.name}-{record.owner_id.id}'
    #         else:
    #             record.unique_name = ''

    @api.constrains('name', 'owner_id') # tells Odoo to run this method when the name or owner_id fields are changed. If the method raises an exception, the changes will be rolled back.
    def _check_unique_name(self):
        for record in self:
            domain = [('owner_id', '=', record.owner_id.id), ('name', '=', record.name)]
            existing = self.env['pets.animal'].search_count(domain)
            if existing > 1:
                raise exceptions.ValidationError(f'The name {record.name} is already used for an animal of the owner {record.owner_id.name}')
            

class Vaccine(models.Model):
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