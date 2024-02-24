from enum import Enum
import sys

from PIL import Image


class GenerationMethod(Enum):
    Brightness = 0
    Sum = 1
    Multiply = 2

class Config:
    path: str
    w: int
    h: int
    save: bool = True
    print: bool = False
    method: GenerationMethod = GenerationMethod.Brightness


def run(cfg: Config):
    pixels = list()
    with Image.open(cfg.path) as img:
        w = cfg.w
        h = cfg.h
        img = img.resize((w, h))
        pixels = list(img.getdata())

    generate = generation_method(cfg.method)
    ascii = ""
    for y in range(h):
        for x in range(w):
            value = generate(pixels[y*w + x])
            if value > 0.99:
                ascii += "#"
            elif value > 0.88:
                ascii += "%"
            elif value > 0.77:
                ascii += "X"
            elif value > 0.66:
                ascii += "="
            elif value > 0.55:
                ascii += "+"
            elif value > 0.44:
                ascii += "-"
            elif value > 0.33:
                ascii += ","
            elif value > 0.22:
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

def generation_method(method: GenerationMethod):
    def colors(pixel):
        r = pixel[0] / 255.0
        g = pixel[1] / 255.0
        b = pixel[2] / 255.0

        return r, g, b

    def brightness(pixel):
        r, g, b = colors(pixel)
        return r*0.299 + g*0.587 + b*0.114

    def sum(pixel):
        r, g, b = colors(pixel)
        return (r + b + g) / 3.0

    def multiply(pixel):
        r, g, b = colors(pixel)
        return r * g * b

    match method:
        case GenerationMethod.Brightness:
            return brightness
        case GenerationMethod.Sum:
            return sum
        case GenerationMethod.Multiply:
            return multiply


if __name__ == "__main__":
    cfg = Config()

    args = sys.argv
    args.pop(0)

    if len(args) == 0:
        print("No filepath specified")
        print("Try '--help' for more information")
        sys.exit(1)

    opts = list()
    i = 0
    while i < len(args):
        arg = args[i]
        if arg[0] == "-":
            if arg[1] != "-" and len(arg) > 2:
                for c in arg[1:]:
                    opts.append("-" + c)
            else:
                opts.append(args[i])
            args.pop(i)
        else:
            i += 1

    if "-h" in opts or "--help" in opts:
        print("Generates ascii from a picture")
        print("Usage: [OPTIONS] [FILEPATH]")
        print("   or: [OPTIONS] [FILEPATH] [SCALE]")
        print("   or: [OPTIONS] [FILEPATH] [WIDTH] [HEIGHT]")
        print()
        print("FILEPATH:   filepath to a picture")
        print("SCALE:      a scale to change the amount of pixels by")
        print("WIDTH:      an amount of pixels to set the width to")
        print("HEIGHT:     an amount of pixels to set the height to")
        print()
        print("OPTIONS:")
        print()
        print("    -b      uses percieved brightnes for generating ascii  (default)")
        print("    -m      uses pixel multiplication for genrating ascii")
        print("    -s      uses pixel sum for generating ascii")
        print()
        print("    -p      prints the ascii")
        print("    -w      saves the ascii to a text file")
        print()
        print("    -h --help   displays this help and exits")
        print()
        sys.exit(0)

    if "-m" in opts:
        cfg.method = GenerationMethod.Multiply
    if "-s" in opts:
        cfg.method = GenerationMethod.Sum
    if "-b" in opts:
        cfg.method = GenerationMethod.Brightness

    if "-p" in opts:
        cfg.save = False
        cfg.print = True
    if "-w" in opts:
        cfg.save = True

    if len(args) > 0:
        cfg.path = args[0]
    if len(args) == 1:
        args.append("0.1")
    if len(args) == 2:
        try:
            scale = float(args[1])
        except:
            print(f"SCALE '{args[1]}' is not a float")
            sys.exit(1)
        else:
            with Image.open(cfg.path) as img:
                w, h = img.size;
                cfg.w = int(w * scale)
                cfg.h = int(h * scale / 2.3)
    elif len(args) == 3:
        try:
            cfg.w = int(args[1])
        except:
            print(f"WIDTH '{args[1]}' is not an int")
            sys.exit(1)
        try:
            cfg.h = int(args[2])
        except:
            print(f"HEIGHT '{args[2]}' is not an int")
            sys.exit(1)
    else:
        print("Too many arguments where provided")
        sys.exit(1)

    run(cfg)
