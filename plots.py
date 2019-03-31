#
# Handy plots
#

import matplotlib.pyplot as plt
import numpy as np
from vect import Vector
import math

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


def status_plot(time_list, altitude_list, drag_list, velocity_list, phi_list, thrust_list, mass_list):
    fig = plt.figure(figsize=(10,5))

    fig.suptitle('Rocket Statistics') 
    alt_and_drag_ax, velocity_ax, theta_ax = fig.subplots(1,3)

    alt_and_drag_ax.plot(time_list, altitude_list, 'r')
    alt_and_drag_ax.set_xlabel("Time [s]")
    alt_and_drag_ax.set_ylabel("Altitude [km]")
    alt_and_drag_ax.grid()

    alt_and_drag_ax2 = alt_and_drag_ax.twinx()
    alt_and_drag_ax2.plot(time_list, drag_list, 'b')
    alt_and_drag_ax2.plot(time_list, thrust_list, 'g')
    alt_and_drag_ax2.set_ylabel("Force [kN]")
    #alt_and_drag_ax2.set_yscale('log')


    theta_ax.plot(phi_list, altitude_list, 'r')
    theta_ax.set_xlabel("Azimuth φ (degrees)")
    theta_ax.set_ylabel("Altitude [km]")
    theta_ax.grid()


    velocity_ax.plot(time_list, velocity_list, 'r')
    velocity_ax.set_xlabel("Time [s]")
    velocity_ax.set_ylabel("Velocity [m/s]")
    velocity_ax.grid()

    velocity_ax2 = velocity_ax.twinx()
    velocity_ax2.plot(time_list, mass_list, 'b')    
    velocity_ax2.set_ylabel("Mass [kg]")

    plt.tight_layout()

    plt.show()

def plot_trajectory(body, altitude_list, phi_list):

    fig = plt.figure(figsize=(10,10))
    ax = plt.subplot(1,1, 1, projection='polar')
    ax.plot(phi_list * math.pi / 180.0 , altitude_list, 'r-')
    #fig.suptitle('Rocket Path') 
    #ax = fig.subplots(1,1)
    
    
    angles = np.array(range(360)) * math.pi  / 180.0
    height = np.full((360,), body.radius)
    ax.plot(angles, height, 'bo')

    
    plt.tight_layout()
    plt.show()
