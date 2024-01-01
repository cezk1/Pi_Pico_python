import machine
import utime
from dht import DHT11


led = machine.Pin(16, machine.Pin.OUT)

class IncorrectTimeInput(Exception):
    def __init__(self):
        pass


def check_input_time(name, input):
    if name == "hours" and input > 23:
        raise IncorrectTimeInput

    if name == "minutes" and input > 59:
        raise IncorrectTimeInput
    

class TimeToShow:
    def __init__(self, name, hours, min, sec):
        self.__name = name
        self.__hours = hours
        self.__min = min
        self.is_time_set = False

    def time_set(self):
        self.is_time_set = False
        
        names = ["hours", "minutes"]
        print("Please set current time:")
        for i in range(len(names)):
            while True:
                try:
                    user_input = int(input(f"Enter <{names[i]}> and press Enter: "))
                    check_input_time(names[i], user_input) # sprawdzenie czy godz lub min podane nie sa poza zakresem
                    self.__element_set(names[i], user_input) # ustwienie czasu
                    break
            
                except ValueError:
                    print("Please input number value.")

                except IncorrectTimeInput:
                    print("Please input hours between 0 and 23 or minutes between 0 and 59.")

        self.display_time()
        self.is_time_set = True

    def __element_set(self, name, value):
        if name == "hours":
            self.__hours = value
        if name == "minutes":
            self.__min = value
        else:
            pass

    def time_reset(self):
        self.is_time_set = False
        self.__hours = 0
        self.__min = 0
        self.is_time_set = True

    def add_hour(self):
        if self.is_time_set == True:
            self.__hours += 1
            if self.__hours == 24:
                self.__hours = 0
        else:
            pass

    def add_min(self):
        if self.is_time_set == True:
            self.__min += 1
            if self.__min == 60:
                self.__min = 0
                self.add_hour()
        else:
            pass

    def display_time(self):
        if self.is_time_set == True:
            hours_display = str(self.__hours)
            min_display = str(self.__min)

            if len(hours_display) < 2:
                hours_display = "0" + str(self.__hours)
            if len(min_display) < 2:
                min_display = "0" + str(self.__min)

            print(f"Time: {hours_display}:{min_display}")

        else:
            pass

time_to_show = TimeToShow("clock1", 0, 0, 0)


class TempHumidSensor(DHT11):
    def __init__(self, name, pin):
        self.__name = name
        self.__pin = pin
        super().__init__(pin)

    def measure_and_display(self):
        self.measure()
        tempCelsius = self.temperature()
        humidPercent = self.humidity()

        print(f"Temperature: {tempCelsius} [Celsius], humidity: {humidPercent} [%]")


temp_sensor_dataPin = machine.Pin(17, machine.Pin.IN, machine.Pin.PULL_DOWN)
temp_sensor = TempHumidSensor("sensor1", temp_sensor_dataPin)

def clock_callback(timer):
    global time_to_show
    global temp_sensor

    if time_to_show.is_time_set == True:
        print("--------------------------------------------------")
        temp_sensor.measure_and_display()

        time_to_show.add_min()
        time_to_show.display_time()

        print("--------------------------------------------------")

    else:
        pass


clock_timer = machine.Timer(period=60000, mode=machine.Timer.PERIODIC, callback=clock_callback)


def led_callback(timer):
    global time_to_show
    if time_to_show.is_time_set == True:
        led.toggle()
    else:
        led.off()

led_timer = machine.Timer(period=1000, mode=machine.Timer.PERIODIC, callback=led_callback)
led_timer.deinit()


try:
    time_to_show.time_set()
    print("==============Start of while loop==============")
    while True:
        # Your main code here
        utime.sleep(1)  # Placeholder for your program's main functionality

except KeyboardInterrupt:
    # Code to run when a keyboard interrupt occurs
    print("\nKeyboard interrupt detected. Stopping everything.")

    led_timer.deinit()
    
finally:
    # Code that will run no matter what, even if there was no exception
    print("Program terminated.")
