import json
import pytz
from auths.models import Customer, Property, CPRelationship, PropertyTokens

class CustomerView():
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
        # 'API_URLS': json.dumps({
        #     'ds': 'dashboard_stats',
        #     'hru': 'highrisk_users',
        #     'sa': 'security_alerts',
        #     'la': 'login_attempts',
        #     'saa': 'user_risk_analytics',
        #     'rrd': 'region_risk_dist',
        #     'rm': 'risk_map',
        #     'ul': 'user_list',
        #     'bud': 'basic_user_details',
        #     'rua': 'recent_user_activities',
        #     'ulo': 'user_locations',
        #     'lus': 'linked_users',
        # }),
        'API_URLS': json.dumps({}),
        'ML_SERVER_API': 'http://demo.authsafe.ai:5000/api/',
        'time_zones': json.dumps(getAllTimeZones.__func__())
    }
    #get customer detail against the email stored in session
    def getCustomerObj(self, request):
        
        email = request.session['email'] #.request.session['email']        
        cust_obj = Customer.objects.get(email=email)

        return cust_obj

    def getPropertyObj(self, request):
        pid = request.session['pid'] #.request.session['email']        
        prop_obj = Property.objects.get(id=pid)

        return prop_obj