#!/bin/bash

##################
##	 iBelotte   ##
##  15/05/2015  ##
##################

echo 'Installation...'

if [[ -e /usr/local/bin/SL_Manager_Server ]]; then
	echo 'SL_Manager_Server has been found.'
	echo -n 'Do you want to replace it with the new one ? (Y/n): '

	read -e replace_directory

	case $replace_directory in
		"" | "Y" | "y" | "o" | "Yes" | "yes" | "O")
			echo 'Purging previous files...'
			sudo rm -r /usr/local/bin/SL_Manager_Server/*
			echo 'Copying news files...'
			sudo cp sources/* /usr/local/bin/SL_Manager_Server
			;;
	esac
else
	echo 'Creating /usr/local/bin/SL_Manager_Server directory...'
	sudo mkdir /usr/local/bin/SL_Manager_Server
	echo 'Copying files...'
	sudo cp sources/* /usr/local/bin/SL_Manager_Server
fi

echo -n 'Do you want the server starts when the Raspberry starts ? (y/N): '

read -e create_daemon

case $create_daemon in
	"Y" | "y" | "o" | "Yes" | "yes" | "O")
		have_to_create_daemon=false

		if [[ -f /etc/init.d/SL_Manager_Server_Daemon ]]; then
			echo -n 'Daemon already exist. Overwrite ? (y/N): '
			read response

			case $response in
				"Y" | "y" | "o" | "Yes" | "yes" | "O")
					have_to_create_daemon=true
					;;
			esac
		else
			have_to_create_daemon=true
		fi

		if [[ have_to_create_daemon ]]; then
			echo 'Creating file...'
			echo "
#!/bin/bash

case \"\$1\" in 
	start)
		#touch /home/pi/ZZZzzzzzzzzzzzzzzz
		sudo python /usr/local/bin/SL_Manager_Server/server.py &
		;;
	*)
		;;
esac" > SL_Manager_Server_Daemon
			sudo mv SL_Manager_Server_Daemon /etc/init.d/
			echo 'File created to /etc/init.d/'

			sudo chmod +x /etc/init.d/SL_Manager_Server_Daemon
			sudo update-rc.d SL_Manager_Server_Daemon defaults
		fi
		;;
esac

echo 'Done.'

exit 0
