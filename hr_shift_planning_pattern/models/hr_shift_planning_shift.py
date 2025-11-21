from datetime import datetime, timedelta, time

class HrShiftPlanningShift(models.Model):
    _inherit = "hr.shift.planning.shift"

    @api.model
    def generate_shifts_from_pattern(self, employee, pattern, start_date, end_date):
        """Genera las líneas de turno para un empleado usando un patrón"""
        shift_obj = self.env['hr.shift.planning.shift']

        # Crear el shift semanal del empleado
        shift = shift_obj.create({
            'employee_id': employee.id,
        })

        # Recorrer cada día entre start_date y end_date
        current_date = start_date
        while current_date <= end_date:
            weekday = str(current_date.isoweekday())  # 1=lunes ... 7=domingo
            line_template = pattern.line_ids.filtered(lambda l: l.day_number == weekday)
            if line_template:
                self.env['hr.shift.planning.line'].create({
                    'shift_id': shift.id,
                    'template_id': line_template.template_id.id,
                    'day_number': weekday,
                    'start_date': current_date,
                })
            current_date += timedelta(days=1)
        return True
