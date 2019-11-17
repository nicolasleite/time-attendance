#!/bin/sh
#run as root

echo "Checking for local network IP" # assuming type C network IP
NET_IP=$(ip addr | grep "inet " | grep -v "127.0.0.1/8" | awk '{print $2}' | awk -F. '{
			split($0, a);
			a[4] = "*";
			for(i=1; i<=4; i++) {
				if (i!=1)
					printf ".";
				printf a[i]
			}
			printf("\n")
		}')

echo "Network is $NET_IP"
echo ""

# clear old logs
if [ -f tmp/check.log ]; then
	rm tmp/check.log
fi
touch tmp/check.log

# creates database if non-existent
if [ ! -f data/data.db ]; then
	python3 src/init.py
fi

# main loop: check for users connected to the network every five minutes
while [[ true ]]; do
	echo "Initiating user scan"

	# appending new entry to file
	date +"%Y-%m-%d %H:%M" >> tmp/check.log # time
	nmap -sP -n $NET_IP | grep "MAC Address: " | awk '{print $3}' >> tmp/check.log # users' mac addresses
	echo "" >> tmp/check.log # empty line

	echo "Users' scan done"

	if [[ $(date +%H) -ge 19 ]]; then # if it's after 7, fetch day info
		python3 src/fetch_day.py
		echo "Work day finished, sleeping until tomorrow."
		sleep 11h
	else # during working hours, check every five minutes
		sleep 5m
	fi

	echo ""
done
