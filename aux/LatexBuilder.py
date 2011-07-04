from SCons.Script import *

def extension(fname, ext):
    return ".".join(fname.split(".")[:-1])+ext

class LatexBuilder(object):
    def __init__(self, env, cfg):
        self.project = cfg.LATEX_PROJECT
        self.dvi = env.DVI(source = "%s.tex" % self.project,
                           target = "%s.dvi" % self.project)
        self.pdf = env.PDF(source = "%s.tex" % self.project,
                           target = "%s.pdf" % self.project)
        self.ps = env.PostScript(source = "%s.tex" % self.project,
                                 target = "%s.ps" % self.project)
        self.makeindex_files = ["%s.%s" % (self.project, ext)
                                for ext in cfg.MAKEINDEX_EXTENSIONS]
        self.default_target = cfg.DEFAULT_TARGET
        self.extensions = cfg.FILE_EXTENSIONS
        self.generated = cfg.GENERATED_DIRECTORY
        self.convertors = {
            "png" : self._png,
            "eps" : self._eps,
            "pdf" : self._pdf,
            "jpg" : self._jpg
            }
        self.env = env

    def aliases(self):
        self.env.Alias("dvi", "%s.dvi" % self.project)
        Clean(self.dvi, self.makeindex_files)
        self.env.Alias("pdf", "%s.pdf" % self.project)
        Clean(self.pdf, self.makeindex_files)
        self.env.Alias("ps", "%s.ps" % self.project)
        Clean(self.ps, self.makeindex_files)
        self.env.Default(self.default_target)

    def figures(self):
        figures = {}
        for d in self._get_figure_dirs():
            for ext in self.extensions.keys():
                glob = "%s/*.%s" % (d, ext)
                figures[ext] = Glob(glob, strings=True)
        for ext, figs in figures.iteritems():
            if ext in self.convertors:
                for f in figs:
                    self.convertors[ext](f)

    def _png(self, f):
        png_file = self._get_generated_path(f)
        eps_file = extension(png_file, ".eps")
        self.env.Command(png_file, f,
                         Copy('$TARGET', '$SOURCE'))
        self.env.Png2eps(eps_file, f)
        self.env.Depends(self.dvi, eps_file)
        self.env.Depends(self.pdf, png_file)
    def _jpg(self, f):
        jpg_file = self._get_generated_path(f)
        eps_file = extension(jpg_file, ".eps")
        self.env.Command(jpg_file, f,
                         Copy('$TARGET', '$SOURCE'))
        self.env.Jpg2eps(eps_file, f)
        self.env.Depends(self.dvi, eps_file)
        self.env.Depends(self.pdf, jpg_file)
    def _pdf(self, f):
        pdf_file = self._get_generated_path(f)
        eps_file = extension(pdf_file, ".eps")
        self.env.Command(pdf_file, f,
                         Copy('$TARGET', '$SOURCE'))
        self.env.Pdf2eps(eps_file, f)
        self.env.Depends(self.dvi, eps_file)
        self.env.Depends(self.pdf, pdf_file)
    def _eps(self, f):
        eps_file = self._get_generated_path(f)
        pdf_file = extension(eps_file, ".pdf")
        self.env.Command(eps_file, f,
                         Copy('$TARGET', '$SOURCE'))
        self.env.Eps2Pdf(pdf_file, f)
        self.env.Depends(self.pdf, pdf_file)
        self.env.Depends(self.dvi, eps_file)
    def _get_figure_dirs(self):
          raise ValueError("Must override _get_figures")

