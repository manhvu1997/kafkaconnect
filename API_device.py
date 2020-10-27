import copy
import csv
import json
# from rancidcmd import RancidCmd
import os
import sys
import time
from pprint import pprint
import requests
from requests.packages import urllib3
from pprint import pprint
import mysql.connector
from os import path
import logging
import mysql.connector
class API_device():
	def __init__(self):
		try:
			path_file = path.dirname(path.abspath(__file__))
			file_name = path.join(path_file,"config.json")
			with open (file_name,'r') as config_file:
				self.config = json.load(config_file)
				self.urltoken = self.config["API"]["url_token"]
				self.urldata = self.config["API"]["url_data"]
				self.headers = self.config["API"]["header"]
		except Exception as e:
			raise e
	def getdataAPI(self):
		try:
			token_text = requests.post(self.urltoken, headers=self.headers, verify=False)
			reponse = eval(token_text.text)
			if "token" in reponse:
				ops_token = reponse["token"]
				# print ops_token
			data_get = requests.get(self.urldata, headers={"token":ops_token}, verify=False)
			data_output = json.loads(data_get.text)
			return data_output
		except Exception as e:
			raise e
if __name__ == '__main__':
	API = API_device()
	data = API.getdataAPI()
	for i in data["data"]:
		print i


