from piotimer import Piotimer
from machine import ADC, Pin, I2C
from fifo import Fifo
import utime
from ssd1306 import SSD1306_I2C


sample_rate = 250
adc = ADC(26)
sample_fifo = Fifo(300)
avg_fifo = Fifo(20)
avg_window = 15
avg_fifo = Fifo(avg_window)
led = Pin("LED", Pin.OUT)
bpm_fifo = Fifo(10)
utime.sleep(1)

width = 128
height = 64
i2c = I2C(1, scl=Pin(15), sda=Pin(14))
oled = SSD1306_I2C(width, height, i2c)

heart_rate_data = []
ppi_counter_list = []

def read_sample(tid):
    sample_fifo.put(adc.read_u16())

def hr(ppi_counter):
    if ppi_counter != 0:
        bpm = 60 / (ppi_counter * 0.004)
        return bpm

def avg_hr(bpm):
    bpm_fifo.put(round(bpm))
    if bpm_fifo.empty(): #and (round(bpm)-bpm_fifo.peek_last()) > 20:
        return
    avg_bpm = bpm_fifo.average()
    bpm_fifo.get()
    pulse = avg_bpm
    print(pulse)
    return pulse
        
        
tmr = Piotimer(mode = Piotimer.PERIODIC,
               freq = sample_rate,
               callback = read_sample)

prev_value = 0
prev_peak_time = 0
peak_cand = False
ppi_counter = 0
ppi_list = []
curr_value = 0

while True:  
    if not sample_fifo.empty():
        value = sample_fifo.get()
        
        avg_fifo.put(value)
        sig = avg_fifo.average()
        avg_fifo.get()
        
        max_value = sample_fifo.fifo_max()
        min_value = sample_fifo.fifo_min()
        threshold = sample_fifo.threshold(0.25)
        ppi_counter += 1
        #print(sig, threshold, max_value, min_value, ppi_counter)

        if sig > threshold: #signal is rising
            led.on()
            curr_value = sig
        elif curr_value > threshold:
            bpm = hr(ppi_counter)
            if 50 < bpm < 130:
                print("MJÄYYYYYY :DD")
                heart_rate = avg_hr(bpm)
                print(heart_rate, bpm)
                oled.fill(0)
                oled.text("HR: " + str(heart_rate) + " BPM", 0, 0)
                oled.show()
                if heart_rate is not None:
                    ppi_counter_list.append(ppi_counter)
            ppi_counter = 0
            curr_value = 0
        elif sig < threshold:
            led.off()
                
