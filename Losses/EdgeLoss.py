import torch
from torch import nn, optim

from util import get_single_rgb
from PIL import Image
from util import *
from urllib.request import urlopen
import torchvision.transforms.functional as TF

from Losses.LossInterface import LossInterface


class EdgeLoss(LossInterface):
    def __init__(self, **kwargs):
        self.image = None
        self.resize = None
        self.resized_mask = None
        super().__init__(**kwargs)

    @staticmethod
    def add_settings(parser):
        parser.add_argument("--edge_thickness", type=int, help="thickness of the edge area all the way around (percent)", default=5, dest='edge_thickness')
        parser.add_argument("--edge_margins", nargs=4, type=int, help="this is for the thickness of each edge (left, right, up, down) 0-pixel size", default=None, dest='edge_margins')
        parser.add_argument("--edge_color", type=str, help="this is the color of the specified region", default="white", dest='edge_color')
        parser.add_argument("--edge_color_weight", type=float, help="how much edge color is enforced", default=0.1, dest='edge_color_weight')
        parser.add_argument("--global_color_weight", type=float, help="how much global color is enforced ", default=0.05, dest='global_color_weight')
        parser.add_argument("--edge_input_image", type=str, help="TBD", default="", dest='edge_input_image')
        parser.add_argument("--edge_mask_image", type=str, help="TBD", default="", dest='edge_mask_image')
        
        return parser

    def parse_settings(self, args):
        if type(args.edge_color) == str:
            args.edge_color = get_single_rgb(args.edge_color)
        if args.edge_margins is None:
            t = args.edge_thickness
            args.edge_margins = (t, t, t, t)
        if args.edge_input_image:
            filelist = None
            if "http" in args.edge_input_image:
                self.image = [Image.open(urlopen(args.edge_input_image))]
            else:
                filelist = real_glob(args.edge_mask_image)
                self.mask = [Image.open(f) for f in filelist]
            self.mask = self.mask[0].convert("L")
        if args.edge_mask_image:
            filelist = None
            if "http" in args.edge_mask_image:
                self.mask = {Image.open(urlopen(args.edge_mask_image))}
            else:
                filelist = real_glob(args.edge_mask_image)
                self.mask = [Image.open(f) for f in filelist]
            self.mask = self.mask[0].convert("L")
        else:
            self.mask = None

        return args
