# ##################
# Rocket simulator #
# ##################
#
# Ron Bessems
#
#
# The goal of this project is to build a 'toy' rocket simulator
# capable of simulating ascent of a multi stage rocket.
#
# Trying to simulate as much real physics as I can. Using SI units everywhere.
#
# Current status
#
# 1. Gravity vs altitude [Done]
# 2. Air pressure and density vs altitude [Done]
# 3. Static Thrust [Done]
# 4. Static Drag [Done]
# 5. Plotting of altitude and density, see Max-Q and RUD on re-entry to due excessive drag
# 6. Implement coordinates [Done]
# . Implement earth rotation
# . Give rocket control over its direction []
# . Implement thurst control []
# . Multi Stage []
# . Orbit Calculations []
# . Dynamic Thrust []

import numpy as np
from body import Earth
from rocket import Rocket
import plots
import matplotlib.pyplot as plt
from vect import Vector
import time

#
# This really needs to be moved into a simulator class.
# experimenting for now.
#

# low earth orbit [m]
leo_altitude = 420.0e3

# Let's create our main body that we're trying to get into orbit around
earth = Earth()

# Basic physics
# plots.plot_accelleration_due_to_mass_to_alt( earth, leo_altitude )
# plots.plot_air_pressure_to_alt(earth, leo_altitude)

# Let's launch a single stage rocket straight up and see what happens.
r = Rocket()
r.position[2] = earth.radius

# Time
t = 0.0

# Our step size
dt = 0.01


time_list = []
altitude_list = []
drag_list = [] 

start = time.time()
# Let's run our simulation
for i in range(500000):
    
    # gravity depends on altitude!
    A_gravity = earth.accelleration(r.position)

    # Valid up to 2500,000 meters
    P0, density = earth.air_pressure_and_density(r.position)

    # rocket thurst depends on altitude    
    F_rocket = r.thrust(P0)
    
    # drag due to atmosphere
    F_drag = r.drag(density)

    # if the drag magnitude becomes to big, the airframe will break.    
    dragMagnitude = F_drag.magnitude
    if ( dragMagnitude > 100000):
        print("R.U.D. Rapid Unscheduled Dissambly, too much drag, your rocket broke up in mid flight")
        print("velocity={} pos={}, drag={}".format(r.velocity, r.position, F_drag))
        break

    # sum Weight, Rocket Thrust and Drag in 3 dimensions.

    # Code below uses less temporary objects but is only 3 seconds
    # faster than readable code which takes 29 seconds.
    # go with readable, thank you.

    # Fs = Vector(F_rocket)
    # Fs.add( F_drag )
    # Fs.add( A_gravity.mult(r.mass()))
    # dv = Fs.mult(dt/r.mass())
    # r.velocity.add(dv)
    # r.position.add( r.velocity * dt)

    # Readable!
    Fs = F_rocket + F_drag + A_gravity * r.mass()
    dv = Fs * (dt / r.mass())
    r.velocity += dv
    r.position += r.velocity * dt

    # did we make it back to terra firma?
    # hope we are going slow.
    if r.position.magnitude < -1.0:
        if r.velocity.magnitude > 5:                        
            print("R.U.D. Rapid Unscheduled Dissambly, welcome home!")
        else:
            print("Level: Musk, Mars is next")
        break

    # debug print
    if i%5000==0:
        print("velocity={} pos={}, drag={}".format(r.velocity, r.position, F_drag))

    # burn a little fuel
    r.burn(dt)    
    
    # keep a list of drag and position so we can plot.
    time_list.append(t)    
    drag_list.append( dragMagnitude / 1000.0 )
    altitude_list.append((r.position.magnitude - earth.radius ) /1000.0)

    # next time step!
    t = t + dt

print("Simulation ran for {} seconds".format(time.time()-start))

fig = plt.figure()

altitude_list = altitude_list
time_list = time_list

fig.suptitle('Rocket altitude') 
ax = fig.subplots(1,1)
ax.plot(time_list, altitude_list, 'r')
ax.set_xlabel("Time [s]")
ax.set_ylabel("Altitude [km]")
ax.grid()

ax2 = ax.twinx()
ax2.plot(time_list, drag_list, 'b')
ax2.set_ylabel("Drag [kN]")

plt.show()
