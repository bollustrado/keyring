#!/usr/bin/env python3
from fabric.api import *
import fabtools
import keyring
import os
import random
import sys
import time
#reload(sys)
#sys.setdefaultencoding('utf-8')
import json
import ssl
import urllib3,requests
urllib3.disable_warnings()
#requests.packages.mod.urllib3.disable_warnings()
#from requests.packages.urllib3.exceptions import InsecureRequestWarning
#requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from jira import JIRA
# from keyrings.alt import file

#env.key_filename = [os.path.join(os.environ['HOME'], '.ssh', 'id_rsa')]
#env.use_ssh_config = True
#env.forward_agent = True
env.password = keyring.get_password('nic', 'iderkun')
env.jira_pasword = keyring.get_password('jira', 'iderkun')
env.jira_login = 'iderkun'
env.sudo_password = env.password
env.shell = 'bash -c -l'
#env.gateway = 'sbox1.slava.hc.ru'
# keyring.get_keyring()
#keyring.set_keyring(keyring.keyrings.se)
# keyring.get_keyring()



#env.hosts = ['cf18', 'fe84', 'uweb1102.nic.ru']
#print(env)


def set_env():
	env.key_filename = [os.path.join(os.environ['HOME'], '.ssh', 'id_rsa')]
	env.password = keyring.get_password('nic', 'iderkun')
	env.sudo_password = env.password
	env.use_ssh_config = True
	env.forward_agent = True

	if 'hc.ru' in env.host_string:
		env.user = 'iderkun'
		env.gateway = 'sbox1.slava.hc.ru'
	elif 'uweb' in env.host_string and 'nic.ru' in env.host_string:
		env.user = 'iderkun'
	elif 'nic.ru' in env.host_string and 'uweb' not in env.host_string:
		env.prefix='sudo sudosh'
		env.user = 'iderkun_op'
	else:
		env.forward_agent = True
		env.use_ssh_config = True


env.key_filename = [os.path.join(os.environ['HOME'], '.ssh', 'id_rsa')]
env.use_ssh_config = True
env.forward_agent = True
#env.gateway = 'sbox1.slava.hc.ru'

#env.password = keyring.get_password('nic', 'iderkun')
#env.sudo_password = env.password


@parallel
def block_ddos_hc():
	env.gateway = 'sbox1.slava.hc.ru'
	#env.use_ssh_config = True
	#env.forward_agent = True
	#env.password = keyring.get_password('nic', 'iderkun')
	#env.sudo_password = env.password
	#env.key_filename = [os.path.join(os.environ['HOME'], '.ssh', 'id_rsa')]
	if 'pl' in env.host_string:
		env.block_cmd = '/opt/sbin/fwtable add '
	elif 'fe' in env.host_string:
		env.block_cmd = '/usr/local/sbin/fwtable add '
	else:
		env.block_cmd = "/opt/sbin/ipblocker -a "
	#total_conns = sudo('netstat -na|wc -l')
	#sudo('whoami')
	#print(env)
	#exit()
	while int(sudo('netstat -na|wc -l')) > 600:
		a=sudo("""netstat -na | grep -oE '[0-9]{1,}\.[0-9]{1,}\.[0-9]{1,}\.[0-9]{1,}' | sort | uniq -c | sort -n   | perl -pe 'sub g(){my$s=`geoiplookup @_`;return$s=~/\s(\S\S)\,/?"$1- ":"---"}s/\d+\.\d+\.\d+\.\d+/&g($&)."$&"/eg '""")
		#print(a)
		ddosers=[]
		#ddoser_nets=()
		#others=[]
		for row in a.splitlines():
			if 'RU' not in row and '---' not in row and 'V6' not in row:
				#print(row)
				ddoser_ip = row.strip().split()[2]
				ddosers.append(ddoser_ip)
				#ddoser_nets=[]
			else:
				pass
		#print(ddosers)
		print(len(ddosers))
		#print(others)
		#print(len(others))
		#for ip in ddosers:
		#	sudo(env.block_cmd+ip)

		while len(ddosers)>0:
			r=random.randint(0, len(ddosers)-1)
			try:
				sudo(env.block_cmd+ddosers[r])
			except:
				pass
			ddosers.pop(r)

		#sudo('netstat -na|wc -l')



def close_jira_issues():
	options = {
		'server': 'https://jira.rbc.ru',
		'verify': False,
		'validate': False,
		'async': True
	}
	jira = JIRA(options, basic_auth=(env.jira_login, keyring.get_password('jira', 'iderkun')))
	#duty= jira.filter('17219')
	issues = jira.filter('19222')
	#report = jira.filter('18808')
	#tasks = jira.filter('18807')
	while True:
		s = jira.search_issues(jql_str=issues.jql)
		for i in s:
			try:
				#print(i.fields.assignee.name)
				if i.fields.status.name=='В процессе':
					#if i.fields.assignee.name=='iderkun':
					jira.transition_issue(i, '21')# решено
					print(i.fields.summary, i.fields.status.name)
				else:
					jira.assign_issue(i, env.jira_login)
					jira.transition_issue(i, '11')# в работу
					jira.transition_issue(i, '21')# решено
					print(i.fields.summary, i.fields.status.name)
			except Exception as e:
				print(e)
		time.sleep(900)



def swap():
	if 'fe' in env.host_string:
		try:
			sudo('/usr/local/etc/rc.d/mysql-server restart')
			sudo('swapoff -a && swapon -a')
		except Exception as e:
			print(e)
	else:
		try:
			#sudo('service mysqld restart')
			sudo("swapoff -a && swapon -a")
		except Exception as e:
			print(e)