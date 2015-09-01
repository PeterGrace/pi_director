pi_director 
===========

Introduction
------------
Raspberry Pis are wonderful tools to use for digital signage.  They're inexpensive, they can be connected to commodity TVs and have reasonably good web rendering performance for most signage applications.  This tool allows one to deploy a fleet of Raspberry Pis that can have centralized management, where one can specify which URL each Pi should display.

Known issues
------------
- There's no authentication.  Be very careful to not deploy this in a public place, or if you do, be certain you don't mind if someone stumbles upon it and sends all of your Pis to an adult website.


Getting Started
---------------

This app works best when run inside a Docker container.  
- Clone this repo to your device, then build the Docker image with `docker build -t pifm .` 
- Then run with `docker run -d -p <port>:6543 pifm` where <port> is the tcp port you want the daemon to run on.
- Once the Docker image is up and running, go to http://your-server:port - where your-server is your IP or hostname, and the port is what you specified above.

