# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Course(models.Model):
    _name = 'openacademy.course'
    _description = 'Guardamos todos los cursos disponibles'

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")

    responsible_id = fields.Many2one('res.users',
                   ondelete="set null", string="Responsible", index=True)
    session_id = fields.One2many(
        'openacademy.session', 'course_id', string="Sessions")

    # Restricciones de SQL
    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         'The title of the course should not be the description'),

        ('name_unique',
         'UNIQUE(name)',
         "The course tittle mut be unique"),
    ]

    # Campos para probar el Onchange
    amount = fields.Integer()
    unit_price = fields.Integer()
    price = fields.Integer()


    # ---------------- MÉTODOS ----------------

    @api.multi
    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', u"Copy of {}%".format(self.name))]
        )

        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)

        default['name'] = new_name
        return super(Course, self).copy(default)



    @api.onchange('amount', 'unit_price')
    def _onchange_price(self):
        # set auto-chaging field
        self.price = self.amount * self.unit_price
        # Can optionally return a warning and domains
        # Opcionalmente, puede devolver una advertencia y dominios.
        # return {
        #     'warning': {
        #         'title': "Something bad happened",
        #         'message': "It was very bad indeed",
        #     },
        # }
