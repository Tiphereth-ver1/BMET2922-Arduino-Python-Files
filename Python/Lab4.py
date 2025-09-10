import matplotlib.pyplot as plt
import numpy as np
import csv
import time

# Checkpoint 2 Content
figure = plt.figure()
x = np.arange(10)*2
y = np.arange(10)
plt.plot(x,y,"ko-")
plt.xlabel("Brain cells")
plt.ylabel("Probability of death")
plt.title("I like trains")
figure.savefig('example.png', dpi = 600)
plt.close(figure)

#Checkpoint 3 Content
figure2 = plt.figure("Exercise 2.4", figsize=(8,15))
figure2.suptitle("Exercise 2.4")

plt.subplot(2,1,1)
plt.title("memery")
x1 = np.linspace(-np.pi,np.pi,100)
y1 = np.sin(x1)
plt.plot(x1,y1)
plt.ylabel("y or something")
plt.xlabel("x for da win in radians")

plt.subplot(2,1,2)
x2 = np.arange(10)*2
y2 = np.arange(10)
plt.title("IBS")
plt.bar(x2,y2,color="red")
plt.ylabel("y so stupid")
plt.xlabel("x")

figure2.savefig('example2.png', dpi = 600)
plt.close(figure2)

#Checkpoint 4 Content
SAMPLE_TIME = 0.02
total_length = 0

with open('pulse.csv') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    wave = []
    pulse = []
    for row in csvReader:
        wave.append(int(row[0]))
        pulse.append(float(row[1]))
    if len(wave) == len(pulse):
        total_length = len(wave)
    else:
        print("Ensure CSV is formatted correctly")

timer = np.arange(0, total_length*SAMPLE_TIME, SAMPLE_TIME)
print(len(timer))
print(len(wave))
count = 0

plt.ion()

# Create figure and axes
figure3, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 14))
figure3.suptitle("Exercise 2.5")

count = 0
scope = 150
while count + scope < total_length:
    ax1.clear()
    ax2.clear()
    
    ax1.plot(timer[count:count+scope], wave[count:count+scope])
    ax1.set_title("Wave")
    ax1.set_ylabel("Amplitude")
    plt.ylim(1800,2300)

    ax2.plot(timer[count:count+scope], pulse[count:count+scope],"r--")
    ax2.set_title("Pulse")
    ax2.set_xlabel("Time [s]")
    ax2.set_ylabel("Value")
    plt.ylim(0.8,1.5)

    plt.pause(0.2)   # both delay & redraw
    count += 10

# Turn interactive mode off, keep final figure open
plt.ioff()
plt.show()