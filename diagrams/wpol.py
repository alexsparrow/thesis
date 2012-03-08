#! /usr/bin/env python2

from pyfeyn.user import *
from pyx.text import preamble
import pyx

preamble(r"\usepackage{hepnicenames}")

processOptions()

def mk2to2(fname, channel, helicities, a, b, c, d, i):
    fd = FeynDiagram()
    momenta = (+1, +1, +1)
    if channel == "s":
        coords = {"a": (-4, 2), "b": (-4, -2), "c": (4,2), "d": (4,-2), "v1": (-2, 0), "v2":(2,0)}
    else:
        coords = {"a": (-2, 3), "b": (-2, -3), "c": (2,3), "d": (2,-3), "v1": (0, 2), "v2":(0,-2)}
    in1 = DecoratedPoint(*coords["a"]).addLabel(a[1])
    in2 = DecoratedPoint(*coords["b"]).addLabel(b[1])
    out1 = DecoratedPoint(*coords["c"]).addLabel(c[1])
    out2 = DecoratedPoint(*coords["d"]).addLabel(d[1])
    v1 = Vertex(*coords["v1"])
    v2 = Vertex(*coords["v2"])
    pa = a[0](in1, v1)
    pb = b[0](in2, v1 if channel == "s" else v2)
    pc = c[0](v2 if channel=="s" else v1, out1)
    pd = d[0](v2, out2)
    internal = i[0](v1, v2)

    # helicity labels
    pc.addParallelArrow(sense = helicities[0], displace = 0.6)
    pc.labels[-1].setCustomStyles([color.rgb.red])
    pd.addParallelArrow(sense = helicities[1], displace = 0.6)
    pd.labels[-1].setCustomStyles([color.rgb.red])

    for l, p in zip([pa, pb, pc, pd, internal], [a,b,c,d,i]):
        if p[0] == Fermion: l.addArrow()
        l.addParallelArrow()
    fd.draw(fname)

def mkwpol(fname, pin1, pin2, pout1, out_momenta_type, helicities=(1,1,1,1,1,1)):
    def helicity(h):
        return h/(abs(h))
    def angle(h):
        return -helicity(h)*(1-abs(h))*90.0
    """ out_momenta_type : 0 -> e+ left, nu right, colinear
                           1 -> e+ left, nu right, neutrino big
                           2 -> e+ left, nu right, neutrino small
                           3 -> nu left, e+ right, neutrino small
                           """
    print "Making wpol: %s" % fname
    fd = FeynDiagram()

    in1 = DecoratedPoint(-1.5, 0).addLabel(pin1[1], displace = -0.3)
    in2 = DecoratedPoint(1.5, 0).addLabel(pin2[1])
    outargs = {}
    if pout1[0] == Gluon: outargs["displace"] = 0.5
    out1 = DecoratedPoint(0, -1.5).addLabel(pout1[1], **outargs)
    out_coords = {0: ((-0.3, 2), (0.1, 3.5)),
                  1: ((-0.5, 2), (1, 3.5)),
                  2: ((-1, 3.5), (0.5, 2)),
                  3: ((0.1, 3.5), (-0.3, 2))
                  }[out_momenta_type]

    out2 = DecoratedPoint(*out_coords[0]).addLabel(r"\Ppositron", displace=-0.3)
    neutargs = {}
    if out_momenta_type == 3: neutargs["displace"] = -0.3
    out3 = DecoratedPoint(*out_coords[1]).addLabel(r"\Pneutrino", **neutargs)
    v1 = Vertex(0, 0)
    v2 = Vertex(0, 1.5)

    f1 = pin1[0](in1, v1)
    if pin1[0] == Fermion: f1.addArrow()
    if pin1[0] == Gluon: f1.invert()
    f2 = pout1[0](v1, out1)

    if pout1[0] == Fermion: f2.addArrow()
    f3 = Vector(v1, v2).addLabel(r"\PWplus", displace=-0.3)
    f4 = Fermion(v2, out2).addArrow()
    f5 = Fermion(v2, out3).addArrow()

    g1 = pin2[0](in2, v1)
    if pin2[0] == Fermion: g1.addArrow()

    for p, x, h in zip([pin1[0], pin2[0], pout1[0], Vector], [f1, g1, f2, f3], helicities[:4]):
        args = {"displace":0.3 if p == Vector else 0.1}
        args["sense"] = helicity(h)
        args["rotation"] = angle(h)
        if p == Vector:
            args["length"] = 0.3*pyx.unit.v_cm
            args["stems"] = 2
        x.addParallelArrow(**args)
        x.labels[-1].setCustomStyles([color.rgb.red])
    if out_momenta_type in [0,1]:
        f4.addParallelArrow(displace=-0.1, sense=helicity(helicities[4]), rotation=angle(helicities[4]),
                            size=3*pyx.unit.v_pt, length=0.25*pyx.unit.v_cm)
        f5.addParallelArrow(displace=0.1, sense=helicity(helicities[5]), rotation=angle(helicities[5]))
    else:
        f4.addParallelArrow(displace=-0.1 if out_momenta_type==2 else 0.1, sense=helicity(helicities[4]), rotation=angle(helicities[4]))
        f5.addParallelArrow(displace=0.1 if out_momenta_type==2 else -0.1, sense=helicity(helicities[5]), rotation=angle(helicities[5]),
                            size=3*pyx.unit.v_pt, length=0.25*pyx.unit.v_cm)
    for x in [f4, f5]: x.labels[-1].setCustomStyles([color.rgb.red])
    fd.draw(fname)


if __name__ == "__main__":
    particles = [(Fermion, r"\Pup"), (Gluon, r"\Pgluon"), (Vector, r"\PWp"), (Fermion, r"\Pdown"), (Fermion, "\Pdown")]
    mk2to2("wpol_1jet_s.pdf", "s", [+1, -1], *particles)
    mk2to2("wpol_1jet_t.pdf", "t", [+1, -1], *particles)

    mkwpol("wpol_prod_a.pdf", (Fermion, r"\Pup"), (Gluon, r"\Pgluon"), (Fermion, r"\Pdown"), 0,
           helicities = (-1, -1, -1, -1, +1, -1))
    mkwpol("wpol_prod_b.pdf", (Fermion, r"\Pup"), (Fermion, "\APdown"), (Gluon, r"\Pgluon"), 1,
           helicities = (-1, +1, -1, -0.5, +1, -1))
    mkwpol("wpol_prod_c.pdf", (Gluon, r"\Pgluon"), (Fermion, "\APdown"), (Fermion, r"\APup"), 1,
           helicities = (-1, +1, +1, -0.5, +1, -1))
    mkwpol("wpol_prod_d.pdf", (Fermion, r"\Pup"), (Gluon, r"\Pgluon"), (Fermion, r"\Pdown"), 2,
           helicities = (-1, +1, -1, 0.5, +1, -1))
    mkwpol("wpol_prod_e.pdf", (Fermion, r"\Pup"), (Fermion, r"\APdown"), (Gluon, r"\Pgluon"), 2,
           helicities = (-1, +1, -1, 0.5, +1, -1))
    mkwpol("wpol_prod_f.pdf", (Gluon, r"\Pgluon"), (Fermion, r"\APdown"), (Fermion, "\APup"), 3,
           helicities = (+1, +1, +1, +1, +1, -1))

#wpol1()
#wpol2()
