import sys
import glob
import BlinkyTape


class BlinkyAdapter(object):

    def __init__(self):
        serial_ports = glob.glob("/dev/ttyACM0")
        port = serial_ports[0]

        if not port:
            sys.exit("Could not locate a BlinkyTape.")

        print "BlinkyTape found at: %s" % port

        self.bt = BlinkyTape.BlinkyTape(port)
        self.bt.displayColor(0, 0, 0)

    def display_colors(self, colors):
        for color in colors:
            self.bt.sendPixel(color[0], color[1], color[2])
        self.bt.show()


