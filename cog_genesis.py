import cog
from pathlib import Path
import torch
import clifter_pixel
import yaml
import pathlib
import os
import yaml

from cogrun import create_temporary_copy


class GensisPredictor(cog.predictor):
    def setup(self):
        print("---> GenesisPredictor setup")

    @cog.input("title", type=str, default="")
    @cog.input("quality", type=str, options=["draft", "mintable"], default="draft")
    @cog.input("optional_settings", type=str, default="\n")
    def predict(self, title, quality, optional_settings):
        print("---> clifter_pixel genesis init")

        clifter_pixel.reset_settings()
        if quality == "draft":
            clifter_pixel.add_settings(
                output="output/genesis_draft.png",
                quality="draft",
                ty="draft",
                scale=2.5,
                iterations=100,
            )
        else:
            clifter_pixel.add_settings(
                output="outputs/genesis.png", quality="best", scale=4, iterations=350
            )

        title = title.strip()
        if title in ["", "(untitled)"]:
            title = "wow, that looks amazing"
            clifter_pixel.add_settings(custom_loss="saturation")

        clifter_pixel.add_settings(prompts=title)

        optional_settings = optional_settings.strip()
        if optional_settings != "":
            ydict = yaml.safe_load(optional_settings)
            if ydict is not None:
                print(ydict)
                if ("drawer" in ydict) and ydict["drawer"] == "pixel":
                    clifter_pixel.add_settings(prompt=f"title {title} #pixelart")
                clifter_pixel.add_settings(**ydict)

        clifter_pixel.add_settings(skip=True)
        settings = clifter_pixel.apply_settings()
        clifter_pixel.do_init(settings)
        run_complete = False
        while run_complete == False:
            run_complete = clifter_pixel.do_run(settings, return_display=True)
            temp_copy = create_temporary_copy(settings.output)
            yield pathlib.path(os.path.realpath(temp_copy))
