from odoo import models, fields, api
from datetime import timedelta

class HrShiftPlanningPattern(models.Model):
    _name = 'hr.shift.planning.pattern'
    _description = 'Patrón de planificación de turnos'

    name = fields.Char(string="Nombre", required=True)
    cycle_length = fields.Integer(string="Duración del ciclo")
    start_date = fields.Date(string="Fecha inicio")
    auto_generate = fields.Boolean(string="Auto-generar")
    line_ids = fields.One2many('hr.shift.planning.pattern.line', 'pattern_id', string="Líneas del patrón")

    def generate_shifts(self):
        # método vacío solo para compatibilidad con la vista
        return True

    @api.model
    def generate_shifts_for_employees(self):
        """
        Genera turnos en hr.shift.planning.shift para todos los empleados
        que tengan asignado este patrón.
        """
        shift_obj = self.env['hr.shift.planning.shift']
        employees = self.env['hr.employee'].search([('shift_pattern_id', '!=', False)])
        for employee in employees:
            pattern = employee.shift_pattern_id
            start_date = pattern.start_date
            for line in pattern.line_ids:
                if not line.is_rest:
                    shift_obj.create({
                        'employee_id': employee.id,
                        'date': start_date + timedelta(days=line.day_number - 1),
                        'shift_template_id': line.shift_template_id.id,
                    })
        return True
