#!/usr/bin/python

import smtplib
import os


def mx_lookup(hostname=''):
	mx = "dig +short %s mx | sort -n | awk '{print $2;exit}' | dig +short -f -"
	mx = mx % hostname
	output = os.popen(mx)
	return output.readline().strip()

def verify_mail(email):
	hostname = email.split('@')[1]
	SMTP_Server = mx_lookup(hostname)
	smtp = smtplib.SMTP(SMTP_Server)
	smtp.putcmd('vrfy', email)
	result_code = smtp.getreply()[0]
	smtp.quit()
	return result_code

def main():
	print (verify_mail('example@example.com'))

if __name__ ==  "__main__":
	main()
