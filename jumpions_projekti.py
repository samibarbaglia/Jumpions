# HARDWARE 2 PROJECT by JUMPIONS (Sami Barbaglia, Ellen Järvenpää, Eemi Korhonen, Eveliina Kytövaara)
# Final code done by the group and with the help of other classmates (Kim L., Samu K.)
# Shout out to MJÄYYY Karamalmi Koodarikissa <33

from piotimer import Piotimer
from machine import ADC, Pin, I2C
from fifo import Fifo
import utime
from ssd1306 import SSD1306_I2C
import math

# variables
sample_rate = 250
adc = ADC(26)
sample_fifo = Fifo(300)
avg_window = 20
avg_fifo = Fifo(avg_window)

led = Pin("LED", Pin.OUT)
bpm_fifo = Fifo(10)
utime.sleep(1)

# OLED
width = 128
height = 64
i2c = I2C(1, scl=Pin(15), sda=Pin(14))
oled = SSD1306_I2C(width, height, i2c)


def read_sample(tid):
    sample_fifo.put(adc.read_u16())

# bpm calculator
def hr(ppi_counter):
    if ppi_counter != 0:
        bpm = 60 / (ppi_counter * 0.004)
        return bpm

# floating average calculator for bpm
def avg_hr(bpm):
    bpm_fifo.put(round(bpm))
    if bpm_fifo.empty(): 
        return
    avg_bpm = bpm_fifo.average()
    bpm_fifo.get()
    pulse = avg_bpm
    return pulse

# median of ppi
def mean_ppi(heart_rate):
    return round(sum(heart_rate) / len(heart_rate))

# now calculate ppi
def calc_mean_ppi(bpm):
    if hr != 0:
        ppi = 60000 / bpm
        return round(ppi)
    else:
        return None
    
# calculate sdnn    
def calc_sdnn(sdnn_intervals):
    if sdnn_intervals != 0:
        mean_nn = sum(sdnn_intervals) / len(sdnn_intervals)
        deviations = [sdnn_interval - mean_nn for sdnn_interval in sdnn_intervals]
        squared_deviations = [deviation**2 for deviation in deviations]
        sum_squared_deviations = sum(squared_deviations)
        n = len(sdnn_intervals)
        sdnn = (sum_squared_deviations / n)**0.5
        return round(sdnn)
    else:
        return None
    
# calculate rmssd   
def calc_rmssd(rr_intervals):
    differences = []
    rmssd = 0
    if rr_intervals != 0:
        for i in range(1, len(rr_intervals)):
            diff = rr_intervals[i] - rr_intervals[i-1]
            differences.append(diff ** 2)
            mean_diff = sum(differences) / len(differences)
            rmssd = mean_diff ** 0.5
        return round(rmssd)
    else:
        return None

        
def display_oled(heart_rate, ppi, sdnn, rmssd):
    oled.fill(0)
    oled.text("MEAN HR: " + str(heart_rate) + " BPM", 0, 0)
    oled.text("MEAN PPI: " + str(ppi) + "ms", 0, 15)
    oled.text("SDNN: " + str(sdnn) + "ms", 0, 30)
    oled.text("RMSSD: " + str(rmssd) + "ms", 0, 45)
    oled.show()
        
        
tmr = Piotimer(mode = Piotimer.PERIODIC,
               freq = sample_rate,
               callback = read_sample)

ppi_list = []
peak_value = 0
ppi_counter_list = []
ppi_counter = 0

#main
while True:  
    if not sample_fifo.empty():
        value = sample_fifo.get()
        
        avg_fifo.put(value)
        curr_value = avg_fifo.average()
        avg_fifo.get()
        
        max_value = sample_fifo.fifo_max()
        min_value = sample_fifo.fifo_min()
        threshold = sample_fifo.threshold(0.15)
        ppi_counter += 1

        if curr_value > threshold: #signal is rising
            led.on()
            peak_value = curr_value
        elif peak_value > threshold: #lets not calculate the peak too many times
            bpm = hr(ppi_counter)
            if 50 < bpm < 150:
                #print("MJÄYYYYYY")
                heart_rate = avg_hr(bpm) # floating average of hr
                ppi = calc_mean_ppi(bpm)
                ppi_counter_list.append(ppi_counter)
                sdnn = calc_sdnn(ppi_counter_list)
                rmssd= calc_rmssd(ppi_counter_list)
                display_oled(heart_rate, ppi, sdnn, rmssd)
                #for demo
                print("bpm: " + str(bpm), "/ ppi: " + str(ppi), "/ sdnn: " + str(sdnn), "/ rmssd: " + str(rmssd))
                print(" ")

            ppi_counter = 0
            peak_value = 0
        elif curr_value < threshold: #signal is falling
            led.off()
                