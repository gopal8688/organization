import json

class BaseView():
    SITE_DATA = {
        'APP_NAME': 'authsafe',
        'API_URLS': json.dumps({
            'ds': 'dashboard_stats',
            'hru': 'highrisk_users',
            'sa': 'security_alerts',
            'la': 'login_attempts',
            'saa': 'security_alert_attacks',
        }),
        'ML_SERVER_API': 'http://demo.authsafe.ai:5000/api/'
    }