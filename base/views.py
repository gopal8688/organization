import json

class BaseView():
    SITE_DATA = {
        'APP_NAME': 'authsafe',
        'API_URLS': json.dumps({
            'hru': 'high_risk_users/',
            'sa': 'security_alerts/',
            'saa': 'security_alert_attacks/',
            'la': 'login_attempts/',
        }),
        'ML_SERVER_API': 'http://demo.authsafe.ai:5000/api/'
    }