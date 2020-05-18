from api.customer_apis.config import Config
from datetime import timedelta, datetime

class SecurityAlerts(Config):
    
    def getNotableDevice(self, pid, from_date, to_date):
        try:
            usr_scr_cat_det = []
            #limit = int(request.args.get('limit'))
            to_date += timedelta(days=1)
    
            logs = Config.db[pid]

            all_logs = logs.find({'lgt': {'$gte':from_date, '$lt': to_date}}).sort([('datetime', 1)])
            all_logs = self.aggregateLogs(all_logs)            

            user_alert = {}
            for log in all_logs:
                #print (log)
                user = log['uid_key']
                mscore = log['final_score']
                
                if mscore > self.high:
                    flag = 'R'
                elif mscore > self.safe:
                    flag = 'Y'
                else:
                    continue
                threat_type = log.get('threat_type')

                if not user_alert.get(user):
                    user_alert[user] = {
                        'user': user,
                        'score': mscore,
                        'cat': flag,
                        'det': threat_type
                    }
                elif (flag == 'R' and user_alert[user]['cat'] == 'Y') or \
                    (flag == 'Y' and user_alert[user]['cat'] == 'G') or \
                    (flag == 'R' and user_alert[user]['cat'] == 'G'):
                        user_alert[user] = {
                            'user': user,
                            'score': mscore,
                            'cat': flag,
                            'det': threat_type
                        }

            for security_alert_log in user_alert.values(): 
                usr_scr_cat_det.append(security_alert_log)
            
            data = {
                'usr_scr_cat_det':usr_scr_cat_det[:],
                'status':'success'
                }
            
            return {
                'status': 'success',
                'data': data
            }
        except:
            return {
                'status':'failed',
                'data': []
                }

if __name__ == "__main__":
    obj = SecurityAlerts()
    pid, from_date, to_date = '14', datetime(2020, 1, 1), datetime(2020, 3, 1)
    data = obj.getNotableDevice(pid, from_date, to_date)
    print (data)