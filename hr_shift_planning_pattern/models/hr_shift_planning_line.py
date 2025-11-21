# models/hr_shift_planning_line.py
from odoo import models, fields

class HrShiftPlanningLine(models.Model):
    _name = 'hr.shift.planning.line'
    _description = 'Línea de turno'

    shift_id = fields.Many2one('hr.shift.planning.shift', string="Turno")
    employee_id = fields.Many2one('hr.employee', string="Empleado")
    template_id = fields.Many2one('hr.shift.template', string='Plantilla de turno')
    date_start = fields.Datetime(string="Inicio")
    date_end = fields.Datetime(string="Fin")
