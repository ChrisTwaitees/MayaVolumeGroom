'''
Adding Curve to selected mesh at UV of ScreenSpace Selection
'''

'''
Maya Intrinsic Imports
'''
import maya.cmds as mc
import selection

# creates a sample closest point on Mesh to sample world space
def getuv_from_world(surface, queryPos):
    pointOnMesh = mc.createNode("closestPointOnMesh")
    surface = mc.listRelatives(surface, shapes=1, f=1)[0]
    mc.connectAttr(surface + ".outMesh", pointOnMesh + ".inMesh")
    mc.connectAttr(surface + ".worldMatrix", pointOnMesh + ".inputMatrix")
    mc.setAttr(pointOnMesh + ".inPositionX", queryPos[0])
    mc.setAttr(pointOnMesh + ".inPositionY", queryPos[1])
    mc.setAttr(pointOnMesh + ".inPositionZ", queryPos[2])
    uv = (mc.getAttr(pointOnMesh + ".parameterU"), mc.getAttr(pointOnMesh + ".parameterV"))
    mc.delete(pointOnMesh)
    return uv


# creates and connects follicle at uv location on given surface
def new_follicle(surface, uv):
    newFollicle = mc.createNode('follicle')
    surfaceShape = mc.listRelatives(surface, shapes=1, f=1)[0]
    follicleTrans = mc.listRelatives(newFollicle, type="transform", p=1)[0]
    mc.connectAttr(newFollicle + ".outRotate", follicleTrans + ".rotate")
    mc.connectAttr(newFollicle + ".outTranslate", follicleTrans + ".translate")
    mc.connectAttr(surfaceShape + ".outMesh", newFollicle + ".inputMesh")
    mc.connectAttr(surfaceShape + ".worldMatrix", newFollicle + ".inputWorldMatrix")
    mc.setAttr(newFollicle + ".simulationMethod", 0)
    mc.setAttr(newFollicle + ".parameterU", uv[0])
    mc.setAttr(newFollicle + ".parameterV", uv[1])
    return newFollicle


# returns a curve of defined length
def newCurve(length, numspans):
    length = float(length)
    positions = [(0, 0, 0), (0, 0, length * 0.25), (0, 0, length * 0.75), (0, 0, length)]
    newCurve = mc.curve(p=positions)
    mc.rebuildCurve(newCurve, spans=numspans, keepEndPoints=1)
    return newCurve


# context function
def onPress(context):
    # create newCurveatOrigin
    newGuide = newCurve(5, 8)
    # makeSurfaceLive
    mc.makeLive(surface)
    hitPos = mc.autoPlace(um=1)
    uv = getuv_from_world(surface, hitPos)
    guideFollicle = new_follicle(surface, uv)
    # cleanup
    mc.makeLive(none=1)
    follicleTrans = mc.listRelatives(guideFollicle, type="transform", p=1)[0]
    mc.parentConstraint(follicleTrans, newGuide)
    mc.parent(newGuide, follicleTrans)

    # pin base cvOfCurve
    curveShape = mc.listRelatives(newGuide, s=1, f=1)[0]
    decomposeMatrix = mc.createNode("decomposeMatrix")
    mc.connectAttr(follicleTrans + ".parentMatrix", decomposeMatrix + ".inputMatrix")
    mc.connectAttr(decomposeMatrix + ".outputTranslate", curveShape + ".controlPoints[0]")


def addGuide(surface):
    follicleContext = "follicleContext"
    if mc.draggerContext(follicleContext, exists=True):
        mc.deleteUI(follicleContext)
    mc.draggerContext(follicleContext, releaseCommand="onPress(follicleContext)", cursor="crossHair")
    mc.setToolTo(follicleContext)


if __name__ == "__main__":
    surface = selection.fetch_selection(mc = True)
    addGuide(surface)