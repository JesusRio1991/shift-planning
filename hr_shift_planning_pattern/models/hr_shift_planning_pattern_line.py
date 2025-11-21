from odoo import models, fields, api

class HrShiftPlanningPatternLine(models.Model):
    _name = 'hr.shift.planning.pattern.line'
    _description = 'Línea de patrón de turno'
    _order = 'day_number asc'

    pattern_id = fields.Many2one('hr.shift.planning.pattern', string="Patrón", required=True)
    day_number = fields.Integer(string="Día", required=True)
    shift_template_id = fields.Many2one('hr.shift.template', string='Plantilla de turno')

    is_rest = fields.Boolean(string="Descanso")

    _sql_constraints = [
        ('unique_day_pattern',
         'unique(pattern_id, day_number)',
         'Cada día solo puede aparecer una vez por patrón.')
    ]

    @api.onchange('is_rest')
    def _onchange_is_rest(self):
        if self.is_rest:
            self.shift_template_id = False
