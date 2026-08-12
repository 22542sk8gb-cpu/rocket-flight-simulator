

import matplotlib.pyplot as plt
import math
import pandas as pd
import numpy as np
from pathlib import Path

# Read experimental data
project_root = Path(__file__).resolve().parents[1]
flight_data = pd.read_csv(project_root / "data" / "flight_data.csv")

real_time = flight_data["Time"]
real_altitude = flight_data["altitude"]




def simulate_flight(thrust_scale, wind_speed, cd, dt, propellant_mass):
    """
    Simulates the flight of a model rocket.

    Parameters:
        thrust_scale (float): Multiplier applied to the motor thrust curve.
        wind_speed (float): Wind speed in m/s (positive = tailwind, negative = headwind).
        cd (float): Drag coefficient.
        dt (float): Simulation time step.
        propellant_mass (float): Initial propellant mass in kg.

        Returns:
        time_Data (list): time history.
        altitude_data(list): altitude history.
        velocity_data(list): velocity history.
        rmse (float): Root Mean Square Error between simulated and experimental altitude.
        thrust_to_weight_ratio (float): Initial thrust-to-weight ratio of the rocket.
    """

    # Rocket properties
    rocket_mass = 0.25
    mass_flow_rate = 0.025

#motor thrust curve
    motor_time = [0.0, 0.1, 0.3, 0.8, 1.4, 2.0]

    motor_thrust = [
        8.0 * thrust_scale,
        12.0 * thrust_scale,
        16.0 * thrust_scale,
        15.0 * thrust_scale,
        10.0 * thrust_scale,
        0.0
    ]
#physical constants
    g = 9.81
    diameter = 0.05
#initial conditions
    launch_mass = rocket_mass + propellant_mass
    burn_rate = mass_flow_rate
    burn_time = propellant_mass / mass_flow_rate
#calc thrust to weight ratio
    initial_thrust = max(motor_thrust)
    thrust_to_weight_ratio = initial_thrust / (launch_mass * g)

#flight state variables
    time = 0
    velocity = 0
    altitude = 0
    mass = launch_mass
#rocket geom
    radius = diameter / 2
    area = math.pi * radius**2
#store simulation results
    time_data = []
    altitude_data = []
    velocity_data = []

#main simulaion loop
    while altitude >= 0:

        if time <= burn_time:
            current_thrust = np.interp(time, motor_time, motor_thrust)

            mass -= burn_rate * dt
            if mass < rocket_mass:
                mass = rocket_mass
        else:
            current_thrust = 0

        weight = mass * g
        rho = 1.225 * math.exp(-altitude / 8500)

        relative_velocity= velocity - wind_speed

        if relative_velocity >= 0:
            drag = 0.5 * rho * cd * area * relative_velocity**2
        else:
            drag = -0.5 * rho * cd * area * relative_velocity**2

        net_force = current_thrust - weight - drag
        acceleration = net_force / mass

        velocity += acceleration * dt
        altitude += velocity * dt

        time_data.append(time)
        altitude_data.append(altitude)
        velocity_data.append(velocity)

        time+= dt

        if altitude < 0:
            break

    sim_altitude = np.interp(real_time, time_data, altitude_data)
    rmse = np.sqrt(np.mean((real_altitude - sim_altitude) ** 2))

    return time_data, altitude_data, velocity_data, rmse , thrust_to_weight_ratio


# ----------------------------
# Run several thrust scales
# ----------------------------

thrust_scales = np.arange(0.8, 1.41, 0.01)
wind_speeds = [-10, -5, 0, 5, 10]
cd_values = np.arange(0.6, 1.21, 0.05)
dt_values= [0.2, 0.1, 0.05, 0.02, 0.01]
propellant_masses = np.arange(0.02, 0.101, 0.005)

cd_rmses= []
cd_altitudes = []

for cd in cd_values:
    time_data, altitude_data, velocity_data, rmse ,twr = simulate_flight(1.0, 0, cd, 0.1, 0.05)

    cd_rmses.append(rmse)
    cd_altitudes.append(max(altitude_data))

    print("Cd:", round(cd,2))
    print("Maximum Altitude:", round(max(altitude_data),2),"m")
    print("RMSE:", round(rmse,2),"m")
    print()

dt_rmses= []
dt_altitudes =[]

for dt in dt_values:
    time_data, altitude_data, velocity_data, rmse, twr = simulate_flight(1.0, 0, 0.9, dt, 0.05)

    dt_rmses.append(rmse)
    dt_altitudes.append(max(altitude_data))

    print("Time Step:", dt, "s")
    print("Maximum Altitude:",round(max(altitude_data),2), "m") 
    print("RMSE:", round(rmse, 2),"m")
    print()



twr_values= []
twr_altitudes =[]
twr_rmses= []

for scale in thrust_scales:

    time_data, altitude_data, velocity_data, rmse, twr = simulate_flight(scale, 0 , 0.9, 0.1, 0.05 )
    twr_values.append(twr)
    twr_altitudes.append(max(altitude_data))
    twr_rmses.append(rmse)

    print("Thrust Scale:", round(scale,2))
    print("Thrust-to-Weight Ratio:", round(twr,2))
    print("Maximum Altitude:",round(max(altitude_data),2),"m")
    print("RMSE:", round (rmse,2),"m")
    print()

best_scales = []
best_rmses = []

propellant_altitudes = []
propellant_velocities= []
propellant_rmses = []
propellant_twr= []

