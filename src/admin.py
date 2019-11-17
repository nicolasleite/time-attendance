import sqlite3
import re


def help ():
	print ("List of commands:\n\
\n\
help			show this command guide\n\
show <user_id>	show information on specific user\n\
now 			list users currently connected\n\
quit 			terminate program\n")

def now():
	flag = False
	lastEntry=[]

	with open("tmp/check.log", "r") as file:
		for line in file:
			line = line.rstrip()
			if line == "":
				lastEntry=[]
				flag = True
			elif flag:
				flag = False
			else:
				lastEntry.append(line)

	db = sqlite3.connect('data/data.db')
	cs = db.cursor()

	for user in lastEntry:
		cs.execute("SELECT UserID, Name, MacAdd FROM employee WHERE MacAdd = '%s'" % (user))
		res = cs.fetchall()
		if res:
			print (res)
		else:
			print ("User not in database (MAC Address: %s)" % (user))

	db.close()	

def show(user):
	db = sqlite3.connect('data/data.db')
	cs = db.cursor()

	cs.execute("SELECT Name FROM employee WHERE UserID = '%s'" % (user))
	name = cs.fetchall()

	print ("\nNome: %s\n" % (name))

	cs.execute("SELECT Date, TotalTime FROM dayLog JOIN employee WHERE MacAdd = UserMAC AND UserID = '%s'" % (user))
	res = cs.fetchall()

	print ("Date\t\tWorking time")
	print ("-------------- ------------")
	for item in res:
		print (item)
	print("")

	db.close()

def main():
	opt = ""
	print ("\tWelcome to the server administration software, type 'help' for a list of commands")
	
	while opt != "quit":
		opt = input ("  > ")
		if opt == "help":
			help()
		elif opt == "now":
			now()
		elif re.match("show [0-9]+", opt):
			args = opt.split()
			show(args[1])

	print ("Quitting... ")	

if __name__ == '__main__':
	main()