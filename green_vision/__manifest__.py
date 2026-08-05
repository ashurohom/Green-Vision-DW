{
    "name": "GreenVision",
    "version": "18.0.1.0.0",
    "summary": "GreenVision Test Module",

    "author": "GreenVision",
    "website": "https://www.greenvision.in",

    "category": "Sales",

    "license": "LGPL-3",

    "depends": [
        "base",
        "sale_management",
        "stock",
        "purchase",
        "account",
        "hr_expense",
    ],

    "data": [
        "views/dashboard_views.xml",
    ],

    "assets": {
        "web.assets_backend": [
            "green_vision/static/src/css/dashboard.css",
            "green_vision/static/src/js/dashboard.js",
            "green_vision/static/src/xml/dashboard.xml",
        ],
    },

    "installable": True,
    "application": True,
    "auto_install": False,
}