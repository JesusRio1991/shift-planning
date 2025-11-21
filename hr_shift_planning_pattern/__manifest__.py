# -*- coding: utf-8 -*-
{
    "name": "HR Shift Planning Patterns",
    "summary": "Add cyclic shift patterns (6+2, 2M/2T/2N/2D, etc.)",
    "version": "17.0.1.0.0",
    "category": "Human Resources",
    "author": "Jesus Rio / Fork",
    "license": "AGPL-3",
    "depends": [
        "hr_shift_planning",
        "hr"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/hr_shift_pattern_views.xml",
        "data/cron_data.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
