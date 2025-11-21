{
    "name": "HR Shift Planning Patterns",
    "version": "17.0.1.0.1",
    "summary": "Add cyclic shift patterns",
    "category": "Human Resources",
    "author": "Jesús Río",
    "license": "AGPL-3",
    "depends": ["hr", "hr_shift"],
    "data": [
        "security/ir.model.access.csv",
        "views/hr_shift_planning_pattern_views.xml",
        "views/hr_shift_planning_pattern_menu.xml",
        "views/hr_employee_views.xml",
        'views/hr_shift_views.xml',
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
