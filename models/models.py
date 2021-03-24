# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions

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


class Session(models.Model):
    _name = 'openacademy.session'

    name = fields.Char(required=True)
    start_date = fields.Date(default=fields.Date.today)
    duration = fields.Float(digits=(6, 2), help="Duration in day")
    seats = fields.Integer(string="Number of seats")
    active = fields.Boolean(default=True)
    taken_seats = fields.Float(string="Taken seats",
                                      compute="_taken_seats")

    instructor_id = fields.Many2one('res.partner', string="Instructor",
                    domain=['|',
                            ('instructor', '=', True),
                            ('category_id.name', 'like', 'Teacher')]
                                    )
    course_id = fields.Many2one('openacademy.course', ondelete="cascade",
                                string="Course", required=True)
    attendee_ids = fields.Many2many('res.partner', string="attendee")

    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for r in self:
            # Si no se han ingresado sillas
            if not r.seats:
                r.taken_seats = 0.0
            # Calculo el porcentaje de sillas
            else:
                r.taken_seats = 100 * len(r.attendee_ids) / r.seats

    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            self.seats = 0
            return {
                'warning': {
                    'title': "Incorrect 'seats' value",
                    'message': "The number of available seats my no be negative"
                },
            }
        if self.seats < len(self.attendee_ids):
            return {
                'warning': {
                    'title': "Too many attendees",
                    'message': "Increse seats or remove excess attendees",
                },
            }

    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendees(self):
        for r in self:
            if r.instructor_id and r.instructor_id in r.attendee_ids:
                raise exceptions.ValidationError("A session's instructor can't be an attendee")

