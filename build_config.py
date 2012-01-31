"""
This is the place that takes the basic configuration of your LaTeX
build project.
"""

# The name of our main LaTeX source, e. g. 'thesis' or a file 'thesis.tex'.
LATEX_PROJECT = 'thesis'

# Default target.
DEFAULT_TARGET = 'dvi'

# --- Things below should mostly not need touching. ---
# Some rather fixed configurations.

IMAGES_DIRECTORY = 'images'
GENERATED_DIRECTORY = 'generated'

FILE_EXTENSIONS = {'eps': '.eps',
                   'pdf': '.pdf',
                   'png': '.png',
                   'jpg': '.jpg',
                   'gnuplot': '.gnuplot'}

CHAPTERS = [
    "1-sm",
    "2-susy",
    "3-framework",
    "4-expt",
    "5-reco",
    "6-wpol",
    "7-susysearch",
    "8-interpretation",
    "appendices"
    ]


MAKEINDEX_EXTENSIONS = ['.glg', '.glo', '.gls']

MAKE_STATUS_PAGE = True
