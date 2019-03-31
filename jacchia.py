# Jacchia Reference Atmosphere
#
# Data taken from: 
# https://ccmc.gsfc.nasa.gov/modelweb/atmos/jacchia.html
#
# Potentially better data here:
# http://www.dem.inpe.br/~val/atmod/default.html
#
# Even better model is EarthGRAM 2016
# https://software.nasa.gov/featuredsoftware/earth-gram-2016

import math
import csv
import constants

data = []

# Returns the requested columns interpolated
# between ra and rb, relative to altitude and column 0.
def _interpolate(altitude, ra, rb, columns=[1,8,9]):    
    delta = rb[0] - ra[0]
    
    if delta==0:
        part = 0
        delta = 1
    else:
        part = (altitude - ra[0])

    res = []
    for column in columns:        
        res.append(ra[column] + ( rb[column] - ra[column]) * part / delta)
    return res

# returns the air pressure based on the static Jacchia 1977 data.
# Input: altitude is in meters.
# Output: [Pressure in Pascal, density kg/m3.]
__warned = False
def air_pressure_and_density(altitude):
    global __warned
    altitude/=1000.0
    # the 8th column holds the log_10 of the molecule density in one cubic meter.

    entries = len(data)    
    if altitude > data[entries-1][0]:
        if not __warned:
            print("Warning going over max altitude for pressure estimates.")
            __warned = True
        altitude = data[entries-1][0]

    previous = data[0]
    for i in range(len(data)):
        row = data[i]
        if altitude <= row[0]:
            v = _interpolate(altitude, previous, row, [1,8,9])
            temp = v[0]            
            density = math.pow(10, v[1])
            molecular_weight = v[2]
            return [ density * temp * constants.kb, density * constants.kb / constants.R * molecular_weight / 1000.0 ]
        
        previous = row

    print("jacchia.py | unable to estimate pressure.")
    exit(-1)    

# On startup load the parameter table.
with open('jacchia-77/t1000.out', 'rt') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|', skipinitialspace=True)
    for row in spamreader:
        r = []
        for v in row:
            r.append(float(v))
        if len(r) == 10:
            data.append(r)


