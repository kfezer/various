sudo #!/bin/bash
# Script for Automatically deploying Nginx server and website
#Written by Karl Fezer 10/11/2016 for Puppet Technical Challenge
#tested on Ubuntu 16.04
#to exececutre, run chmod +x puppetex.sh then ./puppetex.sh

website_src="https://github.com/puppetlabs/exercise-webpage"
local_dir="/data/www"
echo "Nginx Automation for Puppet Technical Challenge - Karl Fezer"
# Make sure only root can run our script
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

echo "Checking for dependancies"
for cmd in "curl" "git" 
	do
		which_cmd=$(which $cmd)
		if [[ ! -x $which_cmd ]]; then
			echo "puppet-exercise requires $cmd. Please install and retry."
			exit 1
		fi
	done

#check for installation of Nginx
echo "Checking for Nginx installation..."
if ! which nginx > /dev/null 2>&1; then
    echo "Nginx not installed... installing Nginx"
	apt-get update
	apt-get install nginx
else
	echo "Nginx already installed, reloading page"

fi

#halt any previous instances of Nginx
nginx -s quit

#check if directory exists
if [ ! -d $local_dir ]; then
	mkdir -p $local_dir
fi

cd $local_dir

#download latest version of git file

if [ -f "exercise-webpage/index.html" ]; then
    	echo "Reloading website"
	rm -r exercise-webpage
fi
echo "Cloning website from Github"
git clone $website_src
cp /data/www/exercise-webpage/index.html   /var/www/html



cd /etc/nginx/sites-available
#check and make sure default.bakpex exists, if so, configurations already applied

if [ -f "default.bakpex" ]; then
    	echo "Configuration already complete"
else
    	#update configuration file to port 8000 and so index.html is the default page
	echo "Updating Configuration"
	sed -i.bakpex 's/listen 80 default_server;/listen 8000 default_server;/' default
	#sed 's/listen [::]:80 default_server;/listen [::]:8000 default_server;/' default
fi


#Reload Nginx
nginx
nginx -s reload

echo "Server setup successful"

exit 0