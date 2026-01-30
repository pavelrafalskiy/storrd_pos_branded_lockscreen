{
    "name": "Storrd POS Branded Lockscreen",
    "version": "1.0",
    "category": "Sales/Point of Sale",
    "summary": "Replace the default Odoo logo on the POS Saver Screen with a custom branded image.",
    "description":
        """
        This module allows users to upload a custom image in the POS settings
        to be displayed on the Lock Screen (Saver Screen) instead of the standard Odoo logo.
        """,
    "author": "Storrd",
    "depends": ["point_of_sale"],
    "data": [
        "views/res_config_settings_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "storrd_pos_branded_lockscreen/static/src/js/binary_field_validation.js",
        ],
        "point_of_sale._assets_pos": [
            "storrd_pos_branded_lockscreen/static/src/xml/saver_screen_inherit.xml",
            "storrd_pos_branded_lockscreen/static/src/js/saver_screen_patch.js",
        ],
    },
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}
