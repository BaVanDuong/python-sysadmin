#!/usr/bin/python

import os
import os.path
import subprocess
import datetime
import sys

def get_stat(path):
	cmd = 'find %s -type f' % path
	files = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE).communicate()[0]
	files = files.split('\n')
	files.pop()
	list_files_stat = []
	
	for f in files:
		info_file = {}
		info_file['path'] = f
		info_file['size'] = os.path.getsize(f)
		info_file['mtime'] = os.path.getmtime(f)
		list_files_stat.append(info_file)
	return list_files_stat

def delete_files_by_percent(size, usage, percent_max, path):
	list_files = sorted(get_stat(path), lambda k: k['mtime'])
	byte_need_delete = (float(usage) / float(size) - percent_max/100) * usage
	if (list_files is None or byte_to_delete <=0):
		return -1
	index = 0
	while byte_to_delete >= 0:
		print "Delete file ", os.path.split(list_files[index]['path'])[1]
		index = index + 1
		byte_to_delete = byte_to_delete - list_files[index]['size']
	return 0

def delete_files_by_date(days, path):
	list_files = get_stat(path)
		if (list_files is None):
			return -1
	for f in list_files:
		diff = (datetime.date.today() - datetime.date.fromtimestamp(f['mtime'])).days
		if(diff >= days):
			print "Delete file %s, %s" % (f['path'], datetime.date.fromtimestamp(f['mtime']))
	return 0
	
def main():
	if (len(sys.argv)) != 3:
		print """
		Use script with option <percent|day> <value> 
		"""
		sys.exit(0)
		
	if(sys.argv[1] == 'percent'):
		size = 6442450944
		usage = 5712144257
		percent_max = sys.argv[2]
		delete_files_by_percent(size, usage, percent_max, path)
	elif(sys.argv[1] == 'day'):
		days = sys.argv[2]
		delete_files_by_date(90, '/tmp')
	else:
		print """
		Use script with option <percent|day> <value> 
		"""
	
if __name__ == '__main__':
	main()
