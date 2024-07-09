import argparse

from PIL import Image


class Config:
    filepath: str
    width: int
    height: int
    write_to: str
    print: bool

    def __init__(self):
        def positive_int(value):
            value = int(value)
            if value <= 0:
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
        parser.add_argument("--write_to", "-w",  type=str, default="",
                            help="write the generated ascii image to a specified file")

        args = parser.parse_args()

        self.filepath = args.filepath
        self.height = args.height
        self.width = args.width
        self.write_to = args.write_to
        self.print = True if not args.write_to else args.print


def luma(pixel) -> float:
    r, g, b, _ = pixel;
    return (r*0.299 + g*0.587 + b*0.114) / 255.0

def run(cfg: Config):
    pixels = []
    with Image.open(cfg.filepath) as img:
        height = cfg.height
        width = cfg.width if cfg.width else int(img.size[0] * (height/img.size[1]) * 2)
        img = img.resize((width, height))
        pixels = list(img.getdata())

    ascii = ""
    for y in range(height):
        for x in range(width):
            l = luma(pixels[y*width + x])
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

    if cfg.write_to:
        with open(cfg.write_to, "w") as f:
            f.write(ascii)
        print(f"ascii saved to {cfg.write_to}")


if __name__ == "__main__":
    cfg = Config()
    run(cfg)
