import argparse


class LossInterface:
    def __init__(self, device=None):
        self.device = device

    def instance_settings(self, arglist):
        pass

    @staticmethod
    def add_settings(parser):
        return parser

    def help(self):
        parser = argparse.ArgumentParser()
        parser = self.add_setting(parser)
        helpstring = ""
        for d in parser._actions:
            helpstring = """parmeter name: {d.dest}\nHelp: {d.help}\nUse case: pixray.add_argument({d.dest}={d.default})"""

        return helpstring

    def parse_setting(self, args):
        return args

    def add_globals(self, args):
        lossglobals = {}
        return lossglobals

    def get_loss(self, cur_cutouts, out, args, globals=None, lossGlobals=None):
        loss = None
        return loss
