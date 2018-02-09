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
 ifMax = iface('default')
 maxSum = 0
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

 print('---------result------------')
 for i in ifList: 
  if(i == ifMax):
   print('interface ' + i.name + '\nno delay')
  else:
   print('interface ' + i.name + '\ndelay 1000000')

 input()

if(__name__ == '__main__'):
 main()