import machine
import utime

# dioda LED do pinu GP16 przez rezystor do masy 
# przycisk do pinu 3V3Out, druga nozka przycisku do pinu GP15

# program zaczyna pomiar czasu w momencie nacisniecia przycisku i konczy gdy drugi raz sie nacisnie

led = machine.Pin(16, machine.Pin.OUT)
button = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_DOWN)

start_time = 0
end_time = 0
timer_running = False
debounce_time = 0

def btn_func(pin):
    global start_time, end_time, timer_running, debounce_time

    button.irq(handler=None) # wylaczenie na czas wykonywania przerwania
    
    if (button.value() == 1) and (utime.ticks_ms() - debounce_time > 500):
        if not timer_running:
            start_time = utime.ticks_ms()
            print("Timer started...")
            timer_running = True
        else:
            end_time = utime.ticks_ms()
            elapsed_time = utime.ticks_diff(end_time, start_time)
            print(f"Timer stopped. Elapsed time in seconds: {elapsed_time*0.001}")
            timer_running = False 
            led.off()

        debounce_time = utime.ticks_ms() # to jest potrzebne zeby lepiej dzialal przycisk (eliminacja "Debouncing switch"), mozna tez to rozwiazac hardware'owo
    
    button.irq(handler=btn_func) # ponowne wlaczenie przerwania

# button interrupt setup 
button.irq(trigger=machine.Pin.IRQ_RISING, handler=btn_func) # .irq(handler="funkcja ktora ma sie wykonac przy przerwaniu") 

def led_blink(timer):
    if timer_running == True: # LED miga tylko jesli timer jest wlaczony
        led.toggle()
    else:
        pass

led_timer = machine.Timer(period=1000, mode=machine.Timer.PERIODIC, callback=led_blink) # period w milisekundach

led.off()

try:
    print("==============Start of while loop==============")
    while True:
        # Your main code here
        utime.sleep(1)  # Placeholder for your program's main functionality

except KeyboardInterrupt:
    # Code to run when a keyboard interrupt occurs
    print("\nKeyboard interrupt detected. Stopping everything.")

    led_timer.deinit()
    led.off()

finally:
    # Code that will run no matter what, even if there was no exception
    print("Program terminated.")

