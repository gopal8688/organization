from api.customer_apis.config import Config

from datetime import datetime, timedelta

class HighRiskUsers(Config):

    def getHighRiskUsers(self, pid, limit, from_date, to_date):
        try:
            to_date += timedelta(days=1)

            logs = Config.db[pid]
            users_scores = []
            user_info = {}

            all_logs = logs.find({'lgt': {'$gte':from_date, '$lt': to_date}})           
            all_logs = self.aggregateLogs(all_logs)

            for log in all_logs:
                user = log['uid_key']
                mscore = log['final_score']
                
                if mscore > self.high:
                    flag = 'R'
                elif mscore > self.safe:
                    flag = 'Y'
                else:
                    continue

                if user not in user_info:
                    user_info[user] = {
                        'user': user,
                        'score': mscore,
                        'cat': flag
                    }
                elif user_info[user]['score'] > mscore:
                    user_info[user]['score'] = mscore
                    user_info[user]['cat'] = flag

            users_scores = [info for info in user_info.values()]
            data = {
                'users_scores':users_scores[:limit],
                'status':'success'
                }
            
            return data
        except:
            return {
                'status': 'error',
                'message': 'There was some error'
            }
