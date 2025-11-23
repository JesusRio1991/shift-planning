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
        """
        Genera turnos para un empleado según un patrón (6+2 o cualquier pattern).
        Crea:
            - hr.shift.planning por semana
            - hr.shift.planning.shift para el empleado
            - hr.shift.planning.line por día
        """
        self.ensure_one()

        employee = self.employee_id
        pattern = employee.shift_pattern_id

        if not employee:
            raise UserError("Debe seleccionar un empleado.")

        if not pattern:
            raise UserError("El empleado no tiene un patrón asignado.")

        pattern_lines = pattern.line_ids.sorted("day")
        if not pattern_lines:
            raise UserError("El patrón no tiene líneas definidas.")

        # Preparar fechas
        current_date = self.start_date
        end_date = self.end_date

        # Grupo de lines por index para acceso rápido
        pattern_length = len(pattern_lines)

        # Recorrer día a día
        while current_date <= end_date:

            # Calcular año y semana ISO de este día
            iso_year, iso_week, _ = current_date.isocalendar()

            # Buscar si ya existe planning para esta semana
            planning = self.env["hr.shift.planning"].search([
                ("year", "=", iso_year),
                ("week_number", "=", iso_week)
            ], limit=1)

            if not planning:
                # Crear nuevo planning semanal
                planning = self.env["hr.shift.planning"].create({
                    "year": iso_year,
                    "week_number": iso_week,
                })

            # Buscar/crear shift del empleado para esta semana
            shift = self.env["hr.shift.planning.shift"].search([
                ("planning_id", "=", planning.id),
                ("employee_id", "=", employee.id),
            ], limit=1)

            if not shift:
                shift = self.env["hr.shift.planning.shift"].create({
                    "planning_id": planning.id,
                    "employee_id": employee.id,
                })

            # ———————————————————————————————
            # Determinar qué turno toca según pattern
            # ———————————————————————————————
            day_offset = (current_date - self.start_date).days % pattern_length
            pattern_line = pattern_lines[day_offset]

            if not pattern_line.is_rest:
                # Insertar línea de turno diario
                self.env["hr.shift.planning.line"].create({
                    "shift_id": shift.id,
                    "template_id": pattern_line.shift_template_id.id,
                    "day_number": str(current_date.weekday()),
                    "start_time": datetime.combine(current_date, time(
                        int(pattern_line.shift_template_id.start_time),
                        int((pattern_line.shift_template_id.start_time % 1) * 60)
                    )),
                    "end_time": datetime.combine(current_date, time(
                        int(pattern_line.shift_template_id.end_time),
                        int((pattern_line.shift_template_id.end_time % 1) * 60)
                    )),
                })

            # Avanzar un día
            current_date += timedelta(days=1)

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "Turnos generados",
                "message": "Los turnos se han generado correctamente.",
                "type": "success",
                "sticky": False,
            },
        }