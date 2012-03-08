from pyfeyn.user import *
from pyx.text import preamble
import pyx

preamble(r"\usepackage{hepnicenames}")

def susy_1lepton(fname):
    fd = FeynDiagram()
    p1 = Point(-4, 2)
    p2 = Point(-4, -2)

    int_x = -2
    v1 = Vertex(int_x, 0.3)
    v2 = Vertex(int_x, -0.3)
    ml1 = MultiLine(p1, v1, 3)
    ml2 = MultiLine(p2, v2, 3)
    in_blob = Ellipse(x=int_x, y=0,  xradius=0.5,# fill=[GREY],
                      yradius=1.5, points=[v1,v2]).setFillStyle(HATCHED45)

    int_two_x = 0
    v3 = Vertex(int_two_x, 2)
    v4 = Vertex(int_two_x, -2)

    g1 = Gluino(v1, v3).addLabel(r"\PSgluino")
    g2 = Gluino(v2, v4).addLabel(r"\PSgluino")


    int_three_x = 2
    p_quark1 = Point(int_three_x, 3)
    v_squark1 = Vertex(int_three_x, 1)

    quark1 = Fermion(v3, p_quark1).addLabel(r"\Pquark")
    squark1 = Sfermion(v3, v_squark1).addLabel(r"\Psquark")

    int_four_x = 4
    p_quark2 = Point(int_four_x, 2)
    v_chargino1 = Vertex(int_four_x, 0)

    quark2 = Fermion(v_squark1, p_quark2).addLabel(r"\Pquark")
    chargino1 = Gaugino(v_squark1, v_chargino1).addLabel(r"\PScharginopm")

    int_five_x = 5
    int_six_x = 6
    v_w1 = Vertex(int_five_x, 1)
    p_lsp1 = Point(int_six_x, -1)

    w1 = Vector(v_chargino1, v_w1).addLabel(r"\PW")
    lsp1 = Gaugino(v_chargino1, p_lsp1).addLabel(r"\PSneutralinoOne")


    p_lepton1 = Point(int_six_x, 1.5)
    p_neutrino1 = Point(int_six_x, 0.5)

    lepton1 = Fermion(v_w1, p_lepton1).addLabel(r"\Pleptonpm")
    lsp1 = Fermion(v_w1, p_neutrino1).addLabel(r"\Pneutrino", displace=0.25)

    # here we go again
    int_three_x = 2
    p_quark3 = Point(int_three_x, -1)
    v_squark2 = Vertex(int_three_x, -3)

    quark3 = Fermion(v4, p_quark3).addLabel(r"\Pquark")
    squark2 = Sfermion(v4, v_squark2).addLabel(r"\Psquark")

    int_four_x = 4
    p_quark4 = Point(int_four_x, -2)
    p_lsp2 = Point(int_four_x, -4)

    quark4 = Fermion(v_squark2, p_quark4).addLabel(r"\Pquark")
    lsp2 = Gaugino(v_squark2, p_lsp2).addLabel(r"\PSneutralinoOne")

    fd.draw(fname)


if __name__ == "__main__":
    susy_1lepton("susy_1lep.eps")
