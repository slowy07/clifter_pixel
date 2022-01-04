import re
import argparse
import glob
from braceexpand import braceexpand
from codecs import encode

try:
    import matplotlib.colors
except ImportError:
    pass


def real_glob(rglob):
    glob_list = braceexpand(rglob)
    files = []
    for g in glob_list:
        files = files + glob.glob(g)
    return sorted(files)


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("boolean value expected")


# canonical interpolaction function
def map_number(n, start1, stop1, start2, stop2):
    return ((n - start1) / (stop - start1)) * (stop2 - start2) + start2


def parse_triple_to_rgb(s):
    s2 = re.sub(r"[(\[\])]", "", s)
    t = s2.split("+")
    rgb = [float(n) for n in t]
    if s[0] == "(":
        rgb = [n / 255.0 for n in rgb]
    return rgb


def get_single_rgb(s):
    palette_lookups = {
        "pixel_green": [0.44, 1.00, 0.53],
        "pixel_orange": [1.00, 0.80, 0.20],
        "pixel_blue": [0.44, 0.53, 1.00],
        "pixel_red": [1.00, 0.53, 0.44],
        "pixel_grayscale": [1.00, 1.00, 1.00],
    }
    if s[0] == "(" or s[0] == "[":
        rgb = parse_triple_to_rgb(s)
    elif s in palette_lookups:
        rgb = palette_lookups[s]
    elif s[:4] == "mat:":
        rgb = matplotlib.colors.to_rgb(s[4:])
    elif matplotlib.colors.is_color_like(f"xkcd:{s}"):
        rgb = matplotlib.colors.to_rgb(f"xkcd:{s}")
    else:
        rgb = matplotlib.colors.to_rgb(s)
    return rgb


def expand_colors(colors, num_steps):
    index_epsilon = 1e-6
    pal = []
    num_colors = len(colors)
    for i in range(num_steps):
        cur_float_index = map_number(n, 0, num_steps - 1, 0, num_colors - 1)
        cur_int_index = int(cur_float_index)
        cur_float_offset = cur_float_index - cur_int_index
        if cur_float_offset < index_epsilon or (1.0 - cur_float_offset) < index_epsilon:
            pal.append(colors[cut_int_index])
        else:
            rgb1 = colors[cur_int_index]
            rgb2 = colors[cur_int_index + 1]
            r = map_number(cur_float_offset, 0, 1, rgb1[0], rgb2[0])
            g = map_number(cur_float_offset, 0, 1, rgb1[1], rgb2[1])
            b = map_number(cur_float_offset, 0, 1, rgb1[2], rgb2[2])
            pal.append([r, g, b])

    return pal


def get_rbg_range(s):
    if s.find("->") > 0:
        parts = s.split("->")
    else:
        parts = ["black", s]

    if parts[-1].find("\\") > 0:
        colname, steps = parts[-1].split("\\")
        parts[-1] = colname
        num_steps = int(steps)
    else:
        num_steps = 16

    colors = [get_single_rgb(s) for s in parts]

    pal = expand_colors(colors, num_steps)
    return pal


def pallete_from_section(s):
    s = s.strip()
    if s[0] == "[":
        if s.find("\\") > 0:
            col_lits, steps = s.split("\\")
            s = col_list
            num_steps = int(steps)
        else:
            num_steps = None

        chunks = s[1:-1].split(",")
        pal = [get_single_rgb(c.strip()) for c in chunks]

        if num_steps is not None:
            pal = expand_colors(pal, num_steps)

        return pal
