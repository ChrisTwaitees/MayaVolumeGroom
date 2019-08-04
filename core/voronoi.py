'''
Maya Intrinsic Imports
'''
import maya.cmds as mc
import maya.api.OpenMaya as om

import random
from ..utils import geo


def fetchNumberCells():
    input = mc.promptDialog(b = ["Voronoi", "Cancel"], m = "Number of Cells", ma = "center", st = "integer", t = "VORONOI SELECTION" )
    if input == "Voronoi":
        input = mc.promptDialog(query=1, text=1)
        return input
    if input == "Cancel":
        return 0


def getSelectionSurface(selection):
    mc.select(selection)
    mcSelection = mc.ls(selection=1, l=1)[0]
    selList = om.MGlobal.getActiveSelectionList()
    path = selList.getDagPath(0)
    path.extendToShape()
    surface = om.MFnMesh(path)
    return mcSelection, surface


def randomUVs(numPoints):
    print numPoints
    u = [random.uniform(0, 1) for i in xrange(numPoints)]
    v = [random.uniform(0, 1) for i in xrange(numPoints)]
    uvs = zip(u, v)
    return uvs


def WS_from_UV(uv, MfnMesh):
    numFaces = MfnMesh.numPolygons
    for i in range(numFaces):
        try:
            pos = MfnMesh.getPointAtUV(i, uv[0], uv[1], om.MSpace.kWorld)
            break;  # point is in poly
        except:
            pos = (0.0, 0.0, 0.0, 0.0)
            continue  # point not found!
    return (pos[0], pos[1], pos[2])


def Voronoi(uvs, selection):
    try:
        originalName = selection
        mcSelection = getSelectionSurface(selection)[0]
        surface = getSelectionSurface(selection)[1]

    except (IndexError):
        return
    centers = [WS_from_UV(uv, surface) for uv in uvs if WS_from_UV(uv, surface)[0]]
    newFaces = []

    #create progress bar
    progressBarWindow = utils.pyside.SimpleProgressBar("Voronoi Cells", "Dividing 0/{0}".format(len(centers)))
    progressBarWindow.show()
    #setting cursor to wait cursor
    utils.pyside.qw.QApplication.setOverrideCursor(utils.pyside.qc.Qt.WaitCursor)

    for i, from_point in enumerate(centers):
        working_geom = mc.duplicate(mcSelection)
        for to_point in centers:
            if from_point != to_point:
                print "**** Cut "

                locator = mc.spaceLocator()
                mc.move(from_point[0], from_point[1], from_point[2])
                mc.parent(locator, working_geom)

                center_point = [(e1 + e2) / 2 for (e1, e2) in zip(to_point, from_point)]
                n = [(e1 - e2) for (e1, e2) in zip(from_point, to_point)]

                es = mc.angleBetween(euler=True, v1=[0, 0, 1], v2=n)

                mc.polyCut(working_geom, deleteFaces=True, cutPlaneCenter=center_point, cutPlaneRotate=es)

                # RandomColors
                mc.setAttr(working_geom[0] + '.displayColors', 1)
                mc.polyOptions(working_geom[0], cm='diffuse')
                mc.polyColorPerVertex(working_geom[0], rgb=utils.geo.random_color(i))

                newFaces.append(working_geom[0])

                #update progressbar
                progressBarWindow.updateLabel("Dividing {0}/{1}".format(i, len(centers)))
                progressBarWindow.updateProgress( len(centers)/(i+1.0)*100.0)


    #removing progressbar
    utils.pyside.qw.QApplication.restoreOverrideCursor()
    progressBarWindow.hide()
    progressBarWindow.deleteLater()


    mc.delete(mcSelection)
    scalp = mc.polyUnite(newFaces, n= originalName)
    mc.polyMergeVertex(scalp, d=0.25)


def main(surface):
    numCells = int(fetchNumberCells())
    if numCells:
        uvs = randomUVs(numCells)
        Voronoi(uvs, surface)
    else:
        print "User Cancelled Voronoi"
        return