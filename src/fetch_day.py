import sqlite3
import datetime
from datetime import timedelta

fmt = '%Y-%m-%d %H:%M'
def fetchEmployee(employee, empConnected, timeLog, db):
	cs = db.cursor()
	lenght = len(empConnected)
	totalTime = 0

	i = 0
	while i < lenght:
		if empConnected[i]:
			totalTime = timedelta()

			begin = timeLog[i]
			while empConnected[i]:
				if i+1 < lenght:
					i += 1
				else:
					break
				
				# checks the next two entries, giving the employee 15 
				# minutes of tolerance 
				if not empConnected[i] and i < lenght:
					if i+1 < lenght:
						if empConnected[i+1]:
							i += 1
							continue
						elif i+2 < lenght:
							if empConnected[i+2]:
								i += 2
								continue
			end = timeLog[i]
			delta = datetime.datetime.strptime(end, fmt) - datetime.datetime.strptime(begin, fmt)
			totalTime = totalTime + delta
		i += 1

	date = timeLog[0].split()
	print("Employee: %s \t Working Hours: %s" % (employee, totalTime))
	cs.execute("INSERT INTO dayLog (UserMAC, TotalTime, Date) VALUES ('%s', '%s', '%s');" % (employee, totalTime, date[0]))



def main():
	timeLog = []
	macLog  = []
	aux 	= []
	flag = True

	with open("tmp/check.log", "r") as file:
		for line in file:
			line = line.rstrip()
			if line == "":
				macLog.append(aux)
				aux=[]
				flag = True
			elif flag:
				timeLog.append(line)
				flag = False
			else:
				aux.append(line)


	db = sqlite3.connect('data/data.db')

	for i in range(0,len(timeLog)-1):
		if macLog[i]:
			for employee in macLog[i]:
				empConnected = []
				for j in range (i, len(macLog)):
					
					if employee in macLog[j]:
						empConnected.append(True)
						macLog[j].remove(employee)
					else:
						empConnected.append(False)
				fetchEmployee(employee, empConnected, timeLog, db)


	db.commit()
	db.close()

if __name__ == '__main__':
	main()
