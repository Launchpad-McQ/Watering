# Hardware setup:
# __________________________________________________
# Number of relays
relaycount = 16
# Number of DACchips
numchip = 2
# Number of sensors per chip
numinputs = 8
# Number of sensors
sensorcount = 16

# Programs values showing system status. (status of sensors and relays)
# __________________________________________________
# array to store sensor readings
reading_arr = [0]*numchip*numinputs
relayon = [False] * relaycount
sensorval = [0] * sensorcount
temperature = 0

# Schedule settings:
# __________________________________________________
duration = 2
# scheduled watering active
onschedule = False
# Postpone schedule time. seconds
pptime = 300

status = {"relayon": relayon, "sensorval": sensorval, "duration": duration, "onschedule": onschedule, "temperature": temperature}
