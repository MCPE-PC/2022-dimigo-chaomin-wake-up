### 초기화 ###

import RPi.GPIO as Gpio
from time import sleep

Gpio.setmode(Gpio.BCM)

Gpio.setup(16, Gpio.OUT)
Gpio.setup(20, Gpio.IN, pull_up_down=Gpio.PUD_DOWN)
Gpio.setup(21, Gpio.OUT)

action = 0

frequencies = list(range(523, 1976)) + list(reversed(range(523, 1976)))
frequenciesNumber = len(frequencies)
frequencyIndex = 0

pressing = False

buzzer = Gpio.PWM(21, 523)

buzzer.start(0)

### 기능 ###

try:
    while True:
        livePressing = bool(Gpio.input(20))
        if pressing != livePressing:
            pressing = livePressing

            if pressing:
                action += 1
                action %= 4
                print("New action: {0}".format(action))

        Gpio.output(16, Gpio.HIGH if action == 1 or action == 3 else Gpio.LOW)

        buzzer.ChangeDutyCycle(80 if action > 1 else 0)

        if action > 1:
            buzzer.ChangeFrequency(frequencies[frequencyIndex])

            frequencyIndex += 1
            frequencyIndex %= frequenciesNumber

        sleep(0.005)
finally:
    buzzer.stop()
    Gpio.cleanup()
    print("빠잉")
