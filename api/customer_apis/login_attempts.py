from datetime import datetime, timedelta

from api.customer_apis.config import Config

class LoginAttempts(Config):
        
    def getLogInAttempts(self, pid, from_date, to_date):     
        #try:
        no_days = (to_date-from_date).days + 1
        date_list = [str(to_date - timedelta(days=x)).split()[0] for x in range(no_days)]
        conn = self.getElasticConn()
        
        res = conn.search(
            index = 'vll_pa',
            body = { 
                    'query': {
                        'bool': {
                            'must': [

                                        { "match": { "pID": pid }},
                                        {
                                            'range': {
                                                'lgt': {
                                                    "gte" : from_date,
                                                    "lte" :  to_date
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
            return {
                'date': date_list,
                's_count': [0]*len(date_list),
                'f_count': [0]*len(date_list),
                'status':'success'
                }

        s_count_list = [0]*no_days
        f_count_list = [0]*no_days

        for log in h_results:
            #print ('----', log)
            key = log['_source']['lgt'].split('T')[0]
            if log['_source']['ss'] in ['success']:
                s_count_list[date_list.index(key)] += 1
            else:
                f_count_list[date_list.index(key)] += 1
        if no_days>7:
            new_key_list = self.getRangeOf7(date_list);
            new_date_list = []
            new_s_count_list = []
            new_f_count_list = []
            for x in range(7):
                new_date_list.append(date_list[new_key_list[x]])
                new_s_count_list.append(s_count_list[new_key_list[x]])
                new_f_count_list.append(f_count_list[new_key_list[x]])
            date_list = new_date_list
            s_count_list = new_s_count_list
            f_count_list = new_f_count_list
        return {
            'date': date_list[::-1],
            's_count': s_count_list[::-1],
            'f_count': f_count_list[::-1],
            'status' : 'success'
        }

        # except:
        #     return {
        #         'status': 'error',
        #         'message': 'There was some error'
        #     }
if __name__ == "__main__":
    obj = LoginAttempts()
    from_date = datetime(2020, 3, 1)
    to_date = datetime(2020, 3, 15)

    data = obj.getLogInAttempts('14', from_date, to_date)
    print (data)