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
from atlas import AtlasV401
import plots
import matplotlib.pyplot as plt
from vect import Vector
import time
from pid import PID
import math


def run_simulation(body, rocket, target_orbit):
   
    # Time
    t = 0.0

    # Our step size
    dt = 0.1


    time_list = []
    altitude_list = []
    phi_list = []
    drag_list = []
    thrust_list = []
    velocity_list = []
    mass_list = []

    start = time.time()
    
    rocket.throttle = 1.0

    # Let's run our simulation
    for i in range(75000):
        
        # gravity depends on altitude!
        A_gravity = body.accelleration(rocket.position)

        # Valid up to 2500,000 meters
        P0, density = body.air_pressure_and_density(rocket.position)

        # AUTO PILOT
        # really crude pitch control. Once above target_orbit. start pushing along the surface of the earth        

        # First find orientation of the rocket. We assume this is always
        # along the surface of the earth, which is the tangent of the 
        # position vector.
        orientation = Vector([-rocket.position[1], rocket.position[0],0])
        
        # In order to rotate the force vector 'upwards' a certain degree
        # we need to find the rotation axis. This is the vector orthogonal
        # to the position and the orientation.
        rotation_axis = rocket.position.cross( orientation ).normalize()

        # High tech auto pilot
        # Straight up first, then abruptly point force vector along the
        # surface of the earth at 200km up. Then when orbital velocity is
        # acchieved power down.
        delta = 1.0
        if rocket.position.magnitude > body.radius + 1e3:
            delta = 0.5
        if rocket.position.magnitude > body.radius + 200e3:
             delta = 0.1

        # should really test for velocity parallel with Earth.
        if rocket.velocity.magnitude > 8672.0:
            rocket.throttle = 0.0

        # Negative rotation means point the force vector out from earth
        # along the surface.
        orientation.rotate(  - delta * math.pi/2.0, rotation_axis )
        rocket.set_orientation(orientation.normalize())

        # Force from rocket thurst depends on altitude    
        F_rocket = rocket.thrust(P0)
        
        # Force from drag due to atmosphere
        F_drag = rocket.drag(density)

        # Force from Gravity
        F_gravity = A_gravity * rocket.mass()
        
        # Make sure our airframe can handle!
        F_rocket_mag = F_rocket.magnitude
        F_drag_mag = F_drag.magnitude
        F_gravity_mag = F_gravity.magnitude
        force_mag_list = [F_rocket_mag, F_drag_mag, F_gravity_mag]

        # if the drag magnitude becomes too big, the airframe will break.    
        maxForce = sum( force_mag_list )
        if ( maxForce > rocket.max_forces ):
            print("R.U.D. Rapid Unscheduled Dissambly, too much forces, your rocket broke up in mid flight, iteration {}".format(i))
            print("velocity={} altitude={}, max_force={}, force_list={} delta={}".format(rocket.velocity, rocket.position.magnitude, maxForce, force_mag_list, delta))
            break

        # Sum Forces: Weight, Rocket Thrust and Drag in 3 dimensions.
        Fs = F_rocket + F_drag + F_gravity
        dv = Fs * (dt / rocket.mass())
        
        # Time step!
        rocket.velocity += dv
        rocket.position += rocket.velocity * dt

        # did we make it back to terra firma?
        # hope we are going slow.
        if rocket.position.magnitude < body.radius - 1:
            print("Current Forces = {}".format(force_mag_list))
            if rocket.velocity.magnitude > 5:
                print("R.U.D. Rapid Unscheduled Dissambly, welcome home!")
            else:
                print("Level: Musk, Mars is next")
            break

        # debug print
        if i%5000==0:
            print("velocity={} pos={}, drag={} delta={}".format(rocket.velocity, rocket.position.magnitude, F_drag, delta))

        # step the rocket time ahead, this burns the fuel and potentially does stage sep.
        rocket.time_step(dt, t)
        
        # keep a list of maxForce and position so we can plot.
        time_list.append(t)    
        drag_list.append( ( F_drag_mag  ) / 1000.0 )
        thrust_list.append( (F_rocket_mag ) / 1000.0 )
        altitude_list.append((rocket.position.magnitude - body.radius ) / 1000.0)
        phi_list.append( 180.0 * rocket.position.phi / math.pi )
        velocity_list.append( rocket.velocity.magnitude )
        mass_list.append(rocket.mass())
        # next time step!
        t = t + dt

    print("Simulation ran for {} seconds".format(time.time()-start))

    return time_list, altitude_list, drag_list, velocity_list, phi_list, thrust_list, mass_list



recalculate = True
earth = Earth()

if recalculate:
    
    # 8000kg to LEO please.
    rocket = AtlasV401(8.0e3, Vector([0.0, earth.radius, 0.0]) )
    rocket.velocity = earth.surface_speed(rocket.position)

    time_list, altitude_list, drag_list, velocity_list, phi_list, thrust_list, mass_list = run_simulation(earth, rocket, 150e3)
    np.savetxt('launch.txt', np.c_[time_list, altitude_list, drag_list, velocity_list, phi_list, thrust_list, mass_list], header='time, alt, drag, velocity, phi, thrust, mass_list', delimiter=',')
    altitude_list = np.array(altitude_list)
    phi_list = np.array(phi_list)
else:
    C = np.loadtxt('launch.txt', delimiter=',')
    time_list = C[:,0]
    altitude_list = C[:,1]
    drag_list = C[:,2]
    velocity_list = C[:,3]    
    phi_list = C[:,4]
    thrust_list = C[:,5]
    mass_list = C[:,6]


plots.status_plot(time_list, altitude_list, drag_list, velocity_list, phi_list, thrust_list, mass_list)
plots.plot_trajectory(earth, altitude_list * 1000 + earth.radius, phi_list)



