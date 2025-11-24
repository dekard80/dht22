# Cyclically reads temperature and humidity from the DHT22/11 sensor with a
# Raspberry Pi and print the readings to the terminal and to a file

from time import time, sleep, localtime, strftime
from board import board_id, D4
from adafruit_dht import DHT22
from math import log


# create a timer
class Timer:
    state = False
    time_interval = 0
    initial_time = 0
    cpu_save = False

    def __init__(self, ti, cpus=False):
        self.cpu_save = cpus
        self.time_interval = ti

    def start(self):
        self.initial_time = time()
        self.state = False

    def get_state(self):
        return self.state

    def run(self):
        if (self.initial_time + self.time_interval) < time():
            self.state = True
        # reduces CPU load
        if self.cpu_save:
            sleep(0.01)


# read the configuration file
# the configuration file must be written in the form: key=value
# you can add comments:
# # comment
# or:
# key=value # comment
# the getValue() method always returns strings
# conf equals None if the file does not exist or contains no valid lines
class Config:
    file_name = ""
    conf = {}

    def __init__(self, fn):
        self.file_name = fn
        try:
            with open(self.file_name, "r") as f:
                for line in f:
                    line = line.replace(" ", "")
                    line = line.replace("\n", "")
                    if line == "" or line.startswith("#") or line.count("=") != 1:
                        continue
                    if "#" in line:
                        line = line[:line.find("#")]
                    line = line.split("=")
                    if line[0] == "" or line[1] == "":
                        continue
                    self.conf[line[0]] = line[1]
                if self.conf.__len__() == 0:
                    self.conf = None
        except FileNotFoundError:
            self.conf = None

    def isValid(self):
        if self.conf is None:
            return False
        else:
            return True

    def getValue(self, key):
        if self.conf is not None:
            if key in self.conf:
                return self.conf[key]
        return None


# calculate the dew point
def dewPoint(Tc, Rh):
    try:
        Es = 6.11 * pow(10, (7.5 * Tc) / (237.7 + Tc))
        E = (Rh * Es) / 100
        dew_point = (-430.22 + 237.7 * log(E)) / (-log(E) + 19.08)
    except ValueError as error:
        return 0.0
    return dew_point


# returns the log file name as "year+month+.log"
# and if the file does not exist it creates it
def initLogFile():
    year = str(localtime().tm_year)
    month = str(localtime().tm_mon)
    file = year + month + ".log"
    try:
        with open(file, "r") as f:
            contenuto = f.readline()
    except FileNotFoundError:
        with open(file, "w") as f:
            f.write("DATE,TIME,TEMPERATURE,HUMIDITY,DEW POINT\n")
    return file


# save readings to log file in csv format
# if the file is deleted during execution it is recreated
def logFile(temp, hum, dp):
    now = strftime("%Y-%m-%d,%H:%M:%S")
    line = f"{now},{temp:.1f},{hum:.1f},{dp:.1f}\n"
    try:
        with open(log_file_name, mode="a", newline="") as file:
            file.write(line)
    except FileNotFoundError:
        initLogFile()


# print the readings to the terminal
def terminalMsg(temp, hum, dp):
    now = strftime("%H:%M:%S")
    print(f"{now} Temperature: {temp:.1f}°C, Humidity: {
          hum:.1f}%, Dew point: {dp:.1f}°C")


# reads the sensor, if the reading is successful it returns True
# otherwise False
# it is based on examples from Adafruit's CircuitPython libraries
# https://github.com/adafruit/Adafruit_CircuitPython_DHT
def sensor_read():
    global temperature
    global humidity
    try:
        temperature = dhtDevice.temperature
        humidity = dhtDevice.humidity
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        return False
    except Exception as error:
        dhtDevice.exit()
        raise error
        return False
    return True


# ------ SETUP --------

# default values
temperature = 0  # °C
humidity = 0  # %
dew_Point = 0  # °C
delay = 2  # seconds
print_on_terminal = True
save_to_file = True

# reading configuration file
# if the file does not exist it is not created, the default values ​​will be used
config = Config("dht.conf")
if config.isValid():
    if config.getValue("delay").isdecimal():
        delay = int(config.getValue("delay"))
    if config.getValue("print_on_terminal") == "no":
        print_on_terminal = False
    if config.getValue("save_to_file") == "no":
        save_to_file = False

# use DHT11 for DHT11 sensor
# use use_pulseio=False on Raspberry Pi board
# change D4 based on the pin on which the sensor is connected
dhtDevice = DHT22(D4, use_pulseio=False)
timer = Timer(delay, True)
if save_to_file:
    log_file_name = initLogFile()

if print_on_terminal:
    print("Device:", board_id)
    print("DHT22 board pin:", D4)
    print("Reading interval:", delay, "sec.")
    if save_to_file:
        print("Log saved on file", log_file_name)
    print("Start reading DHT22...")


# ------ MAIN --------
try:
    while True:
        if timer.get_state():
            # try to read the sensor until the reading is successful
            while not sensor_read():
                sleep(2)
            dew_Point = dewPoint(temperature, humidity)
            if print_on_terminal:
                terminalMsg(temperature, humidity, dew_Point)
            if save_to_file:
                logFile(temperature, humidity, dew_Point)
            timer.start()
        timer.run()
except KeyboardInterrupt:
    if print_on_terminal:
        print("\nExiting...")
