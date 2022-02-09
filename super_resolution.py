from DrawingInterface import DrawingInterface
import os.path
import torch
from torch.nn import functional as F
from torchvision.transforms import functional as TF
from basicr.arch.rrdbnet_arch import RRDBNet

from real_esrganer import RealERGANer
from util import wget_file

superresolution_checkpoint_table = {
    "RealESRGAN_x4plus": "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth",
}

class ReplaceGrad(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x_forward, x_backward):
        ctx.shape = x_backward.shape
        return x_forward

    @staticmethod
    def backward(ctx, grad_in):
        return None, grad_in.sum_to_size(ctx.shape)

replace_grad = ReplaceGrad.apply
