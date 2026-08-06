{
    'name': 'Employee Performance Management',
    'version': '18.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Complete Employee Performance Management System based on KRA, KPA, KPI',
    'description': """
        Employee Performance Management
        ===============================
        A clean, scalable, and modular performance management system.
        
        Features:
        - KRAs, KPAs, KPIs management
        - Configurable Rating Scales
        - Review Cycles
        - Performance Templates
        - Employee Assignments
        - Self & Manager Reviews
        - Automatic Score Calculations
        - Final Evaluation
    """,
    'author': 'Expert Odoo Developer',
    'depends': ['hr', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/menu.xml',
        'views/kpi_views.xml',
        'views/kpa_views.xml',
        'views/kra_views.xml',
        'views/review_cycle_views.xml',
        'views/rating_scale_views.xml',
        'views/performance_template_views.xml',
        'views/employee_assignment_views.xml',
        'views/self_review_views.xml',
        'views/manager_review_views.xml',
        'views/final_evaluation_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
