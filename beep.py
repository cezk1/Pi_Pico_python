import machine
import utime

buzzer = machine.PWM(machine.Pin(13))

again_input = "y"

while again_input == "y":
    buzzer.duty_u16(1000)
    utime.sleep(10)
    buzzer.duty_u16(0)
    utime.sleep(10)

    user_input = input("Do you want to execute again? (y/n)")
    again_input = str(user_input.lower())

