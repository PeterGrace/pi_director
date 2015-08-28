pi_director 
===========

Introduction
------------
Raspberry Pis are wonderful tools to use for digital signage.  They're inexpensive, they can be connected to commodity TVs and have reasonably good web rendering performance for most signage applications.  This tool allows one to deploy a fleet of Raspberry Pis that can have centralized management, where one can specify which URL each pi should display.

Known issues
------------
- There's no authentication.  Be very careful to not deploy this in a public place, or if you do, be certain you don't mind if someone stumbles upon it and sends all of your Pis to an adult website.


Getting Started
---------------

- This app works best when run inside a docker container.  Build it with `docker build -t pifm .` then run once built with `docker run -d -p <port>:6543 pifm` where <port> is the tcp port you want the daemon to run on.

