# test czujnika temperatury i wilgotnosci DHT11

import machine
import utime
import dht

dht_dataPin = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_DOWN) # podciagamy do GND 

dht_sensor = dht.DHT11(dht_dataPin)

print("while loop starts here")


while True:
    dht_sensor.measure()
    tempCelsius = dht_sensor.temperature()
    humidityPercent = dht_sensor.humidity()

    print("\r", f"Temperature: {tempCelsius}\xb0C, Humidity: {humidityPercent}%", end="")

    utime.sleep(2)

