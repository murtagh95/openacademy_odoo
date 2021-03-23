# -*- coding: utf-8 -*-
from pygments.lexer import _inherit

from odoo import models, fields

class Partner(models.Model):
    _inherit = 'res.partner'

    # Add a new column to the res.partner model, by default partners are not
    # instructors
    instructor = fields.Boolean("Instructor", default=False)
    session_ids = fields.Many2many('openacademy.session',
                  string="Attended Sessions", readonlu=True)


