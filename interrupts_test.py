# https://youtu.be/9Fio0BlMsVM
import machine
import utime 
import time


Warning_LED = machine.Pin(16, machine.Pin.OUT)  # create an output pin for warning LED
Warning_LED.value(0)                            # Set it to OFF

Buzzer = machine.PWM(machine.Pin(13))
Buzzer.duty_u16(0)


def Pb_Switch_INT_wersja_gorsza(pin): # wykona sie gdy wystapi przerwanie
    global Pb_Switch_State
    Pb_Switch.irq(handler=None) # wylaczenie irq = interrupt request handler, podczas wykonywania programu w petli przerwania.
    # Oznacza to ze nie wystapi przerwanie gdy bedzie sie wykonywalo przerwanie xd

    if Pb_Switch.value() == 1: # co ma sie stac gdy przycisk jest wcisniety (podczas IRQ_RISING)
        Pb_Switch_State = 1 # update current state of switch
        
        # tu sie wykonuje to co ma sie stac gdy przycisk wcisniety
        Warning_LED.value(1)
        print("=============\nLED on")

    elif Pb_Switch.value() == 0: # co ma sie stac gdy przycisk nie jest wcisniety (podczas IRQ_FALLING)
        Pb_Switch_State = 0
        Warning_LED.value(0)
        print("=============\nLED off")

    # po wykonaniu wszystkiego co ma sie wykonac w petli przerwania trzeba znowu wlaczyc flage przerwania przycisku
    Pb_Switch.irq(handler=Pb_Switch_INT_wersja_gorsza)


def Pb_Switch_INT_wersja_lepsza(pin):
    global Pb_Switch_State
    Pb_Switch.irq(handler=None) # wylaczenie irq = interrupt request handler, podczas wykonywania programu w petli przerwania.
    # Oznacza to ze nie wystapi przerwanie gdy bedzie sie wykonywalo przerwanie xd

    if (Pb_Switch.value() == 1) and (Pb_Switch_State == 0): # jesli przycisk jest wcisniety i state jest na "low", wykonuje sie jezeli jest zmiana stanu przycisku
        Pb_Switch_State = 1 # update current state of switch
        
        # tu sie wykonuje to co ma sie stac gdy przycisk wcisniety
        Warning_LED.value(1)
        Buzzer.duty_u16(1500)
        print("=============\nLED ON\t Buzzer ON")
        

    elif (Pb_Switch.value() == 0) and (Pb_Switch_State == 1): # jesli przycisk jest wylaczony i state jest na "high", wykonuje sie jezeli jest zmiana stanu przycisku
        Pb_Switch_State = 0

        Warning_LED.value(0)
        Buzzer.duty_u16(0)
        print("=============\nLED OFF\t Buzzer OFF")

    # po wykonaniu wszystkiego co ma sie wykonac w petli przerwania trzeba znowu wlaczyc flage przerwania przycisku
    Pb_Switch.irq(handler=Pb_Switch_INT_wersja_lepsza)


Pb_Switch = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_DOWN) # przycisk ktory bedzie wywolywal przerwanie, pull down ustawia w stanie niskim
Pb_Switch.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=Pb_Switch_INT_wersja_lepsza) # ustawienie co ma sie stac gdy wystapi przerwanie

Pb_Switch_State = Pb_Switch.value() # ustawienie pb_switch_state na wartosc jaka ma pb_switch przed startem programu
print(f"Pb_Switch_State = {Pb_Switch_State}")

# nieskonczona petla programu
print("while loop starts\n\n")
while True:
    utime.sleep(1)

