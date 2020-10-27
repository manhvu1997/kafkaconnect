import json
from pprint import pprint
import mysql.connector
from os import path
import logging
import mysql.connector
class database_ipv6():
	def __init__(self):
		try:
			path_file = path.dirname(path.abspath(__file__))
			file_name = path.join(path_file,"config.json")
			with open (file_name,'r') as config_file:
				self.config = json.load(config_file)
				self.host = self.config["database"]["host"]
				self.user = self.config["database"]["user"]
				self.password = self.config["database"]["pass"]
				self.database = self.config["database"]["dbname"]
		except Exception as e:
			raise e
		try:
			self.mydb = mysql.connector.connect(host = self.host, user = self.user, password = self.password, database = self.database)
			self.cursor = self.mydb.cursor(buffered = True)
		except Exception as e:
			raise e
	def getdata(self):
		try:
			data_query = self.config["database"]["query"]["get_data"]
			self.cursor.execute(data_query)
			data = self.cursor.fetchall()
			return data
		except Exception as e:
			raise e
	def getdevicename(self):
		try:
			device_name_query = self.config["database"]["query"]["get_device_name"]
			self.cursor.execute(device_name_query)
			device_name = self.cursor.fetchall()
			return device_name
		except Exception as e:
			raise e
	def getipdevice(self):
		try:
			ip_query = self.config["database"]["query"]["get_ip"]
			self.cursor.execute(ip_query)
			ip_device = self.cursor.fetchall()
			return ip_device
		except Exception as e:
			raise e
if __name__ == '__main__':
	db = database_ipv6()
	x = db.getdevicename()
	y = db.getdata()
	for data in y:
		print data
	# db.getipdevice()
	
