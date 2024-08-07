import argparse
import sys

from PIL import Image


class Config:
    filepath: str
    width: int
    height: int
    characters: str
    write_to: str
    print: bool

    def __init__(self):
        def positive_int(value):
            value = int(value)
            if value <= 0:
                raise argparse.ArgumentTypeError(f"{value} is not positive")
            return value

        def non_empty_str(value):
            value = str(value)
            if len(value) == 0:
                raise argparse.ArgumentTypeError("The argument cannot be an empty string")
            return value

        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                         description="Generate ascii from an image")

        parser.add_argument("filepath", type=str, help="the filepath to the picture to be converted")
        parser.add_argument("height", type=positive_int, nargs="?", default=20,
                            help="the height of the ascii image in characters (default: 20)")
        parser.add_argument("width", type=positive_int, nargs="?", default=0,
                            help="the width of the ascii image in characters (default: whatever keeps the original ratio)")

        parser.add_argument("--characters", "-c", type=non_empty_str, default=" .:*oe?8#",
                            help="the characters used to represent brightness, from darkest to lightest (defaut: ' .:*oe?8#')")

        parser.add_argument("--print", "-p", action="store_true", help="print the generated ascii image to stdout")
        parser.add_argument("--write_to", "-w",  type=str, default="",
                            help="write the generated ascii image to a specified file")

        args = parser.parse_args()

        self.filepath = args.filepath
        self.width = args.width
        self.height = args.height
        self.characters = args.characters
        self.write_to = args.write_to
        self.print = True if not args.write_to else args.print


def luma(pixel) -> float:
    r = pixel[0]
    g = pixel[1]
    b = pixel[2]
    return (r*0.299 + g*0.587 + b*0.114) / 255.0

def run(cfg: Config):
    pixels = []

    try:
        with Image.open(cfg.filepath) as img:
            height = cfg.height
            width = cfg.width if cfg.width else int(img.size[0] * (height/img.size[1]) * 2)
            img = img.resize((width, height))
            pixels = list(img.getdata())
    except FileNotFoundError:
        print(f"Failed to find the file '{cfg.filepath}'")
        sys.exit(1)

    ascii = ""
    for y in range(height):
        for x in range(width):
            l = luma(pixels[y*width + x])
            ascii += cfg.characters[int(l * (len(cfg.characters)-1))]
        ascii += "\n"

    if cfg.print:
        print(ascii[:-1])

    if cfg.write_to:
        with open(cfg.write_to, "w") as f:
            f.write(ascii)
        print(f"ascii saved to {cfg.write_to}")


if __name__ == "__main__":
    cfg = Config()
    run(cfg)
