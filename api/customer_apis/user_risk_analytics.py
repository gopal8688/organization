from datetime import timedelta, datetime

from api.customer_apis.config import Config

class UserRiskAnalytics(Config):
    def getLogScore(self, pid, from_date, to_date):
        try:
            to_date += timedelta(days=1)
            no_days = (to_date-from_date).days + 1
            
            logs = Config.db[pid]

            all_data = logs.find({'lgt': {'$gte':from_date, '$lt': to_date}})
            all_data = self.aggregateLogs(all_data)
            date_list = [str(to_date - timedelta(days=x)).split()[0] for x in range(no_days)]
                    
            r_count_list = [0] * no_days
            g_count_list = [0] * no_days
            y_count_list = [0] * no_days
            
            for log in all_data:
                if not log.get('lgt'):
                    continue
                key = datetime.strftime(log['lgt'], "%Y-%m-%d")
                
                mscore = log['final_score']
                if mscore > self.high:
                    r_count_list[date_list.index(key)] += 1
                elif mscore > self.safe:
                    y_count_list[date_list.index(key)] += 1
                else:
                    g_count_list[date_list.index(key)] += 1
            if no_days>7:
                new_key_list = self.getRangeOf7(date_list);
                new_date_list = []
                new_r_count_list = []
                new_g_count_list = []
                new_y_count_list = []
                for x in range(7):
                    new_date_list.append(date_list[new_key_list[x]])
                    new_r_count_list.append(r_count_list[new_key_list[x]])
                    new_g_count_list.append(g_count_list[new_key_list[x]])
                    new_y_count_list.append(y_count_list[new_key_list[x]])
                date_list = new_date_list
                r_count_list = new_r_count_list
                g_count_list = new_g_count_list
                y_count_list = new_y_count_list
            
            return {
                'date': date_list[::-1],
                'g_count': g_count_list[::-1],
                'y_count': y_count_list[::-1],
                'r_count': r_count_list[::-1],
                'status': 'success'
            }
        except:
            return {
                'status': 'error',
                'message': 'There was some error'
            }

if __name__ == "__main__":
    obj = UserRiskAnalytics()
    pid = '14'
    from_date = datetime(2020, 4,1)
    to_date = datetime(2020, 5, 1)
    data = obj.getLogScore(pid, from_date, to_date)
    print (data)