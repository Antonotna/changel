import sys
import re

class iface:
	bw = 0
	dl = 50000
	name = ''
	Csum = 0
	def __init__(self,name):
		self.name = name

def main():

	ifList = []
	ifMax = iface('None')
	maxSum = 0

	print("Copy & Paste 'sh run | i interface Tunnel|delay|bandwidth' output chunk:")
	for line in sys.stdin:
		if(line == '\n'):
			break
		if('interface' in line):
			t = re.search('interface (.*)',line)
			ifList.append(iface(t.group(1)))
		if('bandwidth' in line):
			t = re.search('bandwidth.*?(\d+)',line)
			ifList[-1].bw = int(t.group(1))
		if('delay' in line):
			t = re.search('delay.*?(\d+)',line)
			ifList[-1].dl = int(t.group(1))

	for i in ifList:
		i.Csum = ((10000000/i.bw) * 256) + i.dl * 256
		if(i.Csum > maxSum):
			maxSum = i.Csum
			ifMax = i

	print('---------Paste to CLI exec mode------------')
	for i in ifList: 
		if(i == ifMax):
			print('!\n\
tclsh\n\
!\n\
if { [regexp "%s " [exec show ip interface brief] ] } {\n\
!\n\
ios_config "interface %s" "no delay"\n\
!\n\
}\n\
exit\
' % (i.name, i.name))
		else:
			print('!\n\
tclsh\n\
!\n\
if { [regexp "%s " [exec show ip interface brief] ] } {\n\
!\n\
ios_config "interface %s" "delay 1000000"\n\
!\n\
}\n\
exit\
' % (i.name, i.name))

	input()

if(__name__ == '__main__'):
 main()