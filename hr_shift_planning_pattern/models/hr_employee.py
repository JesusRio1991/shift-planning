from odoo import models, fields, api
from datetime import date, timedelta, datetime, time

import logging

_logger = logging.getLogger(__name__)

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    shift_pattern_id = fields.Many2one(
        'hr.shift.planning.pattern',
        string="Shift Pattern"
    )

    def generate_shifts_from_pattern(self, days_to_generate=14):
        """Crea un turno de prueba de un día para el empleado"""
        shift_obj = self.env['hr.shift.planning.shift']

        for employee in self:
            # Tomamos el primer template del patrón si existe
            pattern = employee.shift_pattern_id
            if not pattern or not pattern.line_ids:
                _logger.warning("Empleado %s no tiene patrón de turno asignado.", employee.name)
                continue

            template = pattern.line_ids[0].shift_template_id
            if not template:
                _logger.warning("Empleado %s: plantilla de turno no definida.", employee.name)
                continue

            # Crear el shift
            shift = shift_obj.create({
                'employee_id': employee.id,
                'template_id': template.id,
            })
            
            hours = int(template.start_time)
            minutes = int((template.start_time % 1) * 60)
            start_dt = datetime.combine(date.today(), time(hour=hours, minute=minutes))

            hours = int(template.end_time)
            minutes = int((template.end_time % 1) * 60)
            end_dt = datetime.combine(date.today(), time(hour=hours, minute=minutes))

            self.env['hr.shift.planning.line'].create({
                'shift_id': shift.id,
                'employee_id': employee.id,
                'template_id': template.id,
                'date_start': start_dt,
                'date_end': end_dt,
            })

            _logger.info("Turno de prueba creado para %s: %s - %s", employee.name, start_dt, end_dt)

        return True

