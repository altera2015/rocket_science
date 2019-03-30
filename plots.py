#
# Handy plots
#

import matplotlib.pyplot as plt
import numpy as np
from vect import Vector

def plot_accelleration_due_to_mass_to_alt( body, altitude ):
    altitude_list = []
    gravity_list = []
    pos = Vector()
    

    steps = 1000
    for i in range(steps):
        alt = i * altitude / steps
        pos[2] = body.radius + alt
        altitude_list.append( alt )
        gravity_list.append ( body.accelleration( pos ).magnitude )

    fig = plt.figure()

    fig.suptitle('Acceleration due to gravity vs distance from surface')  # Add a title so we know which it is
    ax = fig.subplots(1,1)
    ax.plot(altitude_list, gravity_list, 'r')
    ax.set_xlabel("Altitude [m]")
    ax.set_ylabel("Acceleration due to Gravity $m/s^2$")
    ax.grid()
    plt.show()

def plot_air_pressure_to_alt( body, altitude ):
    altitude_list = []
    air_pressure_list = []
    density_list = []
    pos = Vector()

    steps = 1000
    for i in range(steps+1):
        alt = i * altitude / ( steps )
        pos[2] = body.radius + alt
        altitude_list.append( alt )
        P0, density = body.air_pressure_and_density( pos )
        air_pressure_list.append ( P0 )
        density_list.append ( density )

    fig = plt.figure()

    fig.suptitle('Air pressure at altitude')  # Add a title so we know which it is
    ax = fig.subplots(1,1)
    ax2 = ax.twinx()
    ax.plot(altitude_list, air_pressure_list, 'r')
    ax2.plot(altitude_list, density_list, 'b')
    ax.set_xlabel("Altitude [m]")
    ax.set_ylabel("Air pressure $Pa$")
    ax2.set_ylabel("Air density $kg/m^3$")
    ax2.yaxis.label.set_color("blue")
    ax.set_yscale('log')
    ax2.set_yscale('log')
    ax.grid()
    plt.show()        
