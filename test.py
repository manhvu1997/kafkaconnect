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
# class SieuNhan:
#     def __init__(self):
#     	self.a = "Mrchu is very handsome"
#     	self.b = "Professional"
#     def compare(self):
#     	if self.a == self.b:
#     		n = "true"
#     		print (n)
#     	else:
#     		print ("false")

# if __name__ == '__main__':
# 	i = SieuNhan()
# 	i.compare()
list = ["HNI-CSOC-02","HNI-CSOC-01","DTP-MP-01-01-NEW","DTP-MP-01-02-NEW","HDG-MP-01-01-NEW","HPG-MP-01-03","THA-MP-01-01-NEW"]
regex = r"[A-Z]+\-[A-Z]+\-\d+"
for i in list:
	if len(i)>12:
		name = re.findall(regex,str(i),re.MULTILINE)
		print (name[0])
	else:
		print ("false")
	
	