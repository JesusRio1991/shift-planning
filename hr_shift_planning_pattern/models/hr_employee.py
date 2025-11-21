from odoo import models, fields  # <-- agrega fields

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    shift_pattern_id = fields.Many2one(
        'hr.shift.planning.pattern',
        string="Shift Pattern"
    )

    def generate_shifts_from_pattern(self):
        shift_obj = self.env['hr.shift.planning.shift']
        for employee in self:
            pattern = employee.shift_pattern_id
            if not pattern:
                continue
            for line in pattern.line_ids:
                if line.is_rest:
                    continue
                shift = shift_obj.create({
                    'employee_id': employee.id,
                    'template_id': line.shift_template_id.id,
                })
                # Genera automáticamente las líneas del turno con fechas y horas
                shift._generate_shift_lines()
        return True
