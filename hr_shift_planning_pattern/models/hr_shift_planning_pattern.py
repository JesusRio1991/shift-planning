from odoo import models, fields

class HrShiftPlanningPattern(models.Model):
    _name = 'hr.shift.planning.pattern'
    _description = 'Patrón de planificación de turnos'

    name = fields.Char(string="Nombre", required=True)
    cycle_length = fields.Integer(string="Duración del ciclo")
    start_date = fields.Date(string="Fecha inicio")
    employee_id = fields.Many2one('hr.employee', string="Empleado")
    auto_generate = fields.Boolean(string="Auto-generar")
    line_ids = fields.One2many('hr.shift.planning.pattern.line', 'pattern_id', string="Líneas del patrón")

    def generate_shifts(self):
        # método vacío para que la vista cargue
        print("Generar turnos ejecutado")  
        return True
