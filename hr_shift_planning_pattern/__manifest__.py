{
    "name": "HR Shift Planning Patterns",
    "version": "17.0.1.0.0",
    "summary": "Add cyclic shift patterns (6+2, 2M/2T/2N/2D, etc.)",
    "category": "Human Resources",
    "author": "Jesús Río / Fork",
    "license": "AGPL-3",
    "depends": ["hr", "hr_shift"],
    "data": [
        "security/ir.model.access.csv",
        "views/hr_shift_planning_pattern_views.xml",
        "views/hr_shift_planning_pattern_menu.xml",
        # "data/cron_data.xml",   # opcional, si luego quieres auto-generar turnos
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
