'''
Collection of functions used to generate
randomized geometry colour
cleaning geometry
'''

import random
import maya.cmds as mc



def getrandom_id():
    random.seed()
    id = random.randrange(999999999999)
    return id


def random_color(id):
    random.seed(id+6843651)
    r = random.random()
    random.seed(id+9844318)
    g = random.random()
    random.seed(id+21684651)
    b = random.random()
    rgb = (r,g,b)
    return rgb


def set_polycolor(geo, color):
    mc.setAttr(geo + '.displayColors', 1)
    mc.polyOptions(geo, cm='diffuse')
    mc.polyColorPerVertex(geo, rgb=color)


def set_curvecolor(curveShape, color):
    mc.setAttr(curveShape + '.overrideEnabled', 1)
    mc.setAttr(curveShape + '.overrideRGBColors', 1)
    mc.setAttr(curveShape + '.overrideColorRGB', color[0], color[1], color[2])


def set_randomGeoColor(geo, seed):
    color = random_color(seed)
    set_polycolor(geo, color)


def clean(geo):
    mc.delete(geo, ch=True, icn=True)
    mc.xform(cp=True, ztp=True)
    return geo


bad_chars = "[]"


def findCenterVector(positions):
    center = [0, 0, 0]
    for pos in positions:
        center[0] += pos[0]
        center[1] += pos[1]
        center[2] += pos[2]
    center = [v / len(positions) for v in center]
    return center


def fetch_tube_loops(selection, verts=True):
    loops = []
    edges_along = mc.polySelect(selection, er=0)
    for edge in edges_along:
        ring = mc.polySelect(selection, elb=int(edge))
        if verts:
            ring_verts = mc.polyListComponentConversion(tv=1)
            loops.append(ring_verts)
    return loops


def fetchLoopCenters(selection):
    loops = fetch_tube_loops(selection)
    loopCenters = []

    for loopnum, loop in enumerate(loops):
        verts = loop[0].split(".vtx")[1].split(":")
        for c in bad_chars:
            for i, v in enumerate(verts):
                if c in v:
                    verts[i] = v.replace(c, "")

        verts = [int(vert) for vert in verts]
        vert_positions = []

        for vert in range(verts[0], verts[1] + 1):
            vert_positions.append(mc.pointPosition(selection + ".vtx[" + str(vert) + "]", w=1))

        center = findCenterVector(vert_positions)
        loopCenters.append(center)
    return loopCenters


def createTubeCenterGuide():
    selection = mc.ls(sel=1,l=1)[0]
    loopCenters = fetchLoopCenters(selection)
    print loopCenters
    mc.curve(p=loopCenters)