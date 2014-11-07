#!/usr/bin/python
import re
import optparse
import prlsdkapi
import sys
import os
import fnmatch


try:
	import prlsdkapi.prlsdk
	prlsdk = prlsdkapi.prlsdk
	consts = prlsdkapi.prlsdk.consts
	state = {str(consts.VMS_STOPPED):"stopped",
		str(consts.VMS_RUNNING): "running",
		str(consts.VMS_PAUSED):"paused",
		str(consts.VMS_SUSPENDED):"suspened"}

except ImportError:
	print "[-]Error: Not found module prlsdkapi"
	
def search_vm(server, name, status, memsize, cpucount):
	vm_list = server.get_vm_list().wait()
	result = []
	
	for i in range(vm_list.get_params_count()):
		try:
			vm = vm_list.get_param_by_index(i)
			vm_config = vm.get_config()
			vm_uuid = vm.get_uuid()
			vm_name = vm.get_name()
			vm_stat = vm.get_state().wait()
			vm_stat_code = vm_stat.get_param().get_state()
			vm_state_str= state[str(vm_stat_code)] if str(vm_stat_code) in state.keys() else "unknown"
			vm_memsize = vm_config.get_ram_size()
			vm_cpucount = vm_config.get_cpu_count()
			if (fnmatch.fnmatch(vm_name, name) or name == '')and\
				(vm_state_str == status or status == '')and\
				(eval(str(vm_memsize) + memsize) or memsize is '')and\
				(eval(str(vm_cpucount) + cpucount) or cpucount is ''):
				result.append((vm_uuid, vm_name, vm_state_str, vm_memsize, vm_cpucount))
		except Exception, e:
			print "[-] Error : %s" % e
	return result	
		   

def main():
	COGREEN='\33[92m'
	ENDC='\33[0m'
	usage = '''
prlsearch [-H] [HOST] [options]
-H, --host 								
Default is localhost
-n, --vmname=NAME    					
Name of virtual machine
-s, --state                             
running, stopped, paused, suspened
-m, --memsize="<|>|==|<=|>=NUMBER"       
Memory of VM (MB)
-c, --cpucount="<|>|==|<=|>=NUMBER"      
Amount cpu of VM
-e, --exec								
Excute prlctl command
Example:
- Find all VM with start name test
	 prlsearch --vmname *test
- Find all VM have memory less than 512MB
	prlsearch --memsize "<512"
- Find all VM is running
	prlsearch --state running
- Find all VM is running and stop them.
	prlsearch --state stopped --exec "prlctl stop %s"
'''
	# get arg
	parser = optparse.OptionParser(usage=usage, version="%prog 1.0 beta")
	parser.add_option('-H', '--host', dest="host", default="localhost", type="str")
	parser.add_option('-n', '--vmname', dest="name", default="", type="str")
	parser.add_option('-s', '--state', dest="status", default="", type="str")
	parser.add_option('-m', '--memsize', dest="memsize", default="", type="str")
	parser.add_option('-c', '--cpucount', dest="cpucount", default="", type="str")
	parser.add_option('-e', '--exec', dest="cmd",default='', type="str")
	
	options, remainder = parser.parse_args()
	host = options.host
	name = options.name
	status = options.status
	memsize = options.memsize
	cpucount = options.cpucount
	cmd = options.cmd
	# validation argv
	match_host = fnmatch.fnmatch(host, "*:*:*")
	if not match_host and host != "localhost":
		print usage
		sys.exit(0)
	match_memsize = re.match(r'(>|==|<|<=|>=)(\d+\Z)', memsize)
	if not match_memsize and not memsize is "":
		print usage
		sys.exit(0)
	match_cpu = re.match(r'(>|==|<|<=|>=)(\d+\Z)', cpucount)
	if not match_cpu and not cpucount is "":
		print usage
		sys.exit(0)
	match_cmd = re.match(r'^prlctl\s\w*\s%s', cmd)
	if not match_cmd and not cmd is '':
		print usage
		sys.exit(0)

	# END
	prlsdkapi.init_server_sdk()
	server = prlsdkapi.Server()
	if host == "localhost":
		login = server.login_local('', 0, consts.PSL_NORMAL_SECURITY)
	else:
		host,user,passwd = host.split(':')
		login = server.login(host, user, passwd, 0, 0, consts.PSL_NORMAL_SECRITY)
	result = search_vm(server, name, status , memsize, cpucount)
	if result:
		for item in result:
			try:
				if cmd is '':
					print "%10s | %15s | %5s | %4d | %d" % (item[0], item[1], item[2], item[3], item[4])
				else:
					cmd_exec = cmd % item[0]
					print COGREEN+cmd_exec+ENDC
					print '----------------------------------------------------------'
					os.system(cmd_exec)
					print '----------------------------------------------------------'
			except Exception, e:
				print "[-]Error: %s" % e
		



if __name__ == '__main__':
	try:
		sys.exit(main())
	except:
		pass
