from datetime import datetime, timedelta

import functools

from api.customer_apis.config import Config
class UsersInfo(Config):

    def getRiskMap(self, pid, from_date, to_date):
        """
        Function to return coordinates for the risk map. Scores are aggregated per session in prior.
        """
        try:
            pid = str(pid)
            to_date += timedelta(days=1)
            
            logs = Config.db[pid]

            logs_data = logs.find({'datetime': {'$gte':from_date, '$lt': to_date}})
            logs_data = self.aggregateLogs(logs_data)

            score_count = {}            
            for log in logs_data:
                final_score = log['final_score']
                if not score_count.get(final_score):
                    score_count[final_score] = 0
                score_count[final_score] += 1

        except:
            return {
                'status': 'error'
                }

        return {
               'status': 'success',
               'data': score_count
            }
    
    def getUserList(self, pid, from_date, to_date):
        try:
        #if 1:
            pid = str(pid)
            to_date += timedelta(days=1)

            logs = Config.db[pid]

            logs_data = logs.find({'lgt': {'$gte':from_date, '$lt': to_date}}).sort([('lgt', 1)])
            logs_data = self.aggregateLogs(logs_data)
            #assert False, logs_data[:3]
            user_info = {}
            for log in logs_data:
                username = log['uid_key']
                
                if not user_info.get(username):
                    user_info[username] = {
                        'os': {},
                        'locn': {},
                        'dvc': {},
                    }
                if log.get('leaf_key'):
                    leaf_key = dict(map(lambda x:x.split(':'), log['leaf_key'].split(';')[1:]))
                    loc = "%s, %s, %s"%(leaf_key['ci'], leaf_key['st'], leaf_key['co'])
                    os, device = leaf_key['os'], leaf_key['d']
                else:
                    city, state, country = log.get('ci', ''), log.get('st', ''), log.get('co', '')
                    loc = "%s, %s, %s"%(city, state, country)
                    os, device = log.get('os', ''), log.get('d', '')

                if os and not user_info[username]['os'].get(os): user_info[username]['os'][os] = 0
                if loc and not user_info[username]['locn'].get(loc): user_info[username]['locn'][loc] = 0
                if device and not user_info[username]['dvc'].get(device): user_info[username]['dvc'][device] = 0

                if os: user_info[username]['os'][os] += 1
                if loc: user_info[username]['locn'][loc] += 1
                if device: user_info[username]['dvc'][device] += 1
            
                if 1:
                    mscore = log['final_score']
                    if mscore > self.high:
                        flag = 'R'
                    elif mscore > self.safe:
                        flag = 'Y'
                    else:
                        flag = 'G'

                    if flag == 'R':
                        user_info['obs'] = 'unsafe'
                    else:
                        user_info['obs'] = 'safe'

                    user_info[username]['rec_time'] = log.get('lgt', log['datetime'])
                    user_info[username]['rec_score'] = mscore
                    user_info[username]['rec_flag'] = flag
                    user_info[username]['rec_threat'] = log.get('threat_type', 'Maximum User Behaviour Score') #Made chancges here
        except:
            return {
                'status': 'failed',
                'data': {}
                }
        return {
             'status': 'success', 
             'data': user_info
           }

if __name__ == "__main__":
    pid = '14'
    from_date = datetime(2020, 4,1)
    to_date = datetime(2020, 5, 1)

    obj = UsersInfo()
    print (obj.getUserList(pid, from_date, to_date))
    #print (obj.getRiskMap(pid, from_date, to_date))