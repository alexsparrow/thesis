from SCons.Script import *

def extension(fname, ext):
    return ".".join(fname.split(".")[:-1])+ext

class LatexBuilder(object):
    def __init__(self, env, cfg):
        self.project = cfg.LATEX_PROJECT
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
        self.dvi = self.env.DVI(source = "%s.tex" % self.project,
                           target = "%s.dvi" % self.project)
        self.pdf = self.env.PDF(source = "%s.tex" % self.project,
                           target = "%s.pdf" % self.project)
        self.ps = self.env.PostScript(source = "%s.tex" % self.project,
                                 target = "%s.ps" % self.project)
        self.wc = self.env.WordCount(source = "%s.tex" % self.project,
                                     target = "%s.count.html" % self.project)
        self.env.Alias("dvi", "%s.dvi" % self.project)
        Clean(self.dvi, self.makeindex_files)
        self.env.Alias("pdf", "%s.pdf" % self.project)
        Clean(self.pdf, self.makeindex_files)
        self.env.Alias("ps", "%s.ps" % self.project)
        Clean(self.ps, self.makeindex_files)
        self.env.Alias("wc", "%s.count.html" % self.project)
        Clean(self.wc, "%s.count.html" % self.project)
        self.env.Default(self.default_target)

    def figures(self):
        fig_exts = dict([(ext, []) for ext in self.extensions.keys()])
        for d in self._get_figure_dirs():
            for ext in self.extensions.keys():
                glob = "%s/*.%s" % (d, ext)
                fig_exts[ext].extend(Glob(glob, strings=True))
        for ext, figs in fig_exts.iteritems():
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
        self.env.Eps2pdf(pdf_file, f)
        self.env.Depends(self.pdf, pdf_file)
        self.env.Depends(self.dvi, eps_file)
    def _get_figure_dirs(self):
          raise ValueError("Must override _get_figures")
