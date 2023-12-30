from machine import ADC
from time import sleep


# odczytuje temperature 

def main():
    tempsensor = ADC(4)
    conversionfactor = 3.3/(65535) # conversja z odczytu z pinu na napiecie

    while True:
        currentvoltage = tempsensor.read_u16() * conversionfactor
        temp = 27 - ((currentvoltage - 0.706) / 0.001721)
        print(f"{str(currentvoltage)} : {str(temp)}")
        sleep(2)


if __name__ == "__main__":
    main()
