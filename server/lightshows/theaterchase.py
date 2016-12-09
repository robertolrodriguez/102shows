"""
Theater Chase
(c) 2015 Martin Erzberger, 2016 Simon Leiner
"""

from lightshows.templates.colorcycle import *
from lightshows.utilities.general import wheel


class TheaterChase(ColorCycle):
    """
    Theater Chase: https://www.youtube.com/watch?v=rzDw4Yu_S6U

    No parameters necessary
    """
    def init_parameters(self):
        super().init_parameters()
        self.num_steps_per_cycle = 35

    def before_start(self):
        pass

    def update(self, current_step: int, current_cycle) -> bool:
        # One cycle = One trip through the color wheel, 0..254
        # Few cycles = quick transition, lots of cycles = slow transition
        # Note: For a smooth transition between cycles, numStepsPerCycle must be a multiple of 7
        start_index = current_step % 7  # Each segment is 7 dots long: 2 blank, and 5 filled
        color_index = wheel(int(round(255 / self.num_steps_per_cycle * current_step, 0)))
        for pixel in range(self.strip.num_leds):
            # Two LEDs out of 7 are blank. At each step, the blank ones move one pixel ahead.
            if ((pixel + start_index) % 7 == 0) or ((pixel + start_index) % 7 == 1):
                self.strip.set_pixel(pixel, 0, 0, 0)
            else:
                self.strip.set_pixel(pixel, *color_index)
        return 1
