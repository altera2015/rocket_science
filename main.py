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


def run_simulation(body):
    
    #
    # This really needs to be moved into a simulator class.
    # experimenting for now.
    #

    # low earth orbit [m]
    leo_altitude = 420.0e3

    # Let's create our main body that we're trying to get into orbit around
    # earth = Earth()

    # Basic physics
    # plots.plot_accelleration_due_to_mass_to_alt( earth, leo_altitude )
    # plots.plot_air_pressure_to_alt(earth, leo_altitude)

    # Let's launch a single stage rocket straight up and see what happens.
    r = Rocket()
    r.position[0] = 0
    r.position[1] = body.radius
    r.position[2] = 0

    r.thrust_direction[0] = 0.0
    r.thrust_direction[1] = 1.0 # start launching straight up!
    r.thrust_direction[2] = 0.0
    r.thrust_direction.normalize()
   
    # Time
    t = 0.0

    # Our step size
    dt = 0.1


    time_list = []
    altitude_list = []
    phi_list = []
    drag_list = [] 
    velocity_list = []

    start = time.time()
    # Let's run our simulation
    for i in range(500000):
        
        # gravity depends on altitude!
        A_gravity = body.accelleration(r.position)

        # Valid up to 2500,000 meters
        P0, density = body.air_pressure_and_density(r.position)

        # really crude pitch control. Once above 100k. start pushing along the surface of the earth
        if r.position.magnitude > 100000 + body.radius:        
            r.thrust_direction = Vector([-r.position[1], r.position[0],0]).normalize()
            r.throttle = 0.5


        # rocket thurst depends on altitude    
        F_rocket = r.thrust(P0)
        
        # drag due to atmosphere
        F_drag = r.drag(density)

        # if the drag magnitude becomes too big, the airframe will break.    
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
        if r.position.magnitude < body.radius - 1:
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
        altitude_list.append((r.position.magnitude - body.radius ) / 1000.0)
        phi_list.append( 180.0 * r.position.phi / math.pi )
        velocity_list.append( r.velocity.magnitude )
        
        # next time step!
        t = t + dt

    print("Simulation ran for {} seconds".format(time.time()-start))

    return time_list, altitude_list, drag_list, velocity_list, phi_list

recalculate = True
earth = Earth()

if recalculate:
    time_list, altitude_list, drag_list, velocity_list, phi_list = run_simulation(earth)    
    np.savetxt('launch.txt', np.c_[time_list, altitude_list, drag_list, velocity_list, phi_list], header='time, alt, drag, velocity, phi', delimiter=',')
    altitude_list = np.array(altitude_list)
    phi_list = np.array(phi_list)
else:
    C = np.loadtxt('launch.txt', delimiter=',')
    time_list = C[:,0]
    altitude_list = C[:,1]
    drag_list = C[:,2]
    velocity_list = C[:,3]    
    phi_list = C[:,4]


plots.status_plot(time_list, altitude_list, drag_list, velocity_list, phi_list)
plots.plot_trajectory(earth, altitude_list * 1000 + earth.radius, phi_list)



