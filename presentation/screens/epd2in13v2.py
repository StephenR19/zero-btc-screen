import os

from PIL import Image, ImageDraw, ImageFont
try:
    from waveshare_epd import epd2in13_V2
except ImportError:
    pass
from data.plot import Plot
from presentation.observer import Observer

SCREEN_HEIGHT = 122
SCREEN_WIDTH = 250

FONT_SMALL = ImageFont.truetype(
    os.path.join(os.path.dirname(__file__), os.pardir, 'Roses.ttf'), 8)
FONT_LARGE = ImageFont.truetype(
    os.path.join(os.path.dirname(__file__), os.pardir, 'PixelSplitter-Bold.ttf'), 26)

class Epd2in13v2(Observer):

    def __init__(self, observable, mode):
        super().__init__(observable=observable)
        self.epd = self._init_display()
        self.screen_image = Image.new('1', (SCREEN_WIDTH, SCREEN_HEIGHT), 255)
        self.screen_draw = ImageDraw.Draw(self.screen_image)
        self.mode = mode

    @staticmethod
    def _init_display():
        epd = epd2in13_V2.EPD()
        epd.init(epd.FULL_UPDATE)
        epd.Clear(0xFF)
        epd.init(epd.PART_UPDATE)
        return epd

    def form_image(self, coin, prices, screen_draw):
        screen_draw.rectangle((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), fill="#ffffff")
        screen_draw = self.screen_draw
        if self.mode == "candle":
            Plot.candle(prices, size=(SCREEN_WIDTH - 45, 93), position=(41, 0), draw=screen_draw)
        else:
            last_prices = [x[3] for x in prices]
            Plot.line(last_prices, size=(SCREEN_WIDTH - 42, 93), position=(42, 0), draw=screen_draw)

        flatten_prices = [item for sublist in prices for item in sublist]
        Plot.y_axis_labels(flatten_prices, FONT_SMALL, (0, 0), (38, 89), draw=screen_draw)
        screen_draw.line([(10, 98), (240, 98)])
        screen_draw.line([(39, 4), (39, 94)])
        screen_draw.line([(60, 102), (60, 119)])
        Plot.caption(coin, flatten_prices[len(flatten_prices) - 1], 95, SCREEN_WIDTH, FONT_LARGE, screen_draw)

    def update(self, coin, data):
        self.form_image(coin, data, self.screen_draw)
        screen_image_rotated = self.screen_image.rotate(180)
        # TODO: add a way to switch bewen partial and full update
        # epd.presentation(epd.getbuffer(screen_image_rotated))
        self.epd.displayPartial(self.epd.getbuffer(screen_image_rotated))

    def close(self):
        epd2in13_V2.epdconfig.module_exit()
