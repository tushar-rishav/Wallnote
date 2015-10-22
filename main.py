# -*- coding: utf-8 -*-

from collections import OrderedDict
from Config import Config
from setproctitle import setproctitle
import keylogger
import pickle
import os
import cairo
import pango
import pangocairo
import sys

__version__ = "0.0.1"


class Wallnote(Config):

    def __init__(self):
        self.data = OrderedDict()
        self.flag = False
        self.ignore_keys = ["<left ctrl>","<left shift>","<right shift>","<backspace>","<esc>","<enter>","<caps lock>","<right ctrl>"]
        setproctitle('Wallnote')

        # load saved data
        load_data = self.load_pickle()
        if load_data:
            self.data = load_data
        # know where to add new data
        if load_data and len(load_data):
            self.ins_pos = len(self.data)
        else:
            self.ins_pos = 0
        # start recording
        keylogger.log(self.read_keys)

    def check_escape(self, key):
        """
                Check if user wants is done taking notes
        """
        if self.flag and key == "`":
            self.set_pickle(self.data)
        self.flag = False

        if(key == "<esc>"):
            self.flag = True

    def insert_data(self, key):
        """
                Build the present data using recorded key
        """
        if self.ins_pos in self.data:
            if key == "<enter>":
                self.data[self.ins_pos] += "\n"
            elif key and key not in self.ignore_keys:
                self.data[self.ins_pos] += key
        else:
            self.data[self.ins_pos] = key

    def read_keys(self, key):
        """
                Record key
        """
        self.check_escape(key)
        if not self.flag:
            self.insert_data(key)
            self.dict_to_text(self.data)

    def dict_to_text(self, data):
        """
                Convert the pickle data into text file
        """
        temp_data = ""
        for lineno, line in data.iteritems():
            temp_data += "{}. {}\n".format(lineno, line)
        self.draw_image(temp_data)

    def draw_image(self, temp_data):
        """
                Draw image file from text file
        """

        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1220, 620)
        context = cairo.Context(surf)
        context.rectangle(0, 0, 1220, 620)  # draw a background rectangle:
        context.set_source_rgb(1, 1, 1)
        context.fill()
        font_map = pangocairo.cairo_font_map_get_default()
        families = font_map.list_families()
        context.translate(150, 55)
        pangocairo_context = pangocairo.CairoContext(context)
        pangocairo_context.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
        layout = pangocairo_context.create_layout()
        fontname = sys.argv[1] if len(sys.argv) >= 2 else "Sans"
        font = pango.FontDescription(fontname + " 25")
        layout.set_font_description(font)
        layout.set_text(temp_data)
        context.set_source_rgb(0, 0, 0)
        pangocairo_context.update_layout(layout)
        pangocairo_context.show_layout(layout)

        with open("wallnote.png", "wb") as image_file:
            surf.write_to_png(image_file)
        path = os.path.join(os.getcwd(), "wallnote.png")
        os.popen(
            "gsettings set org.gnome.desktop.background picture-uri file:///{}".format(path))


def main():
    note = Wallnote()

if __name__ == "__main__":
    main()
