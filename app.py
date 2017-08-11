import threading
import time

import sys

import config
from datetime import datetime
from jenkins_adapter import get_section_state_dict
from blinky_adapter import BlinkyAdapter
from model import Led

leds = [Led([0, 0, 0], None)] * 60



def get_colors():
    colors = [Led([0, 0, 0], None)] * config.led_count

    state_dict = get_section_state_dict()
    for section, section_state in state_dict.iteritems():
        state_color_key = section_state.state + "_building" if section_state.building else section_state.state
        color = config.color_mapping[state_color_key]
        for i in range(section.range_start, section.range_end+1):
            colors[i] = color
    print 'INFO: %s' % str(datetime.now())
    print ''.join('{}: {}{}\n'.format(key.name, val.state, "_building" if val.building else "") for key, val in state_dict.items())
    print '-----------------------------------\n'
    return colors

def active_time_range():
    now = datetime.now().time()
    return config.shutdown_time > now > config.startup_time


def led_to_colors(leds, fade_in):
    colors = [[0, 0, 0]] * config.led_count
    for i, led in enumerate(leds):
        colors[i] = led.secondary_color if led.secondary_color is not None and fade_in else led.primary_color
    return colors


def blink_worker():
    global leds
    fade_in = True
    while True:
        fade_in = not fade_in
        if active_time_range():
            colors = led_to_colors(leds, fade_in)
            blinky.fade_to_colors(colors)


if __name__ == "__main__":

    try:

        blinky = BlinkyAdapter()

        blinker = threading.Thread(target=blink_worker)
        blinker.daemon = True
        blinker.start()

        print("Starting...")
        while True:
            if active_time_range():
                leds = get_colors()
            time.sleep(config.request_interval)

    except (KeyboardInterrupt, SystemExit):
        sys.exit()
