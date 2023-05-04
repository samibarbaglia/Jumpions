from machine import Pin, PWM, I2C
import time
from led import Led
import ssd1306

width = 128
height = 64
i2c = I2C(1, scl=Pin(15), sda=Pin(14))
oled = ssd1306.SSD1306_I2C(width, height, i2c)
mode = 1
pos = 0
prev_pos = 1
PIN_1 = 10
PIN_2 = 11
btn = Pin(12, Pin.IN, Pin.PULL_UP)

# Check buttons state
button_pressed = False

# debounce in ms to stabilize button
debounce_ms = 100

def btn_handler(pin):
    global mode
    global button_pressed
    
    if button_pressed:
        return
 
    mode = not mode
    button_pressed = True
    
    # Clears the button_pressed flag
    button_pressed = False
        
btn.irq(trigger=Pin.IRQ_FALLING, handler=btn_handler)

def choose_led():
    global mode
    global led
    global PIN_1 
    global PIN_2
    global prev_pos
    global pos 

    gpio_1 = Pin(PIN_1, Pin.IN, Pin.PULL_UP)
    gpio_2 = Pin(PIN_2, Pin.IN, Pin.PULL_UP)
    
    prev_1 = gpio_1.value()
    prev_2 = gpio_2.value()
       
    while mode == 1:

        # current state of pins
        curr_1 = gpio_1.value()
        curr_2 = gpio_2.value()
        
        # Determines the direction of rotation
        if prev_1 == 0 and curr_1 == 1:
            if curr_2 == 0:
                pos += 1
            else:
                pos -= 1
        elif prev_2 == 0 and curr_2 == 1:
            if curr_1 == 0:
                pos -= 1
            else:
                pos += 1
        
        # Updates previous state of pins
        prev_1 = curr_1
        prev_2 = curr_2
        
        if pos > 45:
            pos = 0
        if pos < 0:
            pos = 45
        # Checks if the position has changed 
        if pos != prev_pos:
            print("LED's position: ", pos)
            prev_pos = pos
            
        if pos < 15:
            led = PWM(Pin(20))
            led_text = "LED 1"
        elif pos < 30:
            led = PWM(Pin(21))
            led_text = "LED 2"
        else:
            led = PWM(Pin(22))
            led_text = "LED 3"

        oled.fill(0)
        oled.text(led_text, 40, 20)
        oled.show()
            
def update_screen():
    prosent = pos*2
    oled.fill(0)
    oled.text("{}%".format(prosent), 55, 15)
    oled.rect(10, 30, 100, 13, 1)
    oled.fill_rect(10,30,prosent,13,2)
    oled.show()

gpio_1 = Pin(PIN_1, Pin.IN, Pin.PULL_UP)
gpio_2 = Pin(PIN_2, Pin.IN, Pin.PULL_UP)

# Initialize position counter and previous state of pins 
prev_1 = gpio_1.value()
prev_2 = gpio_2.value()

while True:

    if mode == 1:
        choose_led()
    if mode == 0:
        update_screen()
    # Current state of pins
    curr_1 = gpio_1.value()
    curr_2 = gpio_2.value()
    
    # Get direction of rotation
    if prev_1 == 0 and curr_1 == 1:
        if curr_2 == 0:
            pos += 1
        else:
            pos -= 1
    elif prev_2 == 0 and curr_2 == 1:
        if curr_1 == 0:
            pos -= 1
        else:
            pos += 1
    
    # Update previous state of pins
    prev_1 = curr_1
    prev_2 = curr_2
    
    if pos > 50:
        pos = 50
    if pos < 0:
        pos = 0
    # Check if the position has changed
    if pos != prev_pos:
        print("Percent position: ", pos)
        prev_pos = pos
    
    time.sleep(0.001)
    # Controls brightness of LEDs
    led.duty_u16(int(pos) * 100)