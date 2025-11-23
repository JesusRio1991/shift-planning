from odoo import models, fields
from datetime import datetime, timedelta, time
from odoo.exceptions import UserError

class HrShiftGenerateWizard(models.TransientModel):
    _name = 'hr.shift.generate.wizard'
    _description = 'Generate Shifts From Pattern'

    employee_id = fields.Many2one('hr.employee', required=True)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)

    def action_generate_shifts(self):
        self.ensure_one()

        employee = self.employee_id
        pattern = employee.shift_pattern_id

        if not pattern:
            raise UserError("El empleado no tiene ningún patrón asignado.")

        pattern_lines = pattern.line_ids.sorted('day')

        if not pattern_lines:
            raise UserError("El patrón no tiene líneas definidas.")

        # Una sola planificación para todo el rango
        planning = self.env['hr.shift.planning'].create({
            'employee_id': employee.id,
            'start_date': self.start_date,
        })

        current_date = self.start_date

        while current_date <= self.end_date:

            # Posición dinámica dentro del patrón (para 6+2 se mueve cada semana)
            offset = (current_date - self.start_date).days % len(pattern_lines)
            pattern_line = pattern_lines[offset]

            if not pattern_line.is_rest:

                template = pattern_line.shift_template_id

                # Crear turno individual por día
                self.env['hr.shift.planning.line'].create({
                    'shift_id': planning.id,
                    'template_id': template.id,
                    'date': current_date,
                })

            current_date += timedelta(days=1)

        return {'type': 'ir.actions.act_window_close'}
