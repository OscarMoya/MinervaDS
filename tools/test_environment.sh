#!/bin/bash

vconfig add eth0 1 
vconfig add eth0 2
vconfig add eth0 3
vconfig add eth0 4
vconfig add eth0 5
vconfig add eth0 6
vconfig add eth0 7
vconfig add eth0 8
vconfig add eth0 9

ifconfig eth0.1 up
ifconfig eth0.2 up
ifconfig eth0.3 up
ifconfig eth0.4 up
ifconfig eth0.5 up
ifconfig eth0.6 up
ifconfig eth0.7 up
ifconfig eth0.8 up
ifconfig eth0.9 up


ifconfig eth0.1 10.10.254.1/24 #This will be the controller MGMT IP
ifconfig eth0.2 10.10.253.1/24 #This Will be the controller DATA

ifconfig eth0.6 10.10.254.2/24 #This will be the client MGMT IP
ifconfig eth0.7 10.10.253.2/24 #This Will be the client DATA

ifconfig eth0.8 10.10.254.3/24 #This will be the server MGMT IP
ifconfig eth0.9 10.10.253.3/24 #This Will be the server DATA

ifconfig eth0.3 10.10.253.20/24 # Server A IP
ifconfig eth0.4 10.10.253.30/24 # Server B IP
ifconfig eth0.5 10.10.253.40/24 # Server C IP

