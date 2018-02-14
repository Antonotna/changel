import sys
import re

try:
	import pyperclip
except ImportError:
	clipFlag = False
except:
	print('Unexpected Import Error', sys.exc_info()[0])	
	sys.exit()	
else:
	clipFlag = True

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
	tclOut = []

	if(clipFlag):
		print('-'*40)
		print('Result will be copied to clipboard')
		print('-'*40)
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

	if(clipFlag):
		for i in ifList: 
			if(i == ifMax):
				tclOut.append('if { [regexp "%s " [exec show ip interface brief] ] } { ios_config "interface %s" "no delay" "end" }' % (i.name, i.name) )
			else:
				tclOut.append('if { [regexp "%s " [exec show ip interface brief] ] } { ios_config "interface %s" "delay 1000000" "end" }' % (i.name, i.name) )
		pyperclip.copy('tclsh\n\n' + ';'.join(tclOut) + ' ; tclquit\n')

	else:
		print('---------Paste to CLI exec mode------------')
		print('tclsh')
		for i in ifList: 
			if(i == ifMax):
				print('\n\nif { [regexp "%s " [exec show ip interface brief] ] } { ios_config "interface %s" "no delay" "end" }\n' % (i.name, i.name) )
			else:
				print('\n\nif { [regexp "%s " [exec show ip interface brief] ] } { ios_config "interface %s" "delay 1000000" "end" }\n' % (i.name, i.name) )
		print('tclquit')
	
		input()

if(__name__ == '__main__'):
	main()