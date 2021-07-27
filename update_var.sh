#!/bin/bash
shopt -s expand_aliases
alias run="sudo apt "

set echo off
#set all_update=`run update | grep "à jour"`
#echo $(all_update)

echo "Recherche de nouvelles mises à jour ...."

a=$(echo `run update 2>/dev/null | grep "Tous les paquets sont à jour."`) 

if [[ -n "$a" ]]
then
	echo $a 
	#echo "Tout est à jour!"
else
	echo '============================================================================' >> log_update.txt	
	date >> log_update.txt	
	run list --upgradable >> log_update.txt 	
	echo Upgrading ...
	run -y upgrade

	echo Dist-upgrading ...
	run -y dist-upgrade

	echo Cleaning ...
	run autoclean

	echo Autoremove ...
	run autoremove
fi
#sleep 2
#./update.sh
#run update
exit 0