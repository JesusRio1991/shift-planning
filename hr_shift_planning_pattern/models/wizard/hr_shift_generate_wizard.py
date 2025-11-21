from odoo import models, fields, api

class HrShiftGenerateWizard(models.TransientModel):
    _name = 'hr.shift.generate.wizard'
    _description = 'Wizard to Generate Shifts'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)

    def action_generate_shifts(self):
        # Aquí llamas a tu método generate_shifts_from_pattern
        self.employee_id.generate_shifts_from_pattern(self.start_date, self.end_date)
        return {'type': 'ir.actions.act_window_close'}
