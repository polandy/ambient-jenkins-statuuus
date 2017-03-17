import time
import config
from blinky_adapter import BlinkyAdapter


def get_colors():
    output_colors = [[0, 0, 0]] * config.led_count

    for section in config.sections:

        state = section.get_state()
        color = config.color_mapping[state]

        for i in range(section.range_start, section.range_end+1):
            output_colors[i] = color

    return output_colors


if __name__ == "__main__":

    blinky = BlinkyAdapter()

    while True:
        time.sleep(1)
        output_colors = get_colors()
        blinky.display_colors(output_colors)
