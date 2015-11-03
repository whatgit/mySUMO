import os, sys

if 'SUMO_HOME' in os.environ:
	tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
	sys.path.append(tools)
else:   
	sys.exit("please declare environment variable 'SUMO_HOME'")

import traci
import traci.constants as tc

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
		#print (" '{0}' speed is : '{1}' at position '{2}', '{3}'".format(v, data.get(tc.VAR_SPEED), data.get(tc.VAR_POSITION)[0], data.get(tc.VAR_POSITION)[1]))


traci.close()
