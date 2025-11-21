from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import timedelta

class HrShiftGenerateWizard(models.TransientModel):
    _name = "hr.shift.generate.wizard"
    _description = "Generate Employee Shifts from Pattern"

    employee_id = fields.Many2one('hr.employee', required=True)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)

    def action_generate_shifts(self):
        self.ensure_one()
        employee = self.employee_id
        pattern = employee.shift_pattern_id
        if not pattern:
            raise UserError("El empleado no tiene un patrón asignado.")
        
        # Generar los turnos
        self.env['hr.shift.planning.shift'].generate_shifts_from_pattern(
            employee, pattern, self.start_date, self.end_date
        )
        return {'type': 'ir.actions.act_window_close'}
