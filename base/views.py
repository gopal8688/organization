import json
import pytz

class BaseView():
    @staticmethod
    def getAllTimeZones():
        all_timezones = []

        timezones = pytz.all_timezones
        
        for timezone in timezones:
            #print (timezone)
            all_timezones.append(timezone)
            #all_timezones.append((timezone, pytz.timezone(timezone)))
        #print (all_timezones[:4])
        return all_timezones
    
    SITE_DATA = {
        'APP_NAME': 'authsafe',
        'API_URLS': json.dumps({
            'hru': 'high_risk_users/',
            'sa': 'security_alerts/',
            'saa': 'security_alert_attacks/',
            'la': 'login_attempts/',
        }),
        'ML_SERVER_API': 'http://demo.authsafe.ai:5000/api/',
        'time_zones': json.dumps(getAllTimeZones.__func__())
    }
