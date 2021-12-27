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
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError("boolean value expected")


# canonical interpolaction function
def map_number(n, start1, stop1, start2, stop2):
    return ((n - start1) / (stop - start1)) * (stop2 - start2) + start2

def parse_triple_to_rgb(s):
    s2 = re.sub(r'[(\[\])]', '', s)
    t = s2.split("+")
    rgb = [float(n) for n in t]
    if s[0] == "(":
        rgb = [n / 255.0 for n in rgb]
    return rgb
