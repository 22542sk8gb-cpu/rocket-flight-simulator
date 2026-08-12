import pandas as pd
import matplotlib.pyplot as plt

print("hello zainab")
data= pd.read_csv("flight_data.csv")
print(data.columns.tolist())
time = data['Time']
altitude = data['altitude']
velocity =[]

for i in range(1, len(altitude)):
    change_in_altitude = altitude[i]- altitude[i - 1]
    change_in_time = time[i]- time[i-1]
    velocity.append(change_in_altitude/change_in_time)

    print("Velocity:", velocity)

highest_velocity = max(velocity)
print("Highest Velocity:", highest_velocity, "m/s")

index= velocity.index(highest_velocity)
time_of_highest_velocity = time[index+1]
print("Time of Highest Velocity:", time_of_highest_velocity, "seconds")

average_velocity = sum(velocity)/len(velocity)
print("Average Velocity:", average_velocity, "m/s")

for i in range (len(velocity)):
    if velocity[i]<0 :
        print(" 🚀Rocket started descending at",time[i+1],"seconds")
        break


print("Rocket Flight Data")
print(time)
print(altitude)
highest = altitude.max()
index = altitude.idxmax()
time_of_apogee = time[index]

print("Rocket Flight Data🚀")
print("Maximum Altitude:", highest, "m")

print("Apogee reached at :",time_of_apogee, "seconds")

plt.plot(time,altitude)
plt.title("Rocket Altitude vs Time")
plt.xlabel("Time (seconds)")
plt.ylabel("Altitude(meters)")
plt.grid(True)
plt.show()