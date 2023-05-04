# tehtävä 1
import time
from machine import Pin
led=Pin(20,Pin.OUT)
led_2=Pin(21,Pin.OUT)
led_3=Pin(22,Pin.OUT)

while True:
    time.sleep(1)
    led.value(1)            
    time.sleep(1)
    led.value(0)            
    time.sleep(1)
    led_2.value(1)
    time.sleep(1)
    led_2.value(0)
    time.sleep(1)
    led_3.value(1)            
    time.sleep(1)
    led_3.value(0)            
    time.sleep(1) 