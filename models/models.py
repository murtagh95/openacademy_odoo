# -*- coding: utf-8 -*-

from odoo import models, fields

class Course(models.Model):
    _name = 'openacademy.course'
    _description = 'Guardamos todos los cursos disponibles'

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")

    responsible_id = fields.Many2one('res.users',
                   ondelete="set null", string="Responsible", index=True)
    session_id = fields.One2many(
        'openacademy.session', 'course_id', string="Sessions")

class Session(models.Model):
    _name = 'openacademy.session'

    name = fields.Char(required=True)
    start_date = fields.Date()
    duration = fields.Float(digits=(6, 2), help="Duration in day")
    seats = fields.Integer(string="Number of seats")

    instructor_id = fields.Many2one('res.partner', string="Instructor",
                    domain=['|',
                            ('instructor', '=', True),
                            ('category_id.name', 'like', 'Teacher')]
                                    )
    course_id = fields.Many2one('openacademy.course', ondelete="cascade",
                                string="Course", required=True)
    attendee_ids = fields.Many2many('res.partner', string="attendee")


