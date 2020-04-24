from datetime import timedelta, datetime
import functools

from pandas.io.json import json_normalize

from api.customer_apis.config import Config

class DashboardStats(Config):

    def getMonitoredUsers(self, conn, pid, from_date, to_date):
        if 1:
            res = conn.search(
                index='vpl_pa',
                body={
                    'query': 
                        {
                            'bool': {
                                "must": [
                                        { "term": { "pID": pid }},
                                        {
                                            "range" : {
                                                "et" : {
                                                    "gte" : from_date,
                                                    "lt" :  to_date
                                                }
                                            }
                                        }
                                    ]
                                }
                            }
                        },
                scroll='1m'
                )
            scroll = res['_scroll_id']
            h_results = res['hits']['hits']
            total_docs = res['hits']['total']['value']
            fetched_so_far = self.extract_size
            remained = total_docs - fetched_so_far

            while remained != 0:
                res = conn.scroll(scroll_id=scroll, scroll='1m')
                h_results += res['hits']['hits']

                fetched_so_far += self.extract_size
                remained = total_docs-fetched_so_far
                if remained < 0:
                    break 
                    
                scroll = res['_scroll_id']
            
            if not h_results:
                return 0

            df = json_normalize(h_results) 
            #print ('---',df.columns)
            unique_uE_vsi = set(df[df['_source.uE']!='']['_source.vsi'].unique()) 
            email_null = df[df['_source.uE']=='']
            #vsi_ = email_null.groupby('_source.vsi')
            unique_nuE_vsi = set(email_null['_source.vsi'].unique())
        
        total_unique_vsi = len(unique_uE_vsi.union(unique_nuE_vsi))
        return total_unique_vsi

    def getAuthenticatedUsers(self, conn, pid, from_date, to_date):
        if 1:
            res = conn.search(
                index='vll_pa',
                body={
                        "query" : {
                            "bool" : {
                                "must" : [ 
                                   { "term": { "ss" : "success" }}, 
                                   { "term": {"pID": pid}},
                                   {
                                        "range" : {
                                            "lgt" : {
                                                "gte" : from_date,
                                                "lt" :  to_date
                                            }
                                        }
                                    }
                                ]
                            },
                        }
                    },
                scroll='1m'
            )
            scroll = res['_scroll_id']
            h_results = res['hits']['hits']
            total_docs = res['hits']['total']['value']
            fetched_so_far = self.extract_size
            remained = total_docs - fetched_so_far

            while remained != 0:
                res = conn.scroll(scroll_id=scroll, scroll='1m')
                h_results += res['hits']['hits']

                fetched_so_far += self.extract_size
                remained = total_docs-fetched_so_far
                if remained < 0:
                    break 
                    
                scroll = res['_scroll_id']
            if not h_results:
                return 0

            df_vll = json_normalize(h_results) 

        count = len(df_vll['_source.uE'].unique())
        return count

    def getCounts(self, pid, from_date, to_date):
        try:
            pid = str(pid)
            to_date += timedelta(days=1)

            conn = self.getElasticConn() 
            total_unique_vsi = self.getMonitoredUsers(conn, pid, from_date, to_date)
            count_authenticated_user = self.getAuthenticatedUsers(conn, pid, from_date, to_date)

            high_risk_users = []
            count_device = 0
            notable_event = 0
            
            logs = Config.db[pid]

            # Caution: not all ML logs have lgt! need to figure our a way.
            all_logs = logs.find({'lgt': {'$gte':from_date, '$lt': to_date}})
            print ('Before Aggregation', all_logs.count())
            all_logs = self.aggregateLogs(all_logs)
            print ('After Aggregation', len(all_logs))
            
            for log in all_logs:
                notable_event += 1
                user = log['uid_key']
                
                if log['final_score'] > self.high:
                    count_device += 1
                    if user not in high_risk_users:
                        high_risk_users.append(user)
                 
                        
            return {
                'status':'success',
                'monitored_users': total_unique_vsi,
                'authenticated_users': count_authenticated_user,
                'high_risk_users': len(high_risk_users),
                'notable_events': notable_event, 
                'suspicious_device':count_device
            }
        except:
            return {
                'status':'error',
                'message': 'There was some error'
            }
       
if __name__ == "__main__":
    obj = DashboardStats()
    from_date = datetime(2020, 3, 21)
    to_date = datetime(2020, 4, 21)
    print (obj.getCounts('14', from_date, to_date))