from odoo import models, fields

class HrShiftPlanningPattern(models.Model):
    _name = 'hr.shift.planning.pattern'
    _description = 'Patrón de planificación de turnos'

    name = fields.Char(string='Nombre', required=True)

    line_ids = fields.One2many(
        'hr.shift.planning.pattern.line',
        'pattern_id',
        string="Líneas del patrón",
        copy=True
    )
