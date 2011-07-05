"""
This is the place that takes the basic configuration of your LaTeX
build project.
"""

# The name of our main LaTeX source, e. g. 'thesis' or a file 'thesis.tex'.
LATEX_PROJECT = 'thesis'

# Default target.
DEFAULT_TARGET = 'pdf'

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
    "1-theory",
    "2-expt",
    "3-wpol",
    "4-susy",
    "5-interpretations"
    ]


MAKEINDEX_EXTENSIONS = ['.glg', '.glo', '.gls']

