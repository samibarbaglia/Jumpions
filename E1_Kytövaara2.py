import time
from machine import Pin, Timer

led = Pin("LED", Pin.OUT)
timer = Timer()

def blink(timer):
    led.toggle()

timer.init(freq=1, mode=Timer.PERIODIC, callback=blink) 


led1=Pin(20,Pin.OUT)
led2=Pin(21,Pin.OUT)
led3=Pin(22,Pin.OUT)


while True:
    time.sleep(1) #001
    led1.value(1)            
    time.sleep(1) 
    led1.value(0)            
    time.sleep(1)
    led2.value(1) #010
    time.sleep(1)
    led2.value(0)
    time.sleep(1)
    led1.value(1) #011
    led2.value(1)
    time.sleep(1)
    led1.value(0)
    led2.value(0)
    time.sleep(1) 
    led3.value(1) #100
    time.sleep(1)
    led3.value(0)
    time.sleep(1)
    led1.value(1) #101
    led3.value(1)
    time.sleep(1)
    led1.value(0)
    led3.value(0)
    time.sleep(1)
    led2.value(1) #110
    led3.value(1)
    time.sleep(1)
    led2.value(0)
    led3.value(0)
    time.sleep(1)
    led1.value(1) #111
    led2.value(1)
    led3.value(1)
    time.sleep(1)
    led1.value(0)
    led2.value(0)
    led3.value(0) 