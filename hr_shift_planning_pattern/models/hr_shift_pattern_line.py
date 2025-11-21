# -*- coding: utf-8 -*-
from odoo import models, fields

class HrShiftPatternLine(models.Model):
    _name = "hr.shift.pattern.line"
    _description = "Shift Pattern Line"
    _order = "day_number asc"

    pattern_id = fields.Many2one('hr.shift.pattern', string="Pattern", required=True, ondelete='cascade')
    day_number = fields.Integer(required=True, help="Day in the cycle (1..cycle_length)")
    shift_template_id = fields.Many2one('hr.shift.template', string="Shift template", help="Template to use for this day")
    is_rest = fields.Boolean(string="Rest", help="If checked, no shift will be created on this day")
