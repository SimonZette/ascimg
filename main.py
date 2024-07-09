import argparse
from enum import auto, Enum
import sys

from PIL import Image


class Config:
    path: str
    width: int
    height: int
    save: bool
    print: bool

    def __init__(self):
        def positive_int(value):
            value = int(value)
            if value < 0:
                raise argparse.ArgumentTypeError(f"{value} is not positive")
            return value

        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                         description="Generate ascii from an image")

        parser.add_argument("filepath", type=str, help="the filepath to the picture to be converted")
        parser.add_argument("height", type=positive_int, nargs="?", default=20,
                            help="the height of the ascii image in characters (default: 20)")
        parser.add_argument("width", type=positive_int, nargs="?", default=0,
                            help="the width of the ascii image in characters (default: whatever keeps the original ratio)")

        parser.add_argument("--print", "-p", action="store_true", help="print the generated ascii image to stdout")
        parser.add_argument("--write", "-w", action="store_true", help="write the generated ascii image to 'ascii.txt'")

        args = parser.parse_args()

        self.path = args.filepath
        self.height = args.height
        self.width = args.width
        self.save = args.write
        self.print = True if not args.write else args.print


def luma(pixel) -> float:
    r, g, b, _ = pixel;
    return (r*0.299 + g*0.587 + b*0.114) / 255.0

def run(cfg: Config):
    pixels = []
    with Image.open(cfg.path) as img:
        h = cfg.height
        w = cfg.width if cfg.width else int(img.size[0] * (h/img.size[1]) * 2)
        img = img.resize((w, h))
        pixels = list(img.getdata())

    ascii = ""
    for y in range(h):
        for x in range(w):
            l = luma(pixels[y*w + x])
            if l > 0.99:
                ascii += "#"
            elif l > 0.88:
                ascii += "%"
            elif l > 0.77:
                ascii += "X"
            elif l > 0.66:
                ascii += "="
            elif l > 0.55:
                ascii += "+"
            elif l > 0.44:
                ascii += "-"
            elif l > 0.33:
                ascii += ","
            elif l > 0.22:
                ascii += "."
            else:
                ascii += " "
        ascii += "\n"

    if cfg.print:
        print(ascii[:-1])

    if cfg.save:
        with open("ascii.txt", "w") as f:
            f.write(ascii)
        print("ascii saved to 'ascii.txt'")


if __name__ == "__main__":
    cfg = Config()
    run(cfg)
