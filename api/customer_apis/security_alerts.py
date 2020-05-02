from api.customer_apis.config import Config
from datetime import timedelta, datetime

class SecurityAlerts(Config):
    
    def getNotableDevice(self, pid, limit, from_date, to_date):
        try:
            usr_scr_cat_det = []
            #limit = int(request.args.get('limit'))
            to_date += timedelta(days=1)
    
            logs = Config.db[pid]

            all_logs = logs.find({'lgt': {'$gte':from_date, '$lt': to_date}})
            all_logs = self.aggregateLogs(all_logs)            

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
                usr_scr_cat_det.append({
                        'user': user,
                        'score': round(mscore),
                        'cat': flag,
                        'det': threat_type
                })
            
            data = {
                'status':'success',
                'usr_scr_cat_det':usr_scr_cat_det[:limit],
                }
            
            return data
        except:
            return {
                'status':'error',
                'message': 'There was some error'
            }

if __name__ == "__main__":
    obj = SecurityAlerts()
    pid, from_date, to_date = '14', datetime(2020, 1, 1), datetime(2020, 3, 1)
    data = obj.getNotableDevice(pid, from_date, to_date)
    print (data)