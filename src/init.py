import sqlite3


def main():
	db = sqlite3.connect('data/data.db')
	cs = db.cursor()

	cs.execute	("CREATE TABLE employee (\
					Name	TEXT	NOT NULL,\
					MacAdd	TEXT	NOT NULL, \
					UserID	INTEGER	PRIMARY KEY\
				);")

	cs.execute 	("CREATE TABLE dayLog (\
					UserMAC		INTEGER	NOT NULL,\
					TotalTime	TEXT	NOT NULL,\
					Date		TEXT	NOT NULL,\
					FOREIGN KEY (UserMAC) REFERENCES employee(MacAdd)\
				);")

	db.commit()
	db.close()

if __name__ == '__main__':
	main()