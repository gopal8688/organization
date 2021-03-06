from api.customer_apis.config import Config

class UserDetails(Config):

    def getBasicDetails(self, pid, user):
        try:
            user = user.strip('/').strip()
            logs = Config.db[pid]
            
            recent_logintime = logs.find({'uid_key': user}).sort([('lgt', -1)]).limit(1)
            
            uuid = ''
            for log in recent_logintime:
                uuid = log['uuid']
            
            if uuid:
                #recent_log = logs.find({'uid_key': user,'uuid': uuid }).sort([('datetime', 1)])
                recent_log = logs.find({'uid_key': user,'uuid': uuid })
                recent_log = self.aggregateLogs(recent_log) # Newly added
            else:
                recent_log = []
            
            data = {}
            score = 0
            for rec_data in recent_log:
                mscore = rec_data['final_score']
                if mscore >= score:
                    score = mscore
                else:
                    continue

                data['rec_dt'] = rec_data['lgt']

                if rec_data.get('leaf_key'):
                    leaf_key = dict(map(lambda x:x.split(':'), rec_data['leaf_key'].split(';')[1:]))
                    loc = "%s, %s, %s"%(leaf_key['ci'], leaf_key['st'], leaf_key['co'])
                else:
                    loc = "%s, %s, %s"%(rec_data.get('ci',''), rec_data.get('st',''), rec_data.get('co',''))
                
                data['rec_loc'] = loc
                
                data['final_score'] = mscore
                if mscore > self.high:
                    data['flag'] = 'R'
                    data['obs'] = 'unsafe'
                elif mscore > self.safe:
                    data['flag'] = 'Y'
                    data['obs'] = 'safe'
                else:
                    data['flag'] = 'G'
                    data['obs'] = 'safe'
                
        except:
            return {
                'status': 'error'
                }

        return {
               'status': 'success',
               'data': data
            }
    
    def getLinkedList(self, pid, user, limit):
        try:
            limit = int(limit)

            logs = Config.db[pid]
            
            linked_users = []
            ## Get ip associated with recent log and find all the logs having that ip.
            recent_log = logs.find({'uid_key': user}).sort([('lgt', -1)]).limit(1)
            for ulog in recent_log:
                if not ulog.get('ip'):
                    break
                ip = ulog['ip']
                for log in logs.find({'ip':ip}):
                    linked_user = log['uid_key']
                    if linked_user not in linked_users and linked_user != user:
                        linked_users.append(linked_user)

            return {
                'status': 'success',
                'data': linked_users[:limit]
            }
        
        except:
            return {
                'status': 'error'
            }

    def __aggregateLogs(self, recent_log):
        agg = {}
        for log in recent_log:
            if not log.get(log['uuid']):
                agg[log['uuid']] = []
            agg[log['uuid']].append(log)

        return agg
        
    def getRecentActivities(self, pid, user, limit):
        
        try:
        #if 1:
            limit = int(limit)
            #from_score, to_score = list(map(lambda x: datetime.strptime(x, '%d-%m-%Y'), request.args.get('score_range').split(';')))        

            logs = Config.db[pid]
            
            recent_log = logs.find({'uid_key': user}).sort([('lgt', -1)])
            recent_logs = self.aggregateLogs(recent_log)
            data = []
            for log in recent_logs:
                curr_log = {}     
                if 1:
                    if log.get('leaf_key'):
                        leaf_key = dict(map(lambda x:x.split(':'), log['leaf_key'].split(';')[1:]))
                        os, device = leaf_key['os'], leaf_key['d'] 
                        loc = "%s, %s, %s"%(leaf_key['ci'], leaf_key['st'], leaf_key['co'])
                    else:
                        os, device = log['os'], log['d']
                        loc = "%s, %s, %s"%(log.get('ci',''), log.get('st',''), log.get('co',''))
                    
                    curr_log = {
                        'os': os,
                        'loc': loc,
                        'dvc': device
                    }
                    mscore = log['final_score']
                    if mscore > self.high:
                        curr_log['flag'] = 'R'
                        curr_log['obs'] = 'unsafe'
                    elif mscore > self.safe:
                        curr_log['flag'] = 'Y'
                        curr_log['obs'] = 'safe'
                    else:
                        curr_log['flag'] = 'G'
                        curr_log['obs'] = 'safe'

                    curr_log['final_score'] = mscore
                    curr_log['datetime'] = log['lgt']

                data.append(curr_log)
        except:
        #else:
            return {
                'status': 'failed',
                'data': []
                }
        #print ('-----------------------',data)
        return {
             'status': 'success', 
             'data': data[:limit]
           }

    def getUserLocations(self, pid, user):
        try:
            logs = Config.db[pid]
            
            recent_log = logs.find({'uid_key': user})
            recent_logs = self.aggregateLogs(recent_log)

            data = {}

            max_score = 0
            highest_score_log = {}
            for log in recent_logs:
                if log.get('leaf_key'):
                    leaf_key = dict(map(lambda x:x.split(':'), log['leaf_key'].split(';')[1:]))
                    loc = (leaf_key['ci'], leaf_key['st'], leaf_key['co'])
                elif log.get('ci'):
                    loc = (log.get('ci',''), log.get('st',''), log.get('co',''))
                else:
                    continue
                
                mscore = log['final_score']
                if mscore >= max_score:
                    max_score = mscore
                    highest_score_log = log
                
                if not data.get(loc):
                    data[loc] = highest_score_log
                elif data[loc]['final_score'] < score:
                    data[loc] = highest_score_log

            loc_data = {
                'co': [],
                'st': [],
                'ci': [],
                'la': [],
                'lo': [],
                'pd': [],
            }
            for loc, log in data.items():
                city, state, country = loc
                la, lo = log.get('la', ''), log.get('lo', '')

                mscore = log['final_score']
                if mscore > self.high:
                    flag = 'R'
                    obs = 'unsafe'
                elif mscore > self.safe:
                    flag = 'Y'
                    obs = 'safe'
                else:
                    flag = 'G'
                    obs = 'safe'

                loc_data['ci'].append(city)
                loc_data['co'].append(country)
                loc_data['st'].append(state)
                loc_data['la'].append(la)
                loc_data['lo'].append(lo)
                loc_data['pd'].append({
                    'flg': flag,
                    'obs': obs,
                    'score': mscore
                })

        except:
            return {
                'status': 'error'
            }
        return {
            'status': 'success',
            'data': loc_data
        }
            
if __name__ == "__main__":
    obj = UsersDetails()
    pid, email = '14', 'deepakr.kotphode@gmail.com'

    print (obj.getBasicDetails(pid, email))
    print (obj.getRecentActivities(pid, email, 100))
    print (obj.getUserLocations(pid, email))