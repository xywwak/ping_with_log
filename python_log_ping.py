from pythonping import ping
import time
from datetime import datetime
from datetime import date as dt
import os
import sys

def summary(file):

	print('-----------------------------------------------')
	print('Log saved: '+file)
	print('-----------------------------------------------')
	
	lines = []
	with open(file) as entry_file:
		
		lines = [line.rstrip() for line in entry_file]

	del lines[0] #removal of first line
	
	values = []
	for each in lines:
		values.append(each.split(';'))

	response_value = []
	time_mark =[]
	packets = []

	for each in values:
		response_value.append(each[1])
		time_mark.append(each[3])
		packets.append(each[2])

	ok = 0
	not_ok = 0

	for each in packets:
		if each == 'True':
			ok +=1
		if each == 'False':
			not_ok +=1

	sum_count = 0
	for each in response_value:
		sum_count = sum_count + float(each)

	prumer = sum_count / len(response_value)

	print('-----------------------------------------------')
	print('Sent '+str(len(packets))+' packets.')
	print('OK: '+str(ok)+' LOST: '+str(not_ok))
	print('AVG response: '+ str(round(prumer, 2))+' ms')
	print('-----------------------------------------------')
	print('Ping went from: '+time_mark[0]+' to: '+time_mark[len(time_mark)-1])
	print('-----------------------------------------------')
	

	a = input('Next ping?: (y/n) ')

	if a == 'n':
		sys.exit()
	if a == 'y':
		main()


def ping_itself(ip):

	try:

		today = dt.today()
		today = today.strftime('%d.%m.%Y')
		pc_ID = os.environ['COMPUTERNAME']
		exists_log = os.path.exists(str(pc_ID)+'_ping_'+ip+'_'+str(today)+'.txt')

		i = 0

		while exists_log == True:
			i += 1
			exists_log = os.path.exists(str(i)+'_'+str(pc_ID)+'_ping_'+ip+'_'+str(today)+'.txt')
			if exists_log == False:
				os.rename(str(pc_ID)+'_ping_'+ip+'_'+str(today)+'.txt', str(i)+'_'+str(pc_ID)+'_ping_'+ip+'_'+str(today)+'.txt')


		with open(str(pc_ID)+'_ping_'+ip+'_'+str(today)+'.txt', 'a') as out:
			out.writelines('target_IP;response_value_ms;response_success;time_mark\n')

		while 1:

			with open(str(pc_ID)+'_ping_'+ip+'_'+str(today)+'.txt', 'a') as out:

				response_valueonse = ping(ip, size=40, count=1)
				now = datetime.now()
				current_time = now.strftime("%H:%M:%S")
				
				print(ip+'  '+ str(response_valueonse.rtt_avg_ms)+'  '+str(response_valueonse.success())+'  '+str(current_time))
				out.writelines(ip+';'+ str(response_valueonse.rtt_avg_ms)+';'+str(response_valueonse.success())+';'+str(current_time)+'\n')

			time.sleep(1)
	except KeyboardInterrupt:
		sum_countmary(str(pc_ID)+'_ping_'+ip+'_'+str(today)+'.txt')

def main():
	try:
		address = input('Write IP (192.168.0.1): ')
		if address == '':
			print("No IP supplied - press CTRL + C to exit")
			main()
		else:
			ping_itself(address)

	except KeyboardInterrupt:
		sys.exit()

if __name__ == '__main__':
	main()
	