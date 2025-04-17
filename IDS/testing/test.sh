#!/bin/bash

cd ..

tp_normal=0
fp_normal=0
tn_normal=0
fn_normal=0

tp_dos=0
fp_dos=0
tn_dos=0
fn_dos=0

tp_r2l=0
fp_r2l=0
tn_r2l=0
fn_r2l=0

tp_probing=0
fp_probing=0
tn_probing=0
fn_probing=0

exec 2> /dev/null # Suppress stderr

# Test normal traffic
echo Testing normal traffic

for (( i = 0; i < 10; i++ ))
do

	./script.sh $1 > /dev/null &
	ssh root@192.168.1.80 'nc google.com 80 &;sleep 2;kill -9 $!' # Establish and close harmless TCP connection

	sleep 2 # Window for IDS to detect and classify connection

	# Clean up background processes
	pkill -9 -f script.sh
	pkill -9 -f kdd99extractor

	# Check logs for detected attacks
	if [ -s logs/dos.txt ] || [ -s logs/r2l.txt ] || [ -s logs/probing.txt ]
	then
		((fn_normal++)) # Incorrectly classified normal traffic as attack

		if [ -s logs/dos.txt ]
		then
			((fp_dos++))
		else
			((tn_dos++))
		fi

		if [ -s logs/r2l.txt ]
		then
			((fp_r2l++))
		else
			((tn_r2l++))
		fi

		if [ -s logs/probing.txt ]
		then
			((fp_probing++))
		else
			((tn_probing++))
		fi
	else
		((tp_normal++)) # Correctly identified normal traffic
		((tn_dos++))
		((tn_r2l++))
		((tn_probing++))
	fi

done


# Test DoS attack
echo Testing DoS attack

for (( i = 0; i < 10; i++ ))
do

	./script.sh $1 > /dev/null &
	ssh root@192.168.1.80 'hping3 -S --flood -p 80 192.168.2.1;sleep 2;kill -9 $!' # Run DoS attack

	sleep 2 # Window for IDS to detect and classify connection

	# Clean up background processes
	pkill -9 -f script.sh
	pkill -9 -f kdd99extractor

	# Check logs for detected attacks
	if [ -s logs/dos.txt ] || [ -s logs/r2l.txt ] || [ -s logs/probing.txt ]
	then
		((tn_normal++))

		if [ -s logs/dos.txt ]
		then
			((tp_dos++))
		else
			((fn_dos++))
		fi

		if [ -s logs/r2l.txt ]
		then
			((fp_r2l++))
		else
			((tn_r2l++))
		fi

		if [ -s logs/probing.txt ]
		then
			((fp_probing++))
		else
			((tn_probing++))
		fi
	else
		((fp_normal++))
		((fn_dos++))
		((tn_r2l++))
		((tn_probing++))
	fi

done


# Test R2L attack
echo Testing R2L attack

for (( i = 0; i < 10; i++ ))
do

	./script.sh $1 > /dev/null &
	ssh root@192.168.1.80 'telnet 192.168.2.1 23;sleep 2;kill -9 $!' # Run R2L attack

	sleep 2 # Window for IDS to detect and classify connection

	# Clean up background processes
	pkill -9 -f script.sh
	pkill -9 -f kdd99extractor

	# Check logs for detected attacks
	if [ -s logs/dos.txt ] || [ -s logs/r2l.txt ] || [ -s logs/probing.txt ]
	then
		((tn_normal++))

		if [ -s logs/dos.txt ]
		then
			((fp_dos++))
		else
			((tn_dos++))
		fi

		if [ -s logs/r2l.txt ]
		then
			((tp_r2l++))
		else
			((fn_r2l++))
		fi

		if [ -s logs/probing.txt ]
		then
			((fp_probing++))
		else
			((tn_probing++))
		fi
	else
		((fp_normal++))
		((tn_dos++))
		((fn_r2l++))
		((tn_probing++))
	fi

done


# Test probing attack
echo Testing probing attack
for (( i = 0; i < 10; i++ ))
do

	./script.sh $1 > /dev/null &
	ssh root@192.168.1.80 'nmap 192.168.2.0/24;sleep 2;kill -9 $!' # Run Probing attack

	sleep 2 # Window for IDS to detect and classify connection

	# Clean up background processes
	pkill -9 -f script.sh
	pkill -9 -f kdd99extractor

	# Check logs for detected attacks
	if [ -s logs/dos.txt ] || [ -s logs/r2l.txt ] || [ -s logs/probing.txt ]
	then
		((tn_normal++))

		if [ -s logs/dos.txt ]
		then
			((fp_dos++))
		else
			((tn_dos++))
		fi

		if [ -s logs/r2l.txt ]
		then
			((fp_r2l++))
		else
			((tn_r2l++))
		fi

		if [ -s logs/probing.txt ]
		then
			((tp_probing++))
		else
			((fn_probing++))
		fi
	else
		((fp_normal++))
		((tn_dos++))
		((tn_r2l++))
		((fn_probing++))
	fi

done

exec 2> /dev/tty # Unsuppress stderr

python testing/metrics.py $tp_normal $fp_normal $tn_normal $fn_normal $tp_dos $fp_dos $tn_dos $fn_dos $tp_r2l $fp_r2l $tn_r2l $fn_r2l $tp_probing $fp_probing $tn_probing $fn_probing