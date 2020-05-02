import functools
from api.customer_apis.config import Config
from datetime import timedelta, datetime
class UsersInfo(Config):

    def getRiskMap(self, pid, from_date, to_date):
        try:
            pid = str(pid)
            to_date += timedelta(days=1)
            
            logs = self.db[pid]

            agg_res = logs.aggregate([
                {"$match": {'datetime': {'$gte':from_date, '$lt': to_date}}},
                {"$group" : {'_id':"$final_score", 'count':{'$sum': 1}}}
            ])

            x_y = {}
            max_val = 0
            for res in agg_res:
                x_y[round(res['_id'])] = res['count']
            for z in x_y:
                if(x_y[z]>max_val):
                    max_val = x_y[z]
            return {
                   'status': 'success',
                   'data': x_y,
                   'max': max_val
                }
        except:
            return {
                'status': 'error',
                'message': 'There was some error'
            }
    
    def getUserList(self, pid, from_date, to_date):
        try:
            pid = str(pid)
            to_date += timedelta(days=1)

            logs = self.db[pid]

            logs_data = logs.find({'datetime': {'$gte':from_date, '$lt': to_date}}).sort([('datetime', 1)])
            #logs_data = self.__aggregateLogs(logs_data)
            logs_data = self.aggregateLogs(logs_data)
            
            user_info = {}
            i = 0;
            for log in logs_data:
                username = log['uid_key'].strip()
                
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
                    #city, state, country = log.get('ci', ''), log.get('st', ''), log.get('co', '')
                    os, device = log.get('os', ''), log.get('d', '')
                    #loc = "%s, %s, %s"%(city, state, country)
                    loc = 'Unknown'

                if os and not user_info[username]['os'].get(os): user_info[username]['os'][os] = 0
                if loc and not user_info[username]['locn'].get(loc): user_info[username]['locn'][loc] = 0
                if device and not user_info[username]['dvc'].get(device): user_info[username]['dvc'][device] = 0

                if os: user_info[username]['os'][os] += 1
                if loc: user_info[username]['locn'][loc] += 1
                if device: user_info[username]['dvc'][device] += 1
            
                if 1:
                    mscore = round(log['final_score'])
                    if mscore > self.high:
                        flag = 'R'
                    elif mscore > self.mid:
                        flag = 'Y'
                    else:
                        flag = 'G'

                    if flag == 'R':
                        user_info[username]['obs'] = 'unsafe'
                    else:
                        user_info[username]['obs'] = 'safe'

                    user_info[username]['rec_time'] = log.get('lgt', log['datetime'])
                    user_info[username]['rec_score'] = mscore
                    user_info[username]['rec_flag'] = flag
                    user_info[username]['rec_threat'] = log.get('threat_type', 'User Behaviour Threat') #Made chancges here
                    user_info[username]['rec_ip'] = log.get('ip', 'Unknown')
            for user_log in user_info:
                #locations = sorted(user_info[username]['locn'].items(), key = lambda x : x[1])
                #locations = sorted(user_info[username]['locn'].items(), key = lambda x : x[1])
                locations = {k: v for k, v in sorted(user_info[user_log]['locn'].items(), key=lambda item: item[1], reverse=True)}
                if len(locations)>1:
                    if locations.get('Unknown'):
                        del locations['Unknown']
                user_info[user_log]['locn'] = list(locations.keys())[0]
            return {
                 'status': 'success', 
                 'data': user_info
               }
        except:
            return {
                'status': 'error',
                'message': 'There was some error'
            }

    def __aggregateLogs(self, recent_log):
        agg = {}
        for log in recent_log:
            if not log.get(log['uuid']):
                agg[log['uuid']] = []
            agg[log['uuid']].append(log)

        return agg
