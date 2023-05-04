from machine import I2C, Pin
import network
import time
from ssd1306 import SSD1306_I2C
from machine import I2C, Pin

i2c = I2C(1, sda=Pin(14), scl=Pin(15), freq = 400000)
oled = SSD1306_I2C(128, 64, i2c)


# enable station interface (STA_IF)
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# connect to WiFi access point
wlan.connect('KMD657Group3', 'Jumpions!3E1S')

while not wlan.isconnected() and wlan.status() >= 0:
    print("Waiting to connect:")
    time.sleep(1)
    
print(wlan.ifconfig())

oled.fill(0)
oled.text("IP address:", 0, 0)
oled.text(wlan.ifconfig()[0], 0, 10)
oled.show() 