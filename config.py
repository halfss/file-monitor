#!/usr/bin/env python2.7
#coding=utf8

import sys

#服务器名字，会用在报警邮件的主题中，以区别服务器
server_name='demo'

#要监控的目录,可以有多个，用''包括，并用','隔开
#会定期对这个目录进行比对，检查目录下的文件是否有更改,如果文件有改变检查是否含有木马关键字
monitor_dir=['/data/www/wwwroot','/data/www/wwwtoor','/usr']

#要检查的目录，可以用多个，用''包括，并用','隔开
#会定期对这些目录下的所有文件内容进行检查是否含有某些关键字（与监控不同的是，不检查文件是否有改变，都检查关键字）
check_dir=['/root','/data/www/wwwroot/data/cache','/data/www/wwwroot/bbs/data/cache']

#不需要检查的目录
#如果要监控和检查的目录下有些目录不想监控或检查，写在这里,不能为空,仅仅写不想检出哦监控的目录名即可，以\/开头，并以|隔开
non_dir='\/log|\/threadcache'

#要检查的文件的类型（通过后缀名的最后2个之母判断）
check_type=['ml','tm','hp','js']

#监控周期，0代表仅仅执行一次。
#多长时间检查一次（单位:秒）
cycle=5


#-------------------------------------------------------------------------------------------------------------------------
#这下面的最好就别动了，除非你真正知道你在干什么

#数据存放目录
#本程序生成的数据的存放目录（默认当前目录下的server_name目录下）
#win平台的话，需要将下面的/改成\\
data_dir=sys.path[0]+'/'+server_name+"/"

#data_dir=server_name+"/"

#生成的md5列表
monitor_file_md5=data_dir+'monitor_file_md5.txt'

#检查结果
result_txt=data_dir+'result.txt'

#仅仅检查的目录的md5
check_file_md5=data_dir+'check_file_md5.txt'

#进程文件
pidfile=data_dir+'pidfile'

#报警地址，mail_to_list可以有多个，以逗号隔开
mail_to_list=['12345678@sina.com','12345678@qq.com']
#mail_to_list=['67888954@qq.com','caojincheng@cy2009.com','1093049199@qq.com','liujiwei@cy2009.com']

#邮件记录
#这里会记录所有的发送记录
mail_log=data_dir+'email.log'

#要检查关键字，正则表达式，python会检查改变或新增文件中是否含有这些
check_contents='phpspy|c99sh|milw0rm|eval\(base64_decode|spider_bc|eval\(gzinflate\(base64_decode'

#邮件主题
#不同情况下邮件有不同的主题
sub_hacked=server_name+'-很可能被黑了，快来看看啊！'#只要有文件检查出木马关键字，主题就是这个
sub_changed=server_name+'-有文件内容改变，你要来看看啊！'#没有文件被黑，有文件被改，主题就是这个
sub_losted=server_name+'-有文件丢了，你要来看看啊！'#没有文件被黑，也没有文件被改，仅仅有文件丢失，主题就是这个
