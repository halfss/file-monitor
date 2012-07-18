#!/usr/bin/env python2.7
#coding=utf8
import email
import mimetypes
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
import smtplib


server = 'smtp.*****.com'
user = '********'
passwd = '***********'

fromAdd = 'monitor@monitor.com'
toAdd = ['12345678@qq.com','12345678@sina.com']
subject = 'hello ,boy title'
plainText = '这里是普通文本'
htmlText = '<B>HTML文本</B>'

def sendEmail(toAdd,subject,htmlText):
        strTo = ','.join(toAdd)
        # 设定root信息
        msgRoot = email.MIMEMultipart.MIMEMultipart('related')
        msgRoot['Subject'] = subject
        msgRoot['From'] = fromAdd
        msgRoot['To'] = strTo
        msgRoot.preamble = 'This is a multi-part message in MIME format.'
        # Encapsulate the plain and HTML versions of the message body in an
        # 'alternative' part, so message agents can decide which they want to display.
        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)
        #设定纯文本信息
#        msgText = MIMEText(plainText, 'plain', 'utf-8')
#        msgAlternative.attach(msgText)
        #设定HTML信息
        msgText = email.MIMEText.MIMEText(htmlText, 'html', 'utf-8')
        msgAlternative.attach(msgText)
       #设定内置图片信息
#        fp = open('test.jpg', 'rb')
#        msgImage = MIMEImage(fp.read())
#        fp.close()
#        msgImage.add_header('Content-ID', '<image1>')
#        msgRoot.attach(msgImage)
       #发送邮件
	try:
	        smtp = smtplib.SMTP()
       		#设定调试级别，依情况而定
	        #smtp.set_debuglevel(1)
        	smtp.connect(server)
	        smtp.login(user, passwd)
		for i in toAdd:
	        	smtp.sendmail(fromAdd,i, msgRoot.as_string())
#        smtp.sendmail(fromAdd, strTo, msgRoot.as_string())
	        smtp.quit()
		return True
	except Exception,e:
		print str(e)
		return False
if __name__ == '__main__' :
        sendEmail(['a12345678@qq.com'],'','<font color=red>red</font>')
