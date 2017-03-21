import sys
import glob
import time
import BlinkyTape
import config


class BlinkyAdapter(object):

    def __init__(self):
        serial_ports = glob.glob("/dev/ttyACM0")
        port = serial_ports[0]

        if not port:
            sys.exit("Could not locate a BlinkyTape.")

        print "BlinkyTape found at: %s" % port

        self.bt = BlinkyTape.BlinkyTape(port)
        self.bt.displayColor(0, 0, 0)

        self.colors = [[0, 0, 0]] * config.led_count

        self.fade_steps = 50
        self.fade_pause = 0.02

    def display_colors(self, colors):
        for color in colors:
            self.bt.sendPixel(color[0], color[1], color[2])
        self.bt.show()
        self.colors = colors

    def fade_to_colors(self, colors):
        start_colors = list(self.colors)
        fade_colors = [[0, 0, 0]] * 60
        for fade_step in range(0, self.fade_steps+1):
            time.sleep(self.fade_pause)
            for i in range(0, config.led_count):
                fade_color = self.get_fade_color(start_colors[i], colors[i], fade_step)
                fade_colors[i] = fade_color
            self.display_colors(fade_colors)

    def get_fade_color(self, start_color, end_color, fade_step):
        fade_color = [0, 0, 0]
        for i in range(0, 3):
            start_weight = self.fade_steps-fade_step
            end_weight = fade_step
            fade_color[i] = int(
                float(start_color[i]*start_weight + end_color[i]*end_weight) / self.fade_steps)
        return fade_color
