from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time
from led import Led

i2c = I2C(1, sda=Pin(14), scl=Pin(15), freq = 400000)
oled = SSD1306_I2C(128, 64, i2c)


class Button_handler:
    
    def __init__(self, pin_number, led_number):
        self.led = Led(led_number)
        self.button = Pin(pin_number, mode = Pin.IN, pull = Pin.PULL_UP)
        
        
def interrupt(pin):
    button1.led.value(0)
    button2.led.value(0)
    button3.led.value(0)

button1 = Button_handler(9, 20)
button2 = Button_handler(8, 21)
button3 = Button_handler(7, 22)

emergency_button = Pin(12, mode = Pin.IN, pull = Pin.PULL_UP)

emergency_button.irq(handler = interrupt, trigger = Pin.IRQ_FALLING)

def update_oled():
    led1_value = button1.led.value()
    led2_value = button2.led.value()
    led3_value = button3.led.value()
    
    oled.fill(0)
    oled.text('eka valo: ' + str(led1_value), 0, 0)
    oled.text('toka valo: ' + str(led2_value), 0, 16)
    oled.text('kolmas valo: ' + str(led3_value), 0, 32)
    oled.show()


while True:
    if button1.button.value() == 0:
        button1.led.toggle()
        while button1.button.value() == 0:
            pass

    if button2.button.value() == 0:
        button2.led.toggle()
        while button2.button.value() == 0:
            pass
        
        
    if button3.button.value() == 0:
        button3.led.toggle()
        while button3.button.value() == 0:
            pass
        
    update_oled()
        
    time.sleep_ms(200) 