#!/usr/bin/env python3
from fabric.api import *
from fabtools import *
import keyring
import os
import random

# from keyrings.alt import file

env.key_filename = [os.path.join(os.environ['HOME'], '.ssh', 'id_rsa')]
env.use_ssh_config = True
env.forward_agent = True
env.password = keyring.get_password('nic', 'iderkun')
env.sudo_password = env.password
env.gateway = 'sbox1.slava.hc.ru'
# keyring.get_keyring()
# keyring.set_keyring(file.EncryptedKeyring())
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




def host_type():
    set_env()
    #run('uname -s')
    #run('hostname')
    # sudo(open_shell())
    sudo('netstat -na|wc -l')


env.key_filename = [os.path.join(os.environ['HOME'], '.ssh', 'id_rsa')]
env.use_ssh_config = True
env.forward_agent = True
env.password = keyring.get_password('nic', 'iderkun')
env.sudo_password = env.password


#@parallel
def block_spammers():
	if int(sudo('exim -bpc'))>40:
		top_senders=[]
		try:
			a=sudo("""exim -bp  | grep '<' | awk {'print $4'} | sort | uniq -c | sort -n""")
			sudo("""/usr/sbin/exim -bp | grep '<>' | awk '{print $3}' | xargs /usr/sbin/exim -Mrm""")
			#a=sudo("""/usr/sbin/exiqgrep -b | awk '{print $3}'|sort | uniq -c | sort -r""")
			#a=sudo("""exipick -i --show-vars authenticated_sender|cut -d\\' -f2|sort|uniq -c|sort -nk1,1|tail -n10""")
		except:
			pass
		rows=a.strip().split('\r\n')
		for row in rows:
			mail_count,sender_acc=row.strip().split()
			if int(mail_count) > 0:
				top_senders.append((sender_acc, mail_count))
			else:
				pass
		print(top_senders)
		'''
		sudo("""/usr/sbin/exim -bp | grep '<>' | awk '{print $3}' | xargs /usr/sbin/exim -Mrm""")
		for host in top_senders:
			print(host)
			if host[0]=='':
				print(host[1])
				
		'''
			
		#print(top_senders)
			

		