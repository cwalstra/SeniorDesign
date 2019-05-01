# This file is designed to test the use of the water level sensor
# in integration with the Raspberry Pi.

import time
import statistics
import RPi.GPIO as io
from timeit import default_timer as Timer
import queue

LEDblue = 20

def setup():
   io.setwarnings(False)
   io.setmode(io.BCM)
   io.setup(LEDblue, io.OUT)
   io.output(LEDblue, 0)

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

def levelSetup():
    changeFactor = 17
    setup()
    charge()
    init_range = 100
    init_vals = []
    skip_factor = 1.15
    sleep_time = 0.2
    for i in range(init_range):
        init_read = analog_read()
        time.sleep(sleep_time)
        init_vals.append(init_read)

    init_mean = statistics.mean(init_vals)
    good_init_vals = []
    for i in range(len(init_vals)):
        if init_vals[i] != 0.0:
            if (init_vals[i] / init_mean < skip_factor**2) and \
                    (init_mean / init_vals[i] < skip_factor**2):
                good_init_vals.append(init_vals[i])
    initial = statistics.mean(good_init_vals)

    print("Initial mean: " + str(initial))

    stdev_limit = initial / changeFactor
    read_range = 10
    read = []
    for i in range(read_range):
        read.append(initial)
    return read, stdev_limit


def levelOutput(read, stdev_limit, q):
    levelHistory = [0, 0, 0, 0, 0, 0, 0, 0]
    while True:
        start = Timer()
        splash = False
        init_range = 100
        skip_factor = 1.15
        sleep_time = 0.2
        cur_read = analog_read()
        time.sleep(sleep_time)
        io.output(LEDblue, 0)
        if cur_read != 0.0:
            #print("Current reading: " + str(cur_read))
            #print("Mean: " + str(statistics.mean(read)))
            if (cur_read / statistics.mean(read) < skip_factor) and \
                    (statistics.mean(read) / cur_read < skip_factor):
                read.pop()
                read.insert(0, cur_read)

                std_dev = statistics.stdev(read)
                if std_dev > stdev_limit:
                    levelHistory.insert(0, True)
                    levelHistory.pop()
                    io.output(LEDblue, 1)
                else:
                    levelHistory.insert(0, False)
                    levelHistory.pop()

        #print(levelHistory)

        try:
            thing = q.get(False)
            q.put(levelHistory, False)
        except queue.Empty:
            q.put(levelHistory, False)
        except queue.Full:
            thing = q.get()
            q.put(levelHistory, False)

        end = Timer()
