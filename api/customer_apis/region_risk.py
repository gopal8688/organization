from datetime import datetime, timedelta

import pandas as pd
import functools

from api.customer_apis.config import Config

class RegionRiskCount(Config):

    def getCountryRisk(self, pid, from_date, to_date):
        
        try:
        #if 1:
            country =[]
            to_date += timedelta(days=1)

            logs = Config.db[pid]
            
            all_logs = logs.find({'lgt': {'$gte':from_date, '$lt': to_date}})
            logs_data = self.aggregateLogs(all_logs)

            country_by_users = {}
            for log in logs_data:
                if log.get('leaf_key'):
                    nation = dict(map(lambda x:x.split(':'), log['leaf_key'].split(';')[1:]))['co']
                elif log.get('co'):
                    nation = log.get('co')
                else:
                    continue

                if not country_by_users.get(nation):
                    country_by_users[nation] = {
                        'good_users': [],
                        'bad_users': []
                    }
                
                mscore = log['final_score']
                cust_user = log['uid_key']

                if mscore > self.high and cust_user not in country_by_users[nation]['bad_users']:
                    country_by_users[nation]['bad_users'].append(cust_user)
                elif cust_user not in country_by_users[nation]['good_users']:
                    country_by_users[nation]['good_users'].append(cust_user)
                
            country = []
            bad_users = []
            good_users = []
            for key, user_dict in country_by_users.items():
                country.append(key)
                bad_ucount = len(user_dict['bad_users']) + 0.0000001
                good_ucount = len(user_dict['good_users']) + 0.00000001
                
                bad_users.append(round(bad_ucount/(bad_ucount+good_ucount), 2))
                good_users.append(round(good_ucount/(bad_ucount+good_ucount), 2))

            dict_ = {
                'country': country,
                'bad_users': bad_users,
                'good_users': good_users
            }            
            return {
                'status': 'success',
                'data': dict_
            }
        except:
        #else:
            return {
                'status': 'failed',
                'data': {}
            }

if __name__ == "__main__":
    obj = RegionRiskCount()
    pid = '14'
    from_date, to_date = datetime(2019, 3, 11), datetime(2020, 5, 11)
    data = obj.getCountryRisk(pid, from_date, to_date)
    print (data)