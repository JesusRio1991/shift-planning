# models/hr_employee.py
from odoo import models, fields

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    shift_pattern_id = fields.Many2one(
        'hr.shift.planning.pattern',
        string='Patrón de turno',
        help='Patrón de turnos asignado a este empleado.'
    )
