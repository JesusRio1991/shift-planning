from odoo import models, fields, api
from datetime import timedelta

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    shift_pattern_id = fields.Many2one(
        'hr.shift.planning.pattern',
        string='Patrón de turno',
        help='Patrón de turnos asignado a este empleado.'
    )

    def generate_shifts_from_pattern(self):
        shift_obj = self.env['hr.shift.planning.shift']
        for employee in self:
            pattern = employee.shift_pattern_id
            if not pattern:
                continue
            start_date = pattern.start_date
            for line in pattern.line_ids:
                if not line.is_rest:
                    shift_obj.create({
                        'employee_id': employee.id,
                        'date': start_date + timedelta(days=line.day_number - 1),
                        'shift_template_id': line.shift_template_id.id,
                    })
        return True
