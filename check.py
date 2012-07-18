#!/usr/bin/env python
#coding

import os
import sys
from create import *
from time import time,sleep

hacked=0
changed=0
losted=0
just_hacked=0
hacked_content=''
changed_content=''
losted_content=''


def check_hacked(files,status):
	global hacked
	global changed
	global hacked_content
	global changed_content
	result=''
	resu=check_file(files, check_contents)
	if resu:
		hacked=1
		hacked_content+="<font color=red>"+files+" - the "+str(resu)+" row(s) maybe hacked!"+status+"</font><br/>\n"
	else:
		changed=1
		changed_content+=files+" - program have not find suspicious! "+status+"<br/>\n"

def start():
	global hacked
	global changed
	global losted
	global hacked_content
	global changed_content
	global losted_content
	hacked=0
	changed=0
	losted=0
	content=''
	hacked_content=''
	changed_content=''
	losted_content=''
	if not os.path.exists(monitor_file_md5):
		create_md5(monitor_dir,non_dir,monitor_file_md5)
		move_check_from_monitor()
	os.popen('mv '+monitor_file_md5+' '+monitor_file_md5+'.old')
	dict_old={}
	for k,v in [line.split("::") for line in file(monitor_file_md5+'.old','r').readlines() if line]:
		dict_old[k]=v

	create_md5(monitor_dir,non_dir,monitor_file_md5)
	move_check_from_monitor()
	print "****************************************\nStart compare......"	
	for files,md5s in [line.split("::") for line in file(monitor_file_md5,'r').readlines() if line]:
		if files in dict_old.keys():
			if md5s!=dict_old[files]:
				check_hacked(files,'changed')
			del dict_old[files]
		else:
			check_hacked(files,'new')
	if len(dict_old):
		losted=1
		for files in dict_old.keys():
			losted_content+="<font color=gray>"+files+"-losted</font><br/>\n"
	content=hacked_content+changed_content+losted_content
	print "****************************************\ncompare over"
	print 'hacked=%d,changed=%d,losted=%s' % (hacked,changed,losted)
	print content+"\n"
	send_result(hacked,changed,losted,content)

def once(check_dir=check_dir):
	create_md5(check_dir,non_dir,check_file_md5,0)
	content=''
	print "----------------------------------------\nstart check..."
	for files,md5 in [line.split("::") for line in file(check_file_md5,'r').readlines() if line]:
		rows=check_file(files,check_contents)
		if rows:
			content+="<font color=red>"+files+" the "+str(rows)+" rows maybe hacked!</font><br/>\n"
	print "----------------------------------------\ncheck over"
	if content:
		print content+'\n'
		return content
	else:
		print "so lucky,process have not  suspicious found!\n"

def daemon(cycle):
	os.popen("echo '' >"+data_dir+'stdout.log')
	checked=0
	check_content=''
	while cycle:
		start()
		content=once()
		if content!=check_content:
			if content:
				send_result(1,0,0,content)
			check_content=content
		sleep(cycle)
		


if __name__=="__main__":
	setup()
	if len(sys.argv)==2:
		if sys.argv[1]=='last':
			start()
			sys.exit(1)
		if sys.argv[1]=='all':
			once_check_dir=monitor_dir+check_dir
			content=once(once_check_dir)
			if content:
				send_result(1,0,0,content)
			sys,exit(1)
		if sys.argv[1]=='stop':
			pid=file(pidfile,'r').readline()
			if len(pid)>2:
				os.system("kill "+pid[:-1]+"&& echo '' > "+pidfile)
				print '\nThe check process is been stop sucess!\n'
			else:
				print '\nThe check process maybe have been stopped,please check!\n'
			sys.exit(1)
		if sys.argv[1]=='start':
			if not  cycle:
				print "please set 'cycle' in config.py"
				sys.exit()
			daemonize(stdout=data_dir+'stdout.log', stderr=data_dir+'stderr.log',pidfile=pidfile)
			daemon(cycle)
		else:
			print help_me
	else:
		print help_me
