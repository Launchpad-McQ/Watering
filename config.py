# Number of relays
relaycount = 16
# Number of DACchips
numchip = 2
# Number of sensors per chip
numinputs = 8
# Number of sensors
sensorcount = 16
# array to store sensor readings
reading_arr = [0]*numchip*numinputs
# Status of sensors and relays
relayon = [False] * relaycount
sensorval = [0] * sensorcount
duration = 2
# scheduled watering active
onschedule = False
# Postpone schedule time. seconds
pptime = 300

status = {"relayon": relayon, "sensorval": sensorval, "duration": duration, "onschedule": onschedule}
