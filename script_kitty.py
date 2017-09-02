# script_kitty.py
# Winston Van
# 0.2
# Auburn University
# Use strip.show()

from __future__ import division
from neopixel import *
from random import randint
import math
import time
import threading

# LED strip configuration:
LED_COUNT      = 150      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 170     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
ICE_RGB = (178, 255, 240)
ICE_SPAN = 11
RED_RGB = (50, 20, 20)
GREEN_RGB = (20, 50, 20)
GOLD_RGB = (255, 215, 0)

BLUE_RGB = (0, 0, 255)
ORANGE_RGB = (75, 255, 0)


def setWave(strip, center, delta, it):
	DIMMED_RGB = tuple([x / delta / it for x in ICE_RGB])
	strip.setPixelColorRGB(center + delta, *(DIMMED_RGB))
	strip.setPixelColorRGB(center - delta, *(DIMMED_RGB))

def eraseWave(strip, center, erase_wave_delay=200):
	time.sleep(erase_wave_delay/1000.0)
	fade_interval = 80
	for x in range (0, ICE_SPAN):
		strip.setPixelColorRGB(center + x, 0, 0, 0)
		strip.setPixelColorRGB(center - x, 0, 0, 0)
		strip.show()
		time.sleep(fade_interval/1000.0)
	print ('eraseWave', center)

def singleDrop(strip, wait_ms=80):
	center = randint(1 + ICE_SPAN, LED_COUNT - ICE_SPAN)	
	
	strip.setPixelColorRGB(center, *(ICE_RGB))
	for it in range(1, 10):
		for delta in range (1, ICE_SPAN):
			if it == delta:
				setWave(strip, center, delta, it)
		strip.show()	
		time.sleep(wait_ms * it/1000.0)
	print ('singleDrop', center)
	e = threading.Thread(name='erase_worker', target=eraseWave, args=(strip, center))
	e.start()


def ribbon(strip, color, forward=True):
	if forward:
		for i in range (0, LED_COUNT):
			strip.setPixelColorRGB(i, *(color))
			strip.show()
	else:
		for i in reverse(range (0, LED_COUNT)):
			strip.setPixelColorRGB(i, *(color))
			strip.show()
	return

def ribbonErase(strip, erase_delay=50, forward=True):
	time.sleep(erase_delay/1000.0)
	if forward:
		for i in range (0, LED_COUNT):
			strip.setPixelColorRGB(i, 0, 0, 60)
			strip.show()
	else:
		for i in reverse(range (0, LED_COUNT)):
			strip.setPixelColorRGB(i, 0, 0, 0)
			strip.show()
	return




def comet(strip, color, length, forward=True):
        # Where head represents the most faded pixel
        for head in range (-1 * length, LED_COUNT):
                for i in range (head, head + length):
                        # Fractional distance from head
                        dist = (i - head) / length
                        # Distance scaled into radians from [0, PI/2)
                        rads_scale = dist * math.pi / 2
                        # Flip to correct for fade direction
                        rads = math.pi / 2 - rads_scale

                        DIMMED_RGB = tuple([int(x * math.cos(rads)) for x in color])

                        if forward:
                            strip.setPixelColorRGB(i, *(DIMMED_RGB))
                        else:
                            strip.setPixelColorRGB(LED_COUNT - i, *DIMMED_RGB)
                # Clean up
                if forward:
                    strip.setPixelColorRGB(head - 1, 0, 0, 0)
                else:
                    strip.setPixelColorRGB(LED_COUNT - (head - 1), 0, 0, 0)
                strip.show()
        return


def beginDrops(quantity=50):
	for drop in range (0, quantity):
		t = threading.Thread(name='init_drop', target=singleDrop, args=(strip,))
		t.start()
		
		time.sleep(600/1000.0)



def clear(strip):
	# Clears the board
	for i in range (0, LED_COUNT):
		strip.setPixelColorRGB(i, 0, 0, 0)
	strip.show()
	print ('clear')	


if __name__ == '__main__':
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
	strip.begin()

	clear(strip)	

	print ('Press Ctrl-C to quit.')
	
	for x in range (0, 150):
		strip.setPixelColorRGB(x, 20, 20, 50)
		strip.show()


	clear(strip)


	while True:

#		beginDrops()

		clear(strip)

		time.sleep(300/1000.0)
		
	#	comet(strip, (randint(0, 255), randint(0, 255), randint(0, 255)), 30)

		comet(strip, BLUE_RGB, 30)
		comet(strip, ORANGE_RGB, 30, False)

		"""

		ribbon_erase_thread = threading.Thread(name='ribbon_erase', target=ribbonErase, args=(strip,))
		ribbon_erase_thread.start()
		ribbon(strip, RED_RGB)

	        """
                
