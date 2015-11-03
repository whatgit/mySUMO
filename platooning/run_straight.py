#!/usr/bin/python

import os, sys

if 'SUMO_HOME' in os.environ:
	tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
	sys.path.append(tools)
else:   
	sys.exit("please declare environment variable 'SUMO_HOME'")

import traci
import traci.constants as tc
import numpy as np
import socket
import struct
import time

#For Driving simulator
ds_ip = "194.47.15.51"	#driving simulator's IP address
ds_port = 8888
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ds_ip, ds_port))


#For TraCI
PORT = 8813
traci.init(PORT)

step = 0

runningVehicles = []
departedVehicles = []
subscribedVehiclesParameters = [tc.VAR_SPEED, tc.VAR_POSITION]
data = {}

traci.simulation.subscribe()



while step < 120:
	step = traci.simulation.getCurrentTime() / 1000;
	traci.simulationStep()
	departedVehicles = traci.simulation.getDepartedIDList()
	for v in departedVehicles:
		if v not in runningVehicles:
			runningVehicles = runningVehicles + departedVehicles
			traci.vehicle.subscribe(v, subscribedVehiclesParameters, 0, 0x7FFFFFFF)

	for v in runningVehicles:
		data = traci.vehicle.getSubscriptionResults(v)
		message = "{0}{1}{2}{3}{4}{5}".format(chr(0x02), struct.pack('!I', len(v)), v, struct.pack('!d', data.get(tc.VAR_POSITION)[0]), struct.pack('!d', data.get(tc.VAR_POSITION)[1]), struct.pack('!d',data.get(tc.VAR_SPEED)))
		msg_size = str(chr(len(message)))
		message = msg_size + message
		sock.send(message)
		#time.sleep(0.01)

traci.close()
sock.close()






