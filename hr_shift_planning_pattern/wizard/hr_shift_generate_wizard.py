from odoo import models, fields, api
from datetime import datetime, timedelta, time
from odoo.exceptions import UserError

class HrShiftGenerateWizard(models.TransientModel):
    _name = 'hr.shift.generate.wizard'
    _description = 'Generate Shifts From Pattern'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
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

        current_date = self.start_date

        while current_date <= self.end_date:

            # Elegir la línea del patrón según posición
            day_index = (current_date - self.start_date).days % len(pattern_lines)
            pattern_line = pattern_lines[day_index]

            # Saltar días de descanso
            if not pattern_line.is_rest:

                template = pattern_line.shift_template_id

                # Convertir horas float → datetime
                start_hour = int(template.start_time)
                start_minute = int((template.start_time % 1) * 60)
                end_hour = int(template.end_time)
                end_minute = int((template.end_time % 1) * 60)

                start_dt = datetime.combine(current_date, time(start_hour, start_minute))
                end_dt = datetime.combine(current_date, time(end_hour, end_minute))

                # Crear turno
                self.env['hr.shift.planning.shift'].create({
                    'employee_id': employee.id,
                    'start_datetime': start_dt,
                    'end_datetime': end_dt,
                    'template_id': template.id,
                })

            current_date += timedelta(days=1)

        return {'type': 'ir.actions.act_window_close'}
