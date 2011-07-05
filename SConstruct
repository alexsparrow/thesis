"""
The master build SConstruct file. This pulls in everything else and makes
things happen.
"""

import os, os.path
import sys
import build_config
from aux.LatexBuilder import LatexBuilder

# Make a new environment.
env = Environment()

# Get all the nested SConscripts in that may alter and pass back
# the environment.
env = SConscript('aux/SConscript', 'env')

class ThesisBuilder(LatexBuilder):
      def __init__(self, env, cfg, chapters):
            self.chapters = chapters
            super(ThesisBuilder, self).__init__(env, cfg)


      def _get_figure_dirs(self):
            return ["%s/figures" % ch for ch in self.chapters]

      def _get_generated_path(self, path):
            return os.path.normpath("%s/../fig/%s" % (os.path.dirname(path),
                                                      os.path.basename(path)))

def main():
    env["LATEXRETRIES"] = 4
    builder = ThesisBuilder(env,
                            build_config,
                            build_config.CHAPTERS)
    builder.figures()
    builder.aliases()


main()

