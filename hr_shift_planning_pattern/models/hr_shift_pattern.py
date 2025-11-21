# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta, date as date_class

class HrShiftPattern(models.Model):
    _name = "hr.shift.pattern"
    _description = "Shift Pattern"

    name = fields.Char(required=True)
    cycle_length = fields.Integer(string="Cycle length (days)", default=8, required=True)
    line_ids = fields.One2many('hr.shift.pattern.line', 'pattern_id', string="Pattern lines", copy=True)
    employee_id = fields.Many2one('hr.employee', string="Employee", help="If empty pattern can be used for many employees")
    start_date = fields.Date(default=fields.Date.context_today, required=True)
    auto_generate = fields.Boolean(string="Auto generate", help="If checked a cron may generate shifts automatically")

    def _create_planning_shift(self, employee, template, the_date):
        """Create a hr.shift.planning.shift (adapt to fields available)."""
        Shift = self.env['hr.shift.planning.shift']
        vals = {
            'employee_id': employee.id,
            'shift_template_id': template.id if template else False,
            'date': the_date,
        }
        # Some modules might expect start/end datetime; adapt if needed.
        return Shift.create(vals)

    def generate_shifts(self, date_to=None):
        """Generate shifts from start_date up to date_to (inclusive). If date_to None, generate for 30 days."""
        self.ensure_one()
        if not date_to:
            date_to = fields.Date.to_string(fields.Date.context_today(self.env) + timedelta(days=30))
        date_from = fields.Date.to_date(self.start_date)
        if isinstance(date_to, str):
            date_to = fields.Date.to_date(date_to)

        # get employee(s)
        employees = self.employee_id and self.employee_id.filtered(lambda r: r) or self.env['hr.employee'].browse(self.env.context.get('employee_ids', []))
        # if no employees in context and no employee_id, raise? we'll default to apply to all employees if none set
        if not employees:
            # apply to all employees? safer: require employee or pass employee_ids in context
            employees = self.env['hr.employee'].search([])

        current = date_from
        while current <= date_to:
            offset_days = (current - date_from).days
            day_num = (offset_days % self.cycle_length) + 1
            line = self.line_ids.filtered(lambda l: l.day_number == day_num)
            if line:
                if not line.is_rest and line.shift_template_id:
                    for emp in employees:
                        # check duplicate: don't create if exists same employee/date and same template
                        exists = self.env['hr.shift.planning.shift'].search([
                            ('employee_id', '=', emp.id),
                            ('date', '=', fields.Date.to_string(current)),
                            ('shift_template_id', '=', line.shift_template_id.id)
                        ], limit=1)
                        if not exists:
                            self._create_planning_shift(emp, line.shift_template_id, fields.Date.to_string(current))
            current = current + timedelta(days=1)

    @api.model
    def cron_generate_all_patterns(self, days_ahead=30):
        """Method runnable by cron to generate patterns for all with auto_generate True."""
        date_to = fields.Date.to_string(fields.Date.context_today(self.env) + timedelta(days=days_ahead))
        patterns = self.search([('auto_generate', '=', True)])
        for p in patterns:
            p.generate_shifts(date_to=date_to)
