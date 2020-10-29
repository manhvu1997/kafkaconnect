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
import re 
import datetime
import database_ipv6
import API_device
import filter_zone

def device_not_added():
	NAT = '0'
	ipv6 = '0'
	ccu = '0'
	ipv4 = '0'
	device_area = { "FTN": ["HNI", "BGG", "BNH", "CBG", "LSN", "LCI", "PTO", "TNN", "TQG", "VPC", "YBI", "HBH", "SLA", "DBN", "QNH", "HNM", "NDH", "NAN", "NBH", "TBH", "THA", "HTH", "HDG", "HPG", "HYN"],
					"FTS": ["BDH", "DNG", "DLK", "GLI", "HUE", "NTG", "KTM", "PYN", "QTI", "QNM", "QBH", "QNI", "KHA", "HCM", "BDG", "BTN", "DNI", "LDG", "NTN", "TNH", "VTU", "BPC", "CTO", "AGG", "BLU", "BTE", "CMU", "DTP", "HGG", "KGG", "TGG", "LAN", "VLG", "STG", "TVH"] 
	}
	device_zone = { "Zone_1":"HNI",
					"Zone_2":["BGG","BNH","CBG","LSN","LCI","PTO","TNN","TQG","VPC","YBI","HBH","SLA","DBN","QNH"],
					"Zone_3":["HNM","NDH","NAN","NBH","TBH","THA","HTH","HDG","HPG","HYN"],
					"Zone_4":["BDH","DNG","DLK","GLI","HUE","NTG","KTM","PYN","QTI","QBH","QNI","KHA","QNM"],
					"Zone_5":"HCM",
					"Zone_6":["BDG","BTN","DNI","LDG","NTN","TNH","VTU","BPC","BTN"],
					"Zone_7":["CTO","AGG","BLU","BTE","CMU","DTP","HGG","KGG","TGG","LAN","VLG","STG","TVH"]
	}
	filter_zone = {"Zone_1_":"1","Zone_2_":"2","Zone_3_":"3","Zone_4_":"4","Zone_5_":"5","Zone_6_":"6","Zone_7_":"7"}
	_row_1 = '+ {0:-^20}+{1:-^20}+{2:-^6}+{3:-^6}+{4:-^6}+{5:-^6}+{6:-^15}+{7:-^30}+{8:-^6}+{9:-^6}+{10:-^20}+\n'.format('','', '','','','','','','','','')
	_row_2 = '|{0:^20} |{1:^20}|{2:^6}|{3:^6}|{4:^6}|{5:^6}|{6:^15}|{7:^30}|{8:^6}|{9:^6}|{10:^20}|\n'.format('hostname', 'ip_device', 'NAT','IPV6','Area','Zone','Province','Log time','CCU','IPV4','NOTE')
	_row_3 = '+ {0:-^20}+{1:-^20}+{2:-^6}+{3:-^6}+{4:-^6}+{5:-^6}+{6:-^15}+{7:-^30}+{8:-^6}+{9:-^6}+{10:-^20}+\n'.format('','', '','','','','','','','','')
	list_ip = []
	data = API.getdataAPI()
	ip_databse = database.getipdevice()
	for ip in ip_databse:
		list_ip.append(ip)
	reg_ip = re.findall(r"\d+\.\d+\.\d+\.\d+",str(list_ip))
	reg_name = r"[A-Z]+\-[A-Z]+\-\d+"
	with open ("/home/dev/Manhvc/device_database/list_review.txt","w+") as review_file:
		review_file.writelines(_row_1)
		review_file.writelines(_row_2)
		review_file.writelines(_row_3)
		for i in data["data"]:
			list_device = []
			function = []
			name_not_added = ""
			ip_not_added = ""
			zone_not_added = ""
			area_not_added = ""
			province_not_added = ""
			nat_not_added = ""
			ipv6_not_added = ""
			ccu_not_added = ""
			ipv4_not_added = ""
			note = ""
			function.append(i["function"])
			if function[0] =="Metro BroadBand BRAS":
				if i["ip"] not in reg_ip:
					ip_not_added += i["ip"]
					update_time = str(datetime.datetime.now())
					name_not_added += i["name"]
					nat_not_added += NAT
					ipv6_not_added += ipv6
					if name_not_added[0:3] in device_area['FTS']:
						area_not_added = area_not_added + 'FTS'
					elif name_not_added[0:3] in device_area['FTN']:
						area_not_added = area_not_added + 'FTN'
					if name_not_added[0:3] in device_zone['Zone_1']:
						zone_not_added= zone_not_added + filter_zone['Zone_1_']
					elif name_not_added[0:3] in device_zone['Zone_2']:
						zone_not_added= zone_not_added + filter_zone['Zone_2_']
					elif name_not_added[0:3] in device_zone['Zone_3']:
						zone_not_added= zone_not_added + filter_zone['Zone_3_']
					elif name_not_added[0:3] in device_zone['Zone_4']:
						zone_not_added= zone_not_added + filter_zone['Zone_4_']
					elif name_not_added[0:3] in device_zone['Zone_5']:
						zone_not_added= zone_not_added + filter_zone['Zone_5_']
					elif name_not_added[0:3] in device_zone['Zone_6']:
						zone_not_added= zone_not_added +filter_zone['Zone_6_']
					elif name_not_added[0:3] in device_zone['Zone_7']:
						zone_not_added= zone_not_added +filter_zone['Zone_7_']
					if (len(i["name"]) > 12):
						province = re.findall(reg_name,str(i["name"]),re.MULTILINE)
						province_not_added +=  province[0]
					else:
						province_not_added += i["name"][0:-3]
					ccu_not_added += ccu
					ipv4_not_added += ipv4
					note += 'not added'
					_row_4 = '|{0:^20} |{1:^20}|{2:^6}|{3:^6}|{4:^6}|{5:^6}|{6:^15}|{7:^30}|{8:^6}|{9:^6}|{10:^20}|\n'.format(name_not_added, ip_not_added, nat_not_added,ipv6_not_added,area_not_added,zone_not_added,province_not_added,update_time,ccu_not_added,ipv4_not_added,note)
					review_file.writelines(_row_4)

