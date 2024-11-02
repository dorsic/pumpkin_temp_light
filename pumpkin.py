# Note all colors are in order of GREEN, RED, BLUE, WHITE
# RPi Pico ADC4 used as temperature sensor
# 1 Watt NeoPixel module with 1 LED used for the light

import machine
import time
import neopixel

PIXEL_PIN = 28
MAX_TEMP = 15
MIN_TEMP = 0

led = machine.Pin('LED', machine.Pin.OUT)
led.high()

np = neopixel.NeoPixel(machine.Pin(28), 1, 4, 1)
vm = machine.ADC(4)

a2temp = lambda av: 27 - (av * (3.3 / 65535.0) - 0.706)/0.001721

def set_color_i(color):
    np[0] = color
    np.write()
    
def set_color_f(color):
    np[0] = [round(c*256) for c in color]
    np.write()
    
def hsv2color(hue, sat, val):
    #param hue: Hue component. Should be on interval 0..65535
    #param sat: Saturation component. Should be on interval 0..255
    #param val: Value component. Should be on interval 0..255
    
    hue = (hue * 1530 + 32768) // 65536
    r, g, b, w = 0, 0, 0, 255-sat
    if hue < 510:
        (r, g) = (255, hue) if hue < 255 else (510-hue, 255)
    elif hue < 1020:
        (g, b) = (255, hue-510) if hue < 765 else (1020 - hue, 255)
    elif hue < 1530:
        (r, b) = (hue - 1020, 255) if hue < 1275 else (255, 1530 - hue)
    else:
        (r, g, b) = (255, 0, 0)

    r, g, b = round(r*sat/255), round(g*sat/255), round(b*sat/255)
    return (round(g*val/255),round(r*val/255), round(b*val/255), round(w*val/255))


def temp():
    return a2temp(vm.read_u16())

def temp2color(temp):
    t = MAX_TEMP if temp > MAX_TEMP else temp
    t = MIN_TEMP if t < MIN_TEMP else t
    hue = 65535-round(t/(MAX_TEMP-MIN_TEMP)*65535)
    return hsv2color(hue, 250, 255)

def test():
    for i in range(0, 65536, 10):
        set_color_i(hsv2color(i, 255, 55))
        time.sleep(0.01)
    led.low()
           
           
def main():
    while True:
        try:
            t = temp()
            c = temp2color(t)
            set_color_i(c)
            print(f"{t}, {c}")
            time.sleep(1)
        except KeyboardInterrupt as e:
            break
    led.low()
    
main()
