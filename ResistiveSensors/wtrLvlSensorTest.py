# This file is designed to test the use of the water level sensor
# in integration with the Raspberry Pi.

import time
import statistics
import RPi.GPIO as io

LED = 20

io.setwarnings(False)
io.setmode(io.BCM)
io.setup(LED, io.OUT)
io.output(LED, 0)

def charge():
    io.setup(25, io.IN)
    io.setup(24, io.OUT)
    io.output(24, 1)
    time.sleep(1)

def discharge():
    io.setup(24, io.IN)
    io.setup(25, io.OUT)
    io.output(25, 0)
    time.sleep(0.05)

def charge_time():
    io.setup(25, io.IN)
    io.setup(24, io.OUT)
    count = 0
    io.output(24, 1)
    while not io.input(25):
        count = count + 1
    return count

def analog_read():
    discharge()
    return charge_time()

charge()
init_range = 100
init_vals = []
skip_factor = 1.15
sleep_time = 0.2
for i in range(init_range):
    init_read = analog_read()
    time.sleep(sleep_time)
    print(init_read)
    init_vals.append(init_read)

init_mean = statistics.mean(init_vals)
good_init_vals = []
for i in range(len(init_vals)):
    if (init_vals[i] / init_mean < skip_factor**2) and \
            (init_mean / init_vals[i] < skip_factor**2):
        good_init_vals.append(init_vals[i])
initial = statistics.mean(good_init_vals)
print("Initial Value: " + str(initial))

stdev_limit = initial / 20
print("StDev Limit: " + str(stdev_limit))
read_range = 10
read = []
for i in range(read_range):
    read.append(initial)
while(True):
    cur_read = analog_read()
    time.sleep(sleep_time)
    print(cur_read)
    io.output(LED, 0)
    if (cur_read / statistics.mean(read) > skip_factor) or \
            (statistics.mean(read) / cur_read > skip_factor):
        print("    Skip")
        continue

    read.pop()
    read.insert(0, cur_read)

    std_dev = statistics.stdev(read)
    print("    " + str(std_dev))
    if std_dev > stdev_limit:
        io.output(LED, 1)

