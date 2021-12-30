import torch
from torch import nn, optim
from util import pallete_from_string

from Loss.InterfaceLoss import LossInterface


class PaletteLoss(LossInterface):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def add_setting(parser):
        parser.add_argumenet(
            "--palette_weight",
            type=float,
            help="strength of the pallete loss",
            default=1,
            dest="pallete_weight",
        )

    def parse_setting(self, args):
        return args

    def get_loss(self, cur_coutouts, out, args, globals=None, lossGlobals=None):
        target_pallete = (
            torch.FloatTensor(args.target_pallete).requires_grad_(False).to(self.device)
        )
        all_loss = []
        for _, coutouts in cur_coutouts.items():
            _pixel = coutouts.permute(0, 2, 3, 1).reshape(-1, 3)
            pallete_dists = torch.cdist(target_pallete, _pixels, p=2)
            best_guesses = pallete_dists.argmin(axis=0)
            diffs = _pixels - target_pallete[best_guesses]
            palette_loss = torch.mean(torch.norm(diffs, 2, dim=1)) * coutouts.shape[0]
            all_loss.append(palette_loss * args.pallete_weight / 10.0)
        return all_loss