def device_recalled():
	# _device_area = { "FTN": ["HNI", "BGG", "BNH", "CBG", "LSN", "LCI", "PTO", "TNN", "TQG", "VPC", "YBI", "HBH", "SLA", "DBN", "QNH", "HNM", "NDH", "NAN", "NBH", "TBH", "THA", "HTH", "HDG", "HPG", "HYN"],
	# 				"FTS": ["BDH", "DNG", "DLK", "GLI", "HUE", "NTG", "KTM", "PYN", "QTI", "QNM", "QBH", "QNI", "KHA", "HCM", "BDG", "BTN", "DNI", "LDG", "NTN", "TNH", "VTU", "BPC", "CTO", "AGG", "BLU", "BTE", "CMU", "DTP", "HGG", "KGG", "TGG", "LAN", "VLG", "STG", "TVH"] 
	# }
	# _device_zone = { "Zone_1":"HNI",
	# 				"Zone_2":["BGG","BNH","CBG","LSN","LCI","PTO","TNN","TQG","VPC","YBI","HBH","SLA","DBN","QNH"],
	# 				"Zone_3":["HNM","NDH","NAN","NBH","TBH","THA","HTH","HDG","HPG","HYN"],
	# 				"Zone_4":["BDH","DNG","DLK","GLI","HUE","NTG","KTM","PYN","QTI","QBH","QNI","KHA","QNM"],
	# 				"Zone_5":"HCM",
	# 				"Zone_6":["BDG","BTN","DNI","LDG","NTN","TNH","VTU","BPC","BTN"],
	# 				"Zone_7":["CTO","AGG","BLU","BTE","CMU","DTP","HGG","KGG","TGG","LAN","VLG","STG","TVH"]
	# }
	# _filter_zone = {"Zone_1_":"1","Zone_2_":"2","Zone_3_":"3","Zone_4_":"4","Zone_5_":"5","Zone_6_":"6","Zone_7_":"7"}
	list_ip = []
	data = API.getdataAPI()
	data_databse = database.getdata()
	for i in data["data"]:
		function = []
		function.append(i["function"])
		if function[0] == "Metro BroadBand BRAS":
			list_ip.append(i["ip"])
	with open ("/home/dev/Manhvc/device_database/list_review.txt","a+") as file:
		try:
			for data in data_databse:
				name_recalled = ""
				ip_recalled = ""
				zone_recalled = ""
				area_recalled = ""
				province_recalled = ""
				nat_recalled = ""
				ipv6_recalled = ""
				ccu_recalled = ""
				ipv4_recalled = ""
				_note = ""
				#regex = r"\(u\'([A-Z]{3}\-[A-Z]+-\d+-\d+)\'.\s+u\'(\d+.\d+.\d+.\d+)\'.\s+(\d+)\,\s+(\d+)\,\s+u\'([A-Z]+)\'\,\s+(\d+)\,\s+u\'([A-Z]+-[A-Z]+\-\d+)\'\,\s+(.*\)\,)\s+(\d+)\,\s+(\d+)\)"
				regex = r"\(u\'([A-Z]+\-[A-z]+\-(\d+|[A-Za-z]+)\-\d+(.*))\'\,\s+u\'(\d+.\d+.\d+.\d+)\'\,\s+(\d+)\,\s+(\d+)\,\s+u\'([A-Z]+)\'\,\s+(\d+)\,\s+u\'([A-Z]+\-[A-Z]+\-(\d+|[A-Za-z]+))\'\,\s+(.*\)\,)\s+(\d+)\,\s+(\d+)\)"
				#regex = r"\(u.*\)"
				matches = re.findall(regex,str(data),re.MULTILINE)
				if matches[0][3] not in list_ip:
					ip_recalled += matches[0][3]
					update_time = str(datetime.datetime.now())
					name_recalled += matches[0][0]
					nat_recalled += matches[0][4]
					ipv6_recalled += matches[0][5]
					area_recalled += matches[0][6]
					zone_recalled += matches[0][7]
					province_recalled += matches[0][8]
					ccu_recalled += matches[0][11]
					ipv4_recalled += matches[0][12]
					_note += 'recalled'
					_row_5 = '|{0:^20} |{1:^20}|{2:^6}|{3:^6}|{4:^6}|{5:^6}|{6:^15}|{7:^30}|{8:^6}|{9:^6}|{10:^20}|\n'.format(name_recalled, ip_recalled, nat_recalled,ipv6_recalled,area_recalled,zone_recalled,province_recalled,update_time,ccu_recalled,ipv4_recalled,_note) 			
					file.writelines(_row_5)
		except Exception:
			print "No device has been recalled"
