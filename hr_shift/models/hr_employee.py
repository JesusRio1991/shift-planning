from odoo import models
from datetime import timedelta

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    def generate_shifts_from_pattern(self):
        shift_obj = self.env['hr.shift.planning.shift']
        for employee in self:
            pattern = employee.shift_pattern_id
            if not pattern:
                continue
            for line in pattern.line_ids:
                if line.is_rest:
                    continue
                # Crear el turno asociando el empleado y la plantilla
                shift = shift_obj.create({
                    'employee_id': employee.id,
                    'template_id': line.shift_template_id.id,
                    # 'planning_id': None,  # opcional
                })
                shift._generate_shift_lines()
        return True
