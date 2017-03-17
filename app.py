import sys
import glob
import time
import BlinkyTape
import config


def connect():
    serial_ports = glob.glob("/dev/ttyACM0")
    port = serial_ports[0]

    if not port:
        sys.exit("Could not locate a BlinkyTape.")

    print "BlinkyTape found at: %s" % port

    bt = BlinkyTape.BlinkyTape(port)
    bt.displayColor(0, 0, 0)
    return bt


def get_colors():
    output_colors = [[0, 0, 0]] * 60

    for section in config.sections:

        state = section.get_state()
        color = config.color_mapping[state]

        for i in range(section.range_start, section.range_end+1):
            output_colors[i] = color

    return output_colors


def display_colors(colors):
    for color in colors:
        bt.sendPixel(color[0], color[1], color[2])
    bt.show()


if __name__ == "__main__":

    bt = connect()

    while True:
        time.sleep(1)
        output_colors = get_colors()
        display_colors(output_colors)
