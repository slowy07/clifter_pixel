import cog
from pathlib import Path
import torch
import yaml
import pathlib
import os
import yaml
import tempfile, shutil
import clifter_pixel


def create_temporary_copy(src_path):
    _, tf_suffix = os.path.splittex(src_path)
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, f"tempfile{tf_suffix}")
    shutil.copy2(src_path, temp_path)
    return temp_path


class BasePixrayPredictor(cog.Predictor):
    def setup(self):
        print("---> base clf predictor setup")
        os.environ["TORCH_HOME"] = "models/"

    @cog.input("settings", type=str, help="default settings to use")
    @cog.input("prompts", type=str, help="text prompts")
    def predict(self, settings, **kwargs):
        print("--> base clf predictor predict")
        os.environ["TORCH_HOME"] = "models/"
        settings_file = f"cogs/{settings}.yaml"
        with open(settings_file, "r") as stream:
            try:
                base_settins = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print("yaml error ", exc)
                sys.exit(1)

        clifter_pixel.reset_settings()
        clifter_pixel.add_settings(**base_settings)
        clifter_pixel.add_settings(**kwargs)
        clifter_pixel.add_settings(skip_args=True)
        settings = clifter_pixel.apply_settings()
        run_complete = False
        while run_complete == False:
            run_complete = clifter_pixel.do_run(settings, return_display=True)
            temp_copy = create_temporary_copy(settings.output)
            yield pathlib.path(os.path.realpath(temp_copy))


class PixrayVqgan(BasePixrayPredictor):
    @cog.input("prompts", type=str, help="text prompt", default="rainbow mountain")
    @cog.input(
        "quality",
        type=str,
        help="better is slower",
        default="normal",
        options=["draft", "normal", "better", "best"],
    )
    @cog.input(
        "aspect",
        type=str,
        help="wide vs square",
        default="widescreen",
        options=["widescreen", "square"],
    )
    # @cog.input("num_cuts", type=int, default="24", min=4, max=96)
    # @cog.input("batches", type=int, default="1", min=1, max=32)
    def predict(self, **kwargs):
        yield from super().predict(settings="pixray_vqgan", **kwargs)


class PixrayPixel(BasePixrayPredictor):
    @cog.input(
        "prompts", type=str, help="text prompt", default="Beirut Skyline. #pixelart"
    )
    @cog.input(
        "aspect",
        type=str,
        help="wide vs square",
        default="widescreen",
        options=["widescreen", "square"],
    )
    @cog.input(
        "drawer",
        type=str,
        help="render engine",
        default="pixel",
        options=["pixel", "vqgan", "line_sketch", "clipdraw"],
    )
    def predict(self, **kwargs):
        yield from super().predict(settings="pixray_pixel", **kwargs)


class Text2Image(BasePixrayPredictor):
    @cog.input(
        "prompts",
        type=str,
        help="description of what to draw",
        default="Robots skydiving high above the city",
    )
    @cog.input(
        "quality",
        type=str,
        help="speed vs quality",
        default="better",
        options=["draft", "normal", "better", "best"],
    )
    @cog.input(
        "aspect",
        type=str,
        help="wide or narrow",
        default="widescreen",
        options=["widescreen", "square", "portrait"],
    )
    def predict(self, **kwargs):
        yield from super().predict(settings="text2image", **kwargs)


class Text2Pixel(BasePixrayPredictor):
    @cog.input(
        "prompts",
        type=str,
        help="text prompt",
        default="Manhattan skyline at sunset. #pixelart",
    )
    @cog.input(
        "aspect",
        type=str,
        help="wide or narrow",
        default="widescreen",
        options=["widescreen", "square", "portrait"],
    )
    @cog.input(
        "pixel_scale", type=float, help="bigger pixels", default=1.0, min=0.5, max=2.0
    )
    def predict(self, **kwargs):
        yield from super().predict(settings="text2pixel", **kwargs)


class PixrayRaw(BasePixrayPredictor):
    @cog.input(
        "prompts",
        type=str,
        help="text prompt",
        default="Manhattan skyline at sunset. #pixelart",
    )
    @cog.input("settings", type=str, help="yaml settings", default="\n")
    def predict(self, prompts, settings):
        ydict = yaml.safe_load(settings)
        if ydict == None:
            # no settings
            ydict = {}
        yield from super().predict(settings="pixrayraw", prompts=prompts, **ydict)


class PixrayApi(BasePixrayPredictor):
    @cog.input("settings", type=str, help="yaml settings", default="\n")
    def predict(self, settings):
        ydict = yaml.safe_load(settings)
        if ydict == None:
            # no settings
            ydict = {}
        yield from super().predict(settings="pixrayapi", **ydict)
