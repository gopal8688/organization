from datetime import datetime, timedelta

import pandas as pd
import functools

from api.customer_apis.config import Config

class RegionRiskCount(Config):

    def getCountryRisk(self, pid, from_date, to_date):
        
        try:
            score = []
            country =[]
            category = []
            to_date += timedelta(days=1)

            logs = Config.db[pid]
            
            all_logs = logs.find({'lgt': {'$gte':from_date, '$lt': to_date}})
            #logs_data = self.__aggregateLogs(all_logs)
            logs_data = self.aggregateLogs(all_logs)

            for log in logs_data:
                mscore = log['final_score']

                if log.get('leaf_key'):
                    nation = dict(map(lambda x:x.split(':'), log['leaf_key'].split(';')[1:]))['co']
                elif log.get('co'):
                    nation = log.get('co')
                else:
                    continue
                
                if mscore > self.high:
                    category.append('risky')
                else:
                    category.append('safe')
                
                score.append(mscore)
                country.append(nation)

            info = {'country': country, 'cat':category, 'score':score}
            data = pd.DataFrame(info)
            df_R = data[data['cat']=='risky']
            df_S = data[data['cat']=='safe']
            df_R['bad_users'] = df_R.groupby(['country'])['cat'].transform('count')
            df_S['good_users'] = df_S.groupby(['country'])['cat'].transform('count')
            df_data = pd.merge(df_R, df_S, how='outer', left_on='country', right_on='country')
            df_data = df_data[['country', 'bad_users','good_users']]
            df_data.fillna(0, inplace=True)
            df_data.drop_duplicates(keep = 'first', inplace = True)
            df_data.reset_index(inplace=True, drop=True)

            bad_users = df_data['bad_users']
            good_users = df_data['good_users']

            df_data['bad_users'] = round((bad_users/(bad_users+good_users))*100)
            df_data['good_users'] = round((good_users/(bad_users+good_users))*100)

            for x in df_data['bad_users']:
                df_data['bad_users'][x] = str(df_data['bad_users'][x])+'%'
            dict_ = df_data.to_dict('list')
            
            return {
                'status': 'success',
                'data': dict_
            }
        except:
            return {
                'status': 'error',
                'message': 'There was some error'
            }

if __name__ == "__main__":
    obj = RegionRiskCount()
    pid = '14'
    from_date, to_date = datetime(2019, 3, 11), datetime(2020, 5, 11)
    data = obj.getCountryRisk(pid, from_date, to_date)
    print (data)