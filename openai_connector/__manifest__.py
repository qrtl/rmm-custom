{
    'name': 'Openai Connector',
    'version': '15.0.1.0.0',
    'author': 'Quatile',
    "license": "AGPL-3",
    'website': 'https://www.quartile.co',
    'depends': ['base_setup', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'views/openai_vision_menu.xml',
        'views/openai_vision_message.xml',
        'views/openai_vision_session.xml',
    ],
    'installable': True,
}
