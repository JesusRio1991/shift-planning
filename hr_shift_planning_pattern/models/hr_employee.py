from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import date, timedelta
import logging

_logger = logging.getLogger(__name__)

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    shift_pattern_id = fields.Many2one(
        'hr.shift.planning.pattern',
        string="Shift Pattern"
    )

    def generate_shifts_from_pattern(self, days_to_generate=14):
        """Genera los turnos de los empleados según su patrón para un rango de días"""
        shift_obj = self.env['hr.shift.planning.shift']

        for employee in self:
            pattern = employee.shift_pattern_id
            if not pattern:
                _logger.warning("Empleado %s no tiene patrón de turno asignado.", employee.name)
                continue

            start_date = date.today()
            end_date = start_date + timedelta(days=days_to_generate)

            for line in pattern.line_ids:
                if line.is_rest:
                    _logger.debug("Empleado %s: línea de descanso, se omite.", employee.name)
                    continue

                template = line.shift_template_id
                if not template:
                    _logger.warning("Empleado %s: línea del patrón sin template, se omite.", employee.name)
                    continue

                # Crear el shift solo con template y empleado
                shift = shift_obj.create({
                    'employee_id': employee.id,
                    'template_id': template.id,
                })

                # Genera automáticamente las líneas del turno usando un rango de fechas
                try:
                    shift._generate_shift_lines(start_date=start_date, end_date=end_date)
                except Exception as e:
                    _logger.error(
                        "Error generando líneas de turno para empleado %s con template %s: %s",
                        employee.name,
                        template.name,
                        e
                    )

        return True
