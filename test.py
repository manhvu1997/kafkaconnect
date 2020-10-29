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
name = u'HNI-CSOC-02'
ip = u'118.70.0.131'
NAT = '0'
ipv6 = 0
area = 'FTN'
zone = 3
province = 'THA-MP-01'
ccu = 0
ipv4 =0
tup = (name,ip,NAT,ipv6,area,zone,province,ccu,ipv4)
command = "insert into total_subipv6 (hostname, ip_device, NAT, ipv6, area, zone, province, ccu, ipv4) values "+ str(tup)+";"
print (command)
print (len(command))
	