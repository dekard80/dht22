# Cyclically reads temperature and humidity from the DHT22/11 sensor with a
# Raspberry Pi and print the readings to the terminal and to a file

from time import localtime, strftime
from Timer import Timer
from Config import Config
from Dht22sensor import Dht22sensor
from board import board_id, D4


# returns the log file name as "year+month+.log"
# and if the file does not exist it creates it
def initLogFile():
    year = str(localtime().tm_year)
    month = str(localtime().tm_mon)
    file = year + "-" + month + ".log"
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
    log_file_name = initLogFile()
    # now = strftime("%Y-%m-%d,%H:%M:%S")  # complete date and time
    now = strftime("%d,%H:%M")
    line = f"{now},{temp:.1f},{hum:.1f},{dp:.1f}\n"
    try:
        with open(log_file_name, mode="a", newline="") as file:
            file.write(line)
    except FileNotFoundError:
        initLogFile()


# print the readings to the terminal
def terminalMsg(temp, hum, dp):
    now = strftime("%H:%M:%S")
    print(f"{now} Temperature: {temp:.1f}°C, Humidity: {hum:.1f}%, Dew point: {dp:.1f}°C")  # noqa: E501


# ------ SETUP --------
# default values
temperature = 0  # °C
humidity = 0  # %
dew_Point = 0  # °C
delay = 2  # seconds
print_on_terminal = True
save_to_file = True

# reading configuration file
# if the file does not exist it is not created and
# the default values ​​will be used
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

timer = Timer(delay, True)
dht22sensor = Dht22sensor(D4)

if print_on_terminal:
    print("Device:", board_id)
    print("DHT22 board pin:", D4)
    print("Reading interval:", delay, "sec.")
    if save_to_file:
        print("Log saved on file", initLogFile())
    print("Start reading DHT22...")


# ------ MAIN --------
try:
    while True:
        if timer.get_state():
            temperature, humidity = dht22sensor.read()
            dew_Point = dht22sensor.dewPoint(temperature, humidity)
            if print_on_terminal:
                terminalMsg(temperature, humidity, dew_Point)
            if save_to_file:
                logFile(temperature, humidity, dew_Point)
            timer.start()
        timer.run()
except KeyboardInterrupt:
    if print_on_terminal:
        print("\nExiting...")
