import machine
import utime

led = machine.Pin(16, machine.Pin.OUT)

class TimeToShow:
    def __init__(self, hours, min, sec):
        self.__hours = hours
        self.__min = min
        self.__sec = sec
        self.is_time_set = False

    def time_set(self):
        self.is_time_set = False
        
        names = ["hours", "minutes", "seconds"]
        print("Please set current time:")
        for i in range(len(names)):
            while True:
                try:
                    user_input = int(input(f"Enter <{names[i]}> and press Enter: "))
                    self.__element_set(names[i], user_input)
                    break
            
                except ValueError:
                    print("Please input integer value")

        self.display_time()
        self.is_time_set = True

    def __element_set(self, name, value):
        if name == "hours":
            self.__hours = value
        if name == "minutes":
            self.__min = value
        if name == "seconds":
            self.__sec = value
        else:
            pass

    def time_reset(self):
        self.is_time_set = False
        self.__hours = 0
        self.__min = 0
        self.__sec = 0
        self.is_time_set = True

    def add_hour(self):
        self.__hours += 1
        if self.__hours == 24:
            self.__hours = 0

    def add_min(self):
        self.__min += 1
        if self.__min == 60:
            self.__min = 0
            self.add_hour()

    def add_sec(self):
        self.__sec += 1
        if self.__sec == 60:
            self.__sec = 0
            self.add_min()

    def display_time(self):
        hours_display = str(self.__hours)
        min_display = str(self.__min)
        sec_display = str(self.__sec)

        if len(hours_display) < 2:
            hours_display = "0" + str(self.__hours)
        if len(min_display) < 2:
            min_display = "0" + str(self.__min)
        if len(sec_display) < 2:
            sec_display = "0" + str(self.__sec)

        print(f"{hours_display}:{min_display}:{sec_display}")

time_to_show = TimeToShow(0, 0, 0)

def clock_callback(timer):
    global time_to_show
    if time_to_show.is_time_set == True:
        time_to_show.add_sec()
        time_to_show.display_time()
    else:
        pass

clock_timer = machine.Timer(period=1000, mode=machine.Timer.PERIODIC, callback=clock_callback)


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
