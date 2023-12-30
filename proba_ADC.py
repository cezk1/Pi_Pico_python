# https://how2electronics.com/how-to-use-adc-in-raspberry-pi-pico-adc-example-code/
import machine
import utime 

analog_value = machine.ADC(28) # zczytanie wartosci z pinu 28 (ADC2)

while True:
    reading = analog_value.read_u16()
    print(f"ADC: {reading}")
    utime.sleep(0.2)

    