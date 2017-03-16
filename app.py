import sys
import glob
import time
import BlinkyTape
import config


def connect():
    serialPorts = glob.glob("/dev/ttyACM0")
    port = serialPorts[0]

    if not port:
        sys.exit("Could not locate a BlinkyTape.")

    print "BlinkyTape found at: %s" % port

    bt = BlinkyTape.BlinkyTape(port)
    bt.displayColor(0, 0, 0)
    return bt


if __name__ == "__main__":

    bt = connect()

    while True:
        time.sleep(1)

        for section in config.sections:

            print('updating section: ' + section.name)

            state = section.get_state()
            color = config.color_mapping[state]

            for i in range(section.range_start, section.range_end+1):
                print(i)
                bt.sendPixel(color[0], color[1], color[2])

        print('end update period')

        bt.show()
