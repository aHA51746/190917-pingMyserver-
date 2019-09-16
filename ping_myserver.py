import re
import os
import time
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


def getState(ip):

	try:
		result = re.search('100',os.popen('ping %s -c 3' %ip).read(),re.S).group()
	except Exception:
		return False
	return result

def mail():

	my_sender=''  # 发件人邮箱账号
	my_pass = ''   # 发件人邮箱密码
	my_user =''      # 收件人邮箱账号，我这边发送给自己

	ret=True
	try:
		msg=MIMEText('建议手动连接','plain','utf-8')
		msg['From']=formataddr(["FromRunoob",my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
		msg['To']=formataddr(["FK",my_user])              # 括号里的对应收件人邮箱昵称、收件人邮箱账号
		msg['Subject']="192.168.123.34 ping不通"                # 邮件的主题，也可以说是标题
		server=smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
		server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
		server.sendmail(my_sender,[my_user,],msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
		server.quit()  # 关闭连接
	except Exception as e:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
		print(e)
		ret=False
	return ret

def main():

	count = 0
	while True:
		ip = '192.168.123.34'
		result = getState(ip)
		if result=='100':
			print('Lost %s %s times' %(ip,str(count)))
			print(time.asctime( time.localtime(time.time() ) ) )
			count += 1
		elif count>0:
			print('Restore connection')
			count = 0
		if count>3:
			while not mail():
				time.sleep(10)
				time.sleep(3600)
		time.sleep(20)

if __name__=='__main__':
	main()