for propellant_mass in propellant_masses:

    time_data, altitude_data, velocity_data, rmse, twr = simulate_flight(1.0,0 , 0.9, 0.1,propellant_mass)

    propellant_altitudes.append(max(altitude_data))
    propellant_velocities.append(max(velocity_data))
    propellant_rmses.append(rmse)
    propellant_twr.append(twr)

    print("Propellant Mass:", round(propellant_mass,3),"kg")
    print("Burn Time:", round(propellant_mass/ 0.025 ,2),"s")
    print("Maximum Altitude:",round(max(altitude_data),2),"m")
    print("Maximum Velocity:", round (max(velocity_data),2),"m/s")
    print("Thrust-to-Weight Ratio:", round(twr,2))
    print("RMSE:", round (rmse,2),"m")
    print()

for wind_speed in wind_speeds:

    print("\n================")
    print(f"Wind Speed: {wind_speed} m/s")
    print("================")

    altitudes = []
    rmses = []
    

    best_rmse = float("inf")
    best_scale = None

    

    for scale in thrust_scales:

        time_data, altitude_data, velocity_data, rmse, twr = simulate_flight(scale, wind_speed,0.9, 0.1, 0.05)

        
        if abs(scale - 1.0) < 0.001:
            best_time = time_data
            best_altitude = altitude_data

        altitudes.append(max(altitude_data))
        rmses.append(rmse)

        if rmse < best_rmse:
            best_rmse = rmse
            best_scale = scale

    print("Best Thrust Scale:", round(best_scale, 2))
    print("Minimum RMSE:", round(best_rmse, 2), "m")

    best_scales.append(best_scale)
    best_rmses.append(best_rmse)

print("\nBest Scales:", best_scales)
print("Best RMSEs:", best_rmses)


# ----------------------------
# Graph 1
# ----------------------------

plt.figure(figsize=(8,5))
plt.plot(best_time, best_altitude, label= "Simulation")
plt.plot(real_time, real_altitude, label="Experimental Data")

plt.xlabel("Time")
plt.ylabel("Altitude (m)")
plt.title("Rocket Flight: Simulation vs Experimental Data")
plt.grid(True)
plt.legend()
plt.show()


plt.figure(figsize=(8,5))
plt.plot(thrust_scales, altitudes, marker="o")
plt.xlabel("Thrust Scale")
plt.ylabel("Maximum Altitude(m)")
plt.title("Effect of Thrust Scale on Maximum Altitude")
plt.grid(True)
plt.show()

# ----------------------------
# Graph 2
# --------------------------

plt.figure(figsize=(8,5))
plt.plot(thrust_scales, rmses, marker="o")
plt.xlabel("Thrust Scale")
plt.ylabel("RMSE (m)")
plt.title("Effect of Thrust Scale on Simulation Error")
plt.grid(True)
plt.show()

plt.figure(figsize=(8,5))
plt.plot(wind_speeds, best_scales, marker="o")
plt.xlabel("Wind Speed (m/s)")
plt.ylabel("Best Thrust Scale")
plt.title("Best Thrust Scale vs Wind Speed")
plt.grid(True)
plt.show()

plt.figure(figsize=(8,5))
plt.plot(wind_speeds, best_rmses, marker="o")
plt.xlabel("Wind Speed (m/s)")
plt.ylabel("Minimum RMSE (m)")
plt.title("Minimum RMSE vs Wind Speed")
plt.grid(True)
plt.show()


#drag graphs
plt.figure(figsize=(8,5))
plt.plot(cd_values, cd_rmses, marker="o")
plt.xlabel("Drag Coefficient (Cd))")
plt.ylabel(" RMSE (m)")
plt.title("Effect of Drag Coefficient on Simulation Error")
plt.grid(True)
plt.show()


plt.figure(figsize=(8,5))
plt.plot(cd_values, cd_altitudes, marker="o")
plt.xlabel("Drag Coefficient (Cd))")
plt.ylabel("Maximum Altitude (m)")
plt.title("Effect of Drag Coefficient on Maximum Altitude")
plt.grid(True)
plt.show()

plt.figure(figsize=(8,5))
plt.plot(dt_values, dt_rmses, marker="o")
plt.xscale("log")
plt.xlabel("Time Step (s)")
plt.ylabel("RMSE (m)")
plt.title("Timee-Step Convergence Study")
plt.grid(True)
plt.show()

#twr graphs

plt.figure(figsize=(8,5))
plt.plot(twr_values,twr_altitudes, marker= "o")
plt.xlabel("Thrust-to-weight Ratio")
plt.ylabel("Maximum Altutude(m)")
plt.title("Effect of Thrust-to-Weight Ratio on Maximum Altitude")
plt.grid(True)
plt.show()

plt.figure(figsize=(8,5))
plt.plot(twr_values,twr_rmses, marker= "o")
plt.xlabel("Thrust-to-weight Ratio")
plt.ylabel("RMSE (m)")
plt.title("Effect of Thrust-to-Weight Ratio on Simulation Error")
plt.grid(True)
plt.show()


plt.figure(figsize=(8,5))
plt.plot(propellant_masses, propellant_altitudes, marker= "o")
plt.xlabel("Propellant Mass(kg)")
plt.ylabel("Maximum Altitude (m)")
plt.title("Effect of Propellant Mass on Max Altitude")
plt.grid(True)
plt.show()


plt.figure(figsize=(8,5))
plt.plot(propellant_masses, propellant_velocities, marker= "o")
plt.xlabel("Propellant Mass(kg)")
plt.ylabel("Maximum Velocity (m/s)")
plt.title("Effect of Propellant Mass on Max Velocity")
plt.grid(True)
plt.show()

plt.figure(figsize=(8,5))
plt.plot(propellant_masses, propellant_twr, marker= "o")
plt.xlabel("Propellant Mass(kg)")
plt.ylabel("Thrust-to-Weight Ratio")
plt.title("Effect of Propellant Mass on Thrust-to-weight ratio")
plt.grid(True)
plt.show()
