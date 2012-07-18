#!/usr/bin/env python2.7
#coding=utf8

import sys
import os
import md5
import re
from config import *
from sendemail import *
from time import sleep

def create_md5(check_dirs,non_dirs,result,is_md5=1):
	'''
	check_dir为传来的要检查的目录
	non_dir为要检查的目录中不需要检查的子目录
	result为检查结果的存放文件位置
	'''
	file_result=open(result,'w')
	for check_dir in check_dirs:
		print check_dir
		print "		create file list..."
		if is_md5:
			for root,dirs,files in os.walk(check_dir):
				if re.findall(non_dirs,root):
					continue
				for name in files:
					file_name=os.path.join(root,name)
					if file_name[-2:] in check_type:
						try:
							file_result.write(file_name+'::'+md5.new(file(file_name).read()).hexdigest()+'\n')
						except IOError:
							pass
		else:
			for root,dirs,files in os.walk(check_dir):
				if re.findall(non_dirs,root):
					continue
				for name in files:
					file_name=os.path.join(root,name)
					if file_name[-2:] in check_type:
						try:
							file_result.write(file_name+'::''\n')
						except IOError:
							pass
		
		
		print "		create files sucess!"			
	file_result.close()
	print "create all files and file's md5 sucess"

def check_file(check_files,check_contents):
	'''
	check_files为要检测的文件，
	
	会返回一个列表，里面中的内容有有制定关键字的行数
	'''
	a=1
	b=[]
	try:
		for line in file(check_files).readlines():
			if re.findall(check_contents,line):
				b.append(a)
			a+=1
		return b
	except IOError:
		pass
def send_result(hacked,changed,losted,contentss):
	global mail_log
	if hacked or changed or losted:
		log=open(mail_log,'a')
		log.write('****************************************\n'+str(mail_to_list)+'\n')
		log.write(str(contentss))
		if hacked:
			changed=0
			losted=0
			print "maybe hacked "
			if sendEmail(mail_to_list,sub_hacked,contentss):
				log.write('sucess\n')
				print "email to ",mail_to_list," sucess"
			else:
				print "send email failed! please check!"
				log.write('failed\n')
		if changed:
			losted=0
			print 'file changed'
			if sendEmail(mail_to_list,sub_changed,contentss):
				log.write('sucess\n')
				print "email to ",mail_to_list," sucess"
			else:
				log.write('failed\n')
				print "send email failed! please check"
		if losted:
			print 'file lost'
			if sendEmail(mail_to_list,sub_losted,contentss):
				log.write('sucess\n')
				print "email to ",mail_to_list," sucess"
			else:
				log.write('failed\n')
				print "send failed! please check"
		log.close()
	else:
		print "So lucky,no suspicious found!"

def daemonize(stdout='/dev/null', stderr=None, stdin='/dev/null',pidfile=None ):
        '''
        This forks the current process into a daemon.
        The stdin, stdout, and stderr arguments are file names that
        will be opened and be used to replace the standard file descriptors
        in sys.stdin, sys.stdout, and sys.stderr.
        Note that stderr is opened unbuffered, so
        if it shares a file with stdout then interleaved output
        may not appear in the order that you expect.
        '''
        # Do first fork.
	try:
		pid = os.fork()
		if pid > 0: sys.exit(0) # Exit first parent.
	except OSError, e:
		sys.stderr.write("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror))
		sys.exit(1)
	# Decouple from parent environment.
	os.chdir("/")
	os.umask(0)
	os.setsid()

        # Do second fork.
	try:
		pid = os.fork()
		if pid > 0: sys.exit(0) # Exit second parent.
	except OSError, e:
		print 'second fork error'
		sys.stderr.write("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror))
		sys.exit(1)
	# Open file descriptors and print start messag
	if not stderr: stderr = stdout
	si = file(stdin, 'r')
	so = file(stdout, 'w')
	se = file(stderr, 'a+', 0)
	pid = str(os.getpid())
	print "Start with Pid: %s\n"  % pid
	sys.stderr.flush()
	if pidfile: file(pidfile,'w').write("%s\n" % pid)
	# Redirect standard file descriptoris.
	sys.stdout.flush()
	sys.stderr.flush()
	os.dup2(si.fileno(), sys.stdin.fileno())
	os.dup2(so.fileno(), sys.stdout.fileno())
	os.dup2(se.fileno(), sys.stderr.fileno())
def move_check_from_monitor():
	global monitor_file_md5
	global check_file_md5
	global check_dir
	global non_dir
	dict_old={}
	for k,v in [line.split("::") for line in file(monitor_file_md5,'r').readlines() if line]:
		dict_old[k]=v
	create_md5(check_dir,non_dir,check_file_md5)
	for files,md5 in [line.split("::") for line in file(check_file_md5,'r').readlines() if line]:
		try:
			del dict_old[files]
		except:
			pass
	files=open(monitor_file_md5,'w')
	for k,v in dict_old.items():
		files.write(k+'::'+v)
	files.close()

	
help_me='''
help
-------------------------------------------------

you can read README to detail info

check must have one parameter of "start","stop","all" ,"last"


start
	check start with daemon,and every cycle(set in 
	config.py)seconds  check dirs in config.
	if the dirs have files changed(file content changed,
	file lost,now file) or have suspicious	email 
	them to "mail_to_list".
stop
	stop the  check process whick the last start.
all
	check all dirs  in config to find wheather they
	have suspicious
last
	check the dirs in config to make sure that they
	don't have changed(file content changed,file 
	lost,new file) and che changed file don't 
	have suspicious,if not,	proces will email 
	che change or suspicious to mail_to_list 
	in config


'''

def setup():
	if not os.path.exists(data_dir):
		os.popen('mkdir -p '+data_dir)
