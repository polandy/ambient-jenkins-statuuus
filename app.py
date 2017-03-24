import time
import config
from jenkins_adapter import get_section_state_dict
from blinky_adapter import BlinkyAdapter


def get_colors():
    colors = [[0, 0, 0]] * config.led_count

    for section, state in get_section_state_dict().iteritems():
        color = config.color_mapping[state]
        for i in range(section.range_start, section.range_end+1):
            colors[i] = color

    return colors


if __name__ == "__main__":
    blinky = BlinkyAdapter()
    while True:
        time.sleep(1)
        output_colors = get_colors()
        blinky.fade_to_colors(output_colors)
