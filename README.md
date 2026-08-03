

# 🚀 Rocket Flight Simulator

## Overview

This project is a physics-based rocket flight simulator developed in Python. The simulator models the vertical flight of a model rocket by incorporating realistic physical effects including thrust, changing mass, aerodynamic drag, gravity, atmospheric density variation and wind.

The simulation is validated against experimental flight data using the Root Mean Square Error (RMSE), allowing the accuracy of the model to be assessed.

---

## Features

- Time-varying motor thrust curve
- Variable propellant mass
- Thrust-to-weight ratio calculation
- Aerodynamic drag modelling
- Atmospheric density variation with altitude
- Wind speed effects
- Experimental validation using RMSE
- Parametric analysis using Python

---


## Software Used

- Python
- NumPy
- Pandas
- Matplotlib

---

## Results
The simulator was used to investigate the effects of several flight parameters on rocket performance.

The following parameters were analysed:
- Thrust Scale
- Wind Speed
- Drag Coefficient (Cd)
- Time Step
- Thrust-to-Weight Ratio
- Propellant Mass

Performance was evaluated using:
- Maximum Altitude
- Maximum Velocity
- Root Mean Square Error (RMSE) against experimental flight data

---

##Engineering Concepts

This project applies several Aerospace Engineering principles, including:
- Newton's Second Law of Motion
- Variable-mass rocket dynamics
- Aerodynamic Drag
- Atmospheric density variation
- Numerical time integration
- Model validation using experimental data


## Future Improvements

- Add multi-stage rocket capability
- Include launch angle effects
- Improve atmospheric modelling
- Compare with additional experimental datasets