def wrong_name():
	ip_API = []
	compare_API = []
	data = API.getdataAPI()
	data_databse = database.getdata()
	for i in data["data"]:
		function = []
		function.append(i["function"])
		if function[0] == "Metro BroadBand BRAS":
			list_API = []
			ip_API.append(i["ip"])
			list_API.append(i["ip"])
			list_API.append(i["name"])
			compare_API.append(list_API)
	with open ("/home/dev/Manhvc/device_database/list_review.txt","a+") as file:
		try:
			for data in data_databse:
				name_wrong = ""
				ip_wrong = ""
				zone_wrong = ""
				area_wrong = ""
				province_wrong = ""
				nat_wrong = ""
				ipv6_wrong = ""
				ccu_wrong = ""
				ipv4_wrong = ""
				compare_db = []
				reg = r"\(u\'([A-Z]+\-[A-z]+\-(\d+|[A-Za-z]+)\-\d+(.*))\'\,\s+u\'(\d+.\d+.\d+.\d+)\'\,\s+(\d+)\,\s+(\d+)\,\s+u\'([A-Z]+)\'\,\s+(\d+)\,\s+u\'([A-Z]+\-[A-Z]+\-(\d+|[A-Za-z]+))\'\,\s+(.*\)\,)\s+(\d+)\,\s+(\d+)\)"
				match = re.findall(reg,str(data),re.MULTILINE)
				if match[0][3] in ip_API:
					compare_db.append(match[0][3])
					compare_db.append(match[0][0])
					if compare_db not in compare_API:
						ip_wrong += match[0][3]
						update_time = str(datetime.datetime.now())
						name_wrong += match[0][0]
						nat_wrong += match[0][4]
						ipv6_wrong += match[0][5]
						area_wrong += match[0][6]
						zone_wrong += match[0][7]
						province_wrong += match[0][8]
						ccu_wrong += match[0][11]
						ipv4_wrong += match[0][12]
						note_ = "wrong_name"
						_row_6 = '|{0:^20} |{1:^20}|{2:^6}|{3:^6}|{4:^6}|{5:^6}|{6:^15}|{7:^30}|{8:^6}|{9:^6}|{10:^20}|\n'.format(name_wrong, ip_wrong, nat_wrong,ipv6_wrong,area_wrong,zone_wrong,province_wrong,update_time,ccu_wrong,ipv4_wrong,note_)
						_row_7 = '+ {0:-^20}+{1:-^20}+{2:-^6}+{3:-^6}+{4:-^6}+{5:-^6}+{6:-^15}+{7:-^30}+{8:-^6}+{9:-^6}+{10:-^20}+\n'.format('','', '','','','','','','','','')
						file.writelines(_row_6)
		except Exception:
			print "No device is wrong name"
		file.writelines(_row_7)

			
<<<<<<< HEAD
			#print list_API
			#print ip_wrong
=======
>>>>>>> telegram

if __name__ == '__main__':
	API = API_device.API_device()
	database = database_ipv6.database_ipv6()
	device_not_added()
	device_recalled()
	wrong_name()
