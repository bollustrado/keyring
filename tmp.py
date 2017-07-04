#!/usr/bin/env python3
from fabric.api import *
import fabtools
import keyring
import os
import random
import sys
import time

env.key_filename = [os.path.join(os.environ['HOME'], '.ssh', 'id_rsa')]
env.use_ssh_config = True
env.forward_agent = True
env.gateway = 'sbox1.slava.hc.ru'
env.ddosers = []



@parallel
def find_ddosers():
	a = sudo(
		"""netstat -na | grep -oE '[0-9]{1,}\.[0-9]{1,}\.[0-9]{1,}\.[0-9]{1,}' | sort | uniq -c | sort -n   | perl -pe 'sub g(){my$s=`geoiplookup @_`;return$s=~/\s(\S\S)\,/?"$1- ":"---"}s/\d+\.\d+\.\d+\.\d+/&g($&)."$&"/eg '""")
	# print(a)

	# ddoser_nets=()
	# others=[]
	for row in a.splitlines():
		if 'RU' not in row and '---' not in row and 'V6' not in row:
			# print(row)
			ddoser_ip = row.strip().split()[2]
			env.ddosers.append(ddoser_ip)
		# ddoser_nets=[]
		else:
			pass

@parallel
def block_ddoser(ipaddr):
	sudo(env.block_cmd + ipaddr)


@parallel
def fuck_them_all():
	if 'pl' in env.host_string:
		env.block_cmd = '/opt/sbin/fwtable add '
	elif 'fe' in env.host_string:
		env.block_cmd = '/usr/local/sbin/fwtable add '
	else:
		env.block_cmd = "/opt/sbin/ipblocker -a "

	while int(sudo('netstat -na|wc -l')) > 600:
		find_ddosers()
		print(len(env.ddosers))
		while len(env.ddosers)>0:
			#r=random.randint(0, len(ddosers)-1)
			try:
				block_ddoser(env.ddosers[-1])
			except:
				pass
			env.ddosers.pop(-1)