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
from pid import PID
import math

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

r.thrust_direction[1] = 0.2
r.thrust_direction[2] = 1.0
r.thrust_direction.normalize()
print(r.thrust_direction)

# Time
t = 0.0

# Our step size
dt = 0.01


time_list = []
altitude_list = []
y_list = []
drag_list = [] 
velocity_list = []

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

    # Sum Forces: Weight, Rocket Thrust and Drag in 3 dimensions.
    Fs = F_rocket + F_drag + A_gravity * r.mass()
    dv = Fs * (dt / r.mass())
    
    # Time step!
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
    y_list.append( 180.0 * r.position.theta / math.pi )
    velocity_list.append( r.velocity.magnitude )

    # next time step!
    t = t + dt

print("Simulation ran for {} seconds".format(time.time()-start))

fig = plt.figure()

altitude_list = altitude_list
time_list = time_list

fig.suptitle('Rocket altitude vs Time') 
ax, ax3, velocity_ax = fig.subplots(1,3)
ax.plot(time_list, altitude_list, 'r')
ax.set_xlabel("Time [s]")
ax.set_ylabel("Altitude [km]")
ax.grid()

ax2 = ax.twinx()
ax2.plot(time_list, drag_list, 'b')
ax2.set_ylabel("Drag [kN]")


ax3.plot(y_list, altitude_list, 'r')
ax3.set_xlabel("Inclination θ (degrees)")
ax3.set_ylabel("Altitude [km]")
ax3.grid()


velocity_ax.plot(time_list, velocity_list, 'r')
velocity_ax.set_xlabel("Time [s]")
velocity_ax.set_ylabel("Velocity [m/s]")
velocity_ax.grid()

plt.tight_layout()

plt.show()
