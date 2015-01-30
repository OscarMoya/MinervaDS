#!/bin/bash

vconfig add eth0 1 
vconfig add eth0 2
vconfig add eth0 3
vconfig add eth0 4
vconfig add eth0 5

ifconfig eth0.1 up
ifconfig eth0.2 up
ifconfig eth0.3 up
ifconfig eth0.4 up
ifconfig eth0.5 up

ifconfig eth0.1 10.10.254.1/24 #This will be the controller IP
ifconfig eth0.2 10.10.253.1/24 #Client Manager IP
ifconfig eth0.3 10.10.253.20/24 # Server A IP
ifconfig eth0.4 10.10.253.30/24 # Server B IP
ifconfig eth0.5 10.10.253.40/24 # Server C IP

