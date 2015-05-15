#!/bin/bash

##################
##	 iBelotte   ##
##  15/05/2015  ##
##################

echo 'Installation...'

if [[ -e /usr/local/bin/SL_Manager_Server ]]; then
	echo 'SL_Manager_Server has been found.'
	echo 'Do you want to replace it with the new one ? (Y/n):'

	read -e replace_directory

	case $replace in
		"" | "Y" | "y" | "o" | "Yes" | "yes" | "O")
			echo 'Purging previous files...'
			sudo rm -r /usr/local/bin/SL_Manager_Server/*
			echo 'Copying news files...'
			sudo cp sources/* /usr/local/bin/SL_Manager_Server
			;;
		*)
			exit 0
			;;
	esac
else
	echo 'Creating /usr/local/bin/SL_Manager_Server directory...'
	sudo mkdir /usr/local/bin/SL_Manager_Server
	echo 'Copying files...'
	sudo cp sources/* /usr/local/bin/SL_Manager_Server
fi

echo 'Done.'

exit 0