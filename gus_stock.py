#coding=utf-8

import time
import itchat
import datetime
import tushare as ts
import requests
import re

stock_symbol = 'sh'

def login():

	itchat.auto_login(enableCmdQR=True)

def get_realtime_stock():
	time = datetime.datetime.now()

	now = time.strftime('%H:%M:%S')
	#if int(now[:2])>9 and int(now[:2])<15:

	data = ts.get_realtime_quotes(stock_symbol)
	#r1 = float(data['price'])
	columns = ['price','time']
	#columns = ['price','bid','ask','time']

	countent = now + '\n'

	print '\n'

	for col in columns:
		countent = countent + str(col)+' : '+str(data[col].values[0]) +'\n'
	print str(col)+' : '+str(data[col].values[0])
	return countent


def other_gus():
	hds = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
	gus_1 = 0
	gus_1_val = 0.0
	gus_0 = 0
	gus_0_val = 0.0
	no_gus = 0
	for page in range(1,6):
	    url = 'http://www.fengjr.com/activity/api/v2/stock/ranking/current?pageSize=10&pageNum=%d&t=1488459849058'%page
	    html = requests.get(url,headers=hds).text

	#print html
	    guess = re.findall('"todayGuessRemark":"(.*?)","totalNums"',html,re.S)
	    for gus in guess:
	        #print gus
	        if gus.find(u'看涨') != -1:
	            gus_1 += 1
	            gus_1_val += float(gus[:7])
	        if gus.find(u'看跌')!= -1:
	            gus_0 += 1
	            gus_0_val += float(gus[:7])
	        if gus.find(u'本轮未猜测') !=-1:
	            no_gus += 1
	        

	
	send_no_gus = u'top50本轮未猜测: %d\n'%no_gus

	if gus_1>0:
	    send_gus_1 = u'top50看涨: %d,%0.2f\n'%(gus_1,gus_1_val/gus_1)
	else:
	    send_gus_1= u'top50看涨: 0, 0\n'

	if gus_0>0:
	    send_gus_0 = u'top50看跌: %d,%0.2f'%(gus_0,gus_0_val/gus_0)
	else:
	    send_gus_0 =  u'top50看跌: 0, 0' 
	print send_no_gus
	print send_gus_1
	print send_gus_0
	return send_no_gus+send_gus_1+send_gus_0

def top1_gus():
	
	hds = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}     
	for page in range(1,11):
         
		url = 'http://www.fengjr.com/activity/api/v2/stock/ranking/current?pageSize=10&pageNum=%d&t=1488459849058'%page
		html = requests.get(url,headers=hds).text

        #print html
		guess = re.findall('"todayGuessRemark":"(.*?)","totalNums"',html,re.S)
            #print html
		peos = re.findall('"mobile":"(.*?)","ranking"',html,re.S)
		for peo,gus in zip(peos,guess):
			if peo == '153****8002' and gus.find(u'本轮未猜测') ==-1:
				gus = 'top1:'+ gus
				#print peo,gus
				#itchat.send(gus,toUserName='zmb_nju')
				#itchat.send(gus,toUserName='YY3214789650')
				return (1,gus)
	return (0,'none')

if __name__ == '__main__':
	login()
	time.sleep(2)
	itchat.send('login success!',toUserName='z_n')
	flag1 = 1 
	flag2 = 1

	while True:
		now_time = datetime.datetime.now()

		now_str = str(now_time.strftime('%H:%M'))

		time.sleep(2)



		#flag3,gus = top1_gus()

		if (now_str>='09:50' and now_str<'11:16'):
			flag3,gus = top1_gus()
			if flag1 and flag3:
				itchat.send(gus,toUserName='z')
				itchat.send(gus,toUserName='Y0')			
				flag1 = 0

		if (now_str>='13:20' and now_str<'14:46'):
			flag3,gus = top1_gus()
			if flag2 and flag3:
				itchat.send(gus,toUserName='z')
				itchat.send(gus,toUserName='Y')			
				flag2 = 0


		if now_str[:4]=='15:0':
			realtime_stock = get_realtime_stock()
			itchat.send(realtime_stock,toUserName='z')
			#itchat.send(realtime_stock,toUserName='Y')
			break
		if now_str[:4]=='11:3':
			realtime_stock = get_realtime_stock()
			itchat.send(realtime_stock,toUserName='z')
			time.sleep(60*8)

		if (now_str>='11:10' and now_str<'11:16') or (now_str >'14:35'and now_str<'14:46'):
			try:
				#stock()
				if int(now_str[-1])%2 == 0:
					top_50gus = other_gus()
					itchat.send(top_50gus,toUserName='znju')
					itchat.send(top_50gus,toUserName='Y')
					
					realtime_stock = get_realtime_stock()
					itchat.send(realtime_stock,toUserName='z_nju')
					#itchat.send(realtime_stock,toUserName='Y')

				
				time.sleep(40)
			except KeyboardInterrupt:
				itchat.send('done bye !\n',toUserNmae='filehelper')
