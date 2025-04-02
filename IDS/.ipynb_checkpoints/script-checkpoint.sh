#! /bin/bash

# Activate python virtual environment
source ../../sklearn-env/bin/activate

# Reset log files
mkdir -p logs
rm -f logs/*

function run_model {

	# Keep function running so it continues to receive records
	while true;
	do
		# Run classifier whenever new record received
		read record && python deployment/classifier.py $1 $record
	done
}

../../kdd99extractor | run_model $1 & # Run feature extractor and pipe output to function

# Kill child processes (i.e. extractor) when script ended
trap "pkill -P $$;exit" EXIT

# Keep script running until interrupt received
while true;
do
	sleep 1
done
