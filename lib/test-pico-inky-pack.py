"""Simple test script for 2.9" 296x128 grayscale display.

Supported products:
  * Adafruit 2.9" Grayscale
    * https://www.adafruit.com/product/4777
  """

import time
import busio
import board
import displayio
import terminalio
from adafruit_display_text import label


displayio.release_displays()

# This pinout works on the Raspberry Pi Pico and Pico W and may need to be altered if these pins are being used by other packs or bases.
spi = busio.SPI(board.GP18, MOSI=board.GP19, MISO=board.GP16)  # Uses SCK and MOSI
epd_cs = board.GP17
epd_dc = board.GP20
epd_reset = board.GP21
epd_busy = None

# Make a bus to communicate with the screen.
display_bus = displayio.FourWire(
    spi, command=epd_dc, chip_select=epd_cs, reset=epd_reset, baudrate=400000
)
time.sleep(1)

# Setting parameters for the display.
display = adafruit_uc8151d.UC8151D(
    display_bus,
    width=128,
    height=296,
    rotation=180,
    black_bits_inverted=False,
    color_bits_inverted=False,
    grayscale=True,
    refresh_time=1,
)

# Make a group to write to.
g = displayio.Group()


#lines 0 10, 20, 30 ... to 290
#22 caracters per line
#columns 0 10, 20, 30 ... for tab

def displayText(content, line, column):
    text = content
    text_area = label.Label(terminalio.FONT, text=text)
    text_area.x = line
    text_area.y = column
    return text_area
  
def displayData(light_value,temperature_value,humidity_value):
    g.append(displayText("Sensors Data", 10, 10))
    g.append(displayText("Light: "  + str(light_value) + " Lux" , 10, 20))
    g.append(displayText("Temperature: " + str(temperature_value) + " C", 10, 30))
    g.append(displayText("Humidity: " + str(humidity_value) + " H", 10, 40))
    display.show(g)
    display.refresh()

def updateData(light_value,temperature_value,humidity_value):
    time.sleep(180)  # Adjust the delay as needed, but no les tha 180
    for loop in range (len(g)):
        g.pop()
    g.append(displayText("Sensors Data", 10, 10))
    g.append(displayText("Light: "  + str(light_value) + " Lux" , 10, 20))
    g.append(displayText("Temperature: " + str(temperature_value) + " C", 10, 30))
    g.append(displayText("Humidity: " + str(humidity_value) + " H", 10, 40))
    display.refresh() 

displayData(10,30,0.8)

while True:
    updateData(18,29,0.7)
    
       
    
    