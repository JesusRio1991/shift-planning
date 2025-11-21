from odoo import models, fields

class HrShiftPlanningPatternLine(models.Model):
    _name = 'hr.shift.planning.pattern.line'
    _description = 'Línea de patrón de turno'

    pattern_id = fields.Many2one('hr.shift.planning.pattern', string="Patrón")
    day_number = fields.Integer(string="Día")
    shift_template_id = fields.Many2one('hr.shift', string="Plantilla de turno")
    is_rest = fields.Boolean(string="Descanso")
