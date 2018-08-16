import maya.cmds as mc
import maya.api.OpenMaya as om
import random
import math

numPoints = 5

mcSelection = mc.ls(selection=1, l=1)[0]
selList = om.MGlobal.getActiveSelectionList()
path = selList.getDagPath(0)
path.extendToShape()
surface = om.MFnMesh(path)

u = [random.uniform(0, 1) for i in xrange(numPoints)]
v = [random.uniform(0, 1) for i in xrange(numPoints)]

uvs = zip(u, v)


def WS_from_UV(uv, MfnMesh):
    numFaces = MfnMesh.numPolygons
    WSpoint = om.MPoint(0.0, 0.0, 0.0)
    for i in range(numFaces):
        try:
            pos = MfnMesh.getPointAtUV(i, uv[0], uv[1], om.MSpace.kWorld)
            break;  # point is in poly
        except:
            pos = (0.0, 0.0, 0.0, 0.0)
            continue  # point not found!
    return (pos[0], pos[1], pos[2])


centers = [WS_from_UV(uv, surface) for uv in uvs if WS_from_UV(uv, surface)[0]]
newFaces = []

for i, from_point in enumerate(centers):
    working_geom = cmds.duplicate(mcSelection)
    for to_point in centers:
        if from_point != to_point:
            print "**** Cut "

            locator = mc.spaceLocator()
            cmds.move(from_point[0], from_point[1], from_point[2])
            cmds.parent(locator, working_geom)

            center_point = [(e1 + e2) / 2 for (e1, e2) in zip(to_point, from_point)]
            n = [(e1 - e2) for (e1, e2) in zip(from_point, to_point)]

            es = cmds.angleBetween(euler=True, v1=[0, 0, 1], v2=n)

            mc.polyCut(working_geom, deleteFaces=True, cutPlaneCenter=center_point, cutPlaneRotate=es)

            # RandomColors
            mc.setAttr(working_geom[0] + '.displayColors', 1)
            mc.polyOptions(working_geom[0], cm='diffuse')
            mc.polyColorPerVertex(working_geom[0], rgb=random_color(i))

            newFaces.append(working_geom[0])
cmds.delete(mcSelection)

scalp = mc.polyUnite(newFaces, n="scalp_test")
mc.polyMergeVertex(scalp, d=0.25)