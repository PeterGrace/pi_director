pi_director 
===========

Introduction
------------
Raspberry Pis are wonderful tools to use for digital signage.  They're inexpensive, they can be connected to commodity TVs and have reasonably good web rendering performance for most signage applications.  This tool allows one to deploy a fleet of Raspberry Pis that can have centralized management, where one can specify which URL each Pi should display.

Known issues
------------
- Why did I implement all this auth stuff and not add a way to authenticate the first administrator?  Ugh.


Getting Started
---------------

This app works best when run inside a Docker container.  
- Clone this repo to your system
- Add your google oauth keys to production.ini in the velruse.google.* fields (https://console.developers.google.com)
- Build the Docker image with `docker build -t pifm .` 
- Then run with `docker run -d -p <port>:6543 pifm` where <port> is the tcp port you want the daemon to run on.
- Go to http://your-server:port/authorize/your-email@gmail.com to create a user for yourself that has admin rights.  NOTE: this url will not work once there is at least one administrator in your database.
- Once the Docker image is up and running, go to http://your-server:port - where your-server is your IP or hostname, and the port is what you specified above.

