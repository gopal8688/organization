from pymongo import MongoClient
from elasticsearch import Elasticsearch

import functools

from sshtunnel import SSHTunnelForwarder

class Config():
	MONGO_HOST = "localhost"
	MONGO_PORT = 27017
	MONGO_DB = 'ml_logs' #"DATABASE_NAME"
	MONGO_USER = 'admin'
	MONGO_PASS = 'Sl7@1234'

	# server = SSHTunnelForwarder(
	#     MONGO_HOST,
	#    # ssh_username=MONGO_USER,
	#    # ssh_password=MONGO_PASS,
	#     remote_bind_address=('127.0.0.1', 27017)
	# )   
	# server.start()

	client = MongoClient(MONGO_HOST,MONGO_PORT,username=MONGO_USER,password=MONGO_PASS)
	db = client[MONGO_DB]
	high = 0
	mid = 0
	safe = 0
	extract_size = 30

	# Generalized criterias.
	def __init__(self):
		# self.server = 'localhost'
		# self.port = '27017'
		# self.db = 'IngressoRapido'
		# connection = pymongo.Connection(self.server, self.port)
		# db = connection[self.db]

		self.high = 90
		self.mid = 77
		self.safe = 20

		self.extract_size = 30

	def getElasticConn(self):
		conn = Elasticsearch([{
					'host':  '95.216.170.200', 
					'port':  '9200'
				}], 
				http_auth=(
					'elastic', 
					'263508SL72k19'
				)
			)
		return conn 

	# Function to aggregate logs. 
	def aggregateLogs(self, recent_log):
		agg = {}
		for log in recent_log:
			if not log.get(log['uuid']):
				agg[log['uuid']] = []
			agg[log['uuid']].append(log)

		agg_one_log = []
		for _, logs in agg.items():
			all_keys = list(functools.reduce(lambda x, y: x+y, [log.keys() for log in logs]))
			if 'user_score' in all_keys: all_keys.remove('user_score')
			if 'env_score' in all_keys: all_keys.remove('env_score')
			h_fscore = 0
			no_logs = len(logs)
			new_log = {}
			for key in all_keys:
				for i in range(no_logs):
					if key == 'threat_type':
						continue
					elif key == 'final_score' and logs[i]['final_score'] >= h_fscore:
						new_log['final_score'] = logs[i]['final_score']
						new_log['threat_type'] = logs[i].get('threat_type', 'Unusual Score')
						h_fscore = new_log['final_score']
					elif logs[i].get(key):
						new_log[key] = logs[i][key]
			agg_one_log.append(new_log)

		return agg_one_log