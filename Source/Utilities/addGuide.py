'''
Adding Curve to selected mesh at UV of ScreenSpace Selection
'''

'''
Maya Intrinsic Imports
'''
import maya.cmds as mc


class AddGuide():
    def __init__(self, surface, numspans):
        self.numspans = numspans
        self.surface = surface
        self.context = "follicleContext"


    # creates a sample closest point on Mesh to sample world space
    def getuv_from_world(self, queryPos):
        surfaceShape = self.surface
        pointOnMesh = mc.createNode("closestPointOnMesh")
        mc.connectAttr(surfaceShape + ".outMesh", pointOnMesh + ".inMesh")
        mc.connectAttr(surfaceShape + ".worldMatrix", pointOnMesh + ".inputMatrix")
        mc.setAttr(pointOnMesh + ".inPositionX", queryPos[0])
        mc.setAttr(pointOnMesh + ".inPositionY", queryPos[1])
        mc.setAttr(pointOnMesh + ".inPositionZ", queryPos[2])
        uv = (mc.getAttr(pointOnMesh + ".parameterU"), mc.getAttr(pointOnMesh + ".parameterV"))
        mc.delete(pointOnMesh)
        return uv


    # creates and connects follicle at uv location on given surface
    def new_follicle(self, uv):
        print self.surface
        surface = self.surface
        newFollicle = mc.createNode('follicle')
        surfaceShape = self.surface
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
    def newCurve(self, length):
        length = float(length)
        positions = [(0, 0, 0), (0, 0, length * 0.25), (0, 0, length * 0.75), (0, 0, length)]
        newCurve = mc.curve(p=positions)
        return newCurve


    # context function
    def onPress(self):
        # create newCurveatOrigin
        print "creating a newcurve"
        newGuide = self.newCurve(5)
        # makeSurfaceLive
        print "making surface live"
        mc.makeLive(self.surface)
        hitPos = mc.autoPlace(um=1)
        uv = self.getuv_from_world(hitPos)
        guideFollicle = self.new_follicle(uv)
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


    def addGuide(self):
        if mc.draggerContext(self.context, exists=True):
            print "setting context"
            mc.deleteUI(self.context)

        mc.draggerContext(self.context, name = self.context, releaseCommand= self.onPress,
                          cursor="crossHair")
        print "set dragger context"
        mc.setToolTo(self.context)
        print "set tool to follicle context"

def main(surface, numspans):
    print "Adding Guide..."
    AddGuide(surface, numspans).addGuide()


#TO STUDY:
# import maya.cmds as cmds
# import pymel.core as pm
# import maya.api.OpenMaya as om
# import maya.api.OpenMayaUI as omui
#
# Context = 'Context'
#
#
# class SamsClass():
#
#     def __init__(self):
#         pass
#
#     def pointLocator(self, *args):
#         '''
#         pass in the name of a mesh, or just select one
#         '''
#
#         # clear any previous contexts
#         if cmds.draggerContext(Context, exists=True):
#             print 'deleting'
#             cmds.deleteUI(Context)
#         cmds.setToolTo('selectSuperContext')
#
#         # parse args and selection
#         mesh = None
#         self.geo = None
#         if args:
#             mesh = pm.PyNode(args[0])
#         else:
#             try:
#                 mesh = pm.selected()[0]
#             except Exception as e:
#                 pass
#
#         # make sure we have a the Transform of a Mesh object
#         if isinstance(mesh, pm.nodetypes.Transform):
#             mesh = mesh.getShape(ni=True)
#         if isinstance(mesh, pm.nodetypes.Mesh):
#             self.geo = mesh.getParent()
#         if not self.geo:
#             print 'Invalid selection. Please select a poly object.'
#             return
#
#         # create context and set tool
#         cmds.draggerContext(Context, pressCommand=self.onPress, dragCommand=self.onDrag, name=Context,
#                             cursor='crossHair')
#         cmds.setToolTo(Context)
#
#     def onPress(self):
#         vpX, vpY, _ = cmds.draggerContext('Context', query=True, anchorPoint=True)
#         pos = om.MPoint()
#         direction = om.MVector()
#         omui.M3dView().active3dView().viewToWorld(int(vpX), int(vpY), pos, direction)
#         selectionList = om.MSelectionList()
#         selectionList.add(self.geo.name())
#         dagPath = selectionList.getDagPath(0)
#         self.fnMesh = om.MFnMesh(dagPath)
#         self.intersection = self.fnMesh.closestIntersection(om.MFloatPoint(pos), om.MFloatVector(direction),
#                                                             om.MSpace.kWorld, 99999, False)
#
#         if self.intersection:
#             hitPoint, hitRayParam, hitFace, hitTriangle, hitBary1, hitBary2 = self.intersection
#
#         if hitTriangle != -1:
#             self.loc1 = pm.spaceLocator(p=(hitPoint[0], hitPoint[1], hitPoint[2]), a=True)
#             cmds.refresh()
#
#     def onDrag(self):
#         vpX, vpY, _ = cmds.draggerContext('Context', query=True, dragPoint=True)
#         pos = om.MPoint()
#         direction = om.MVector()
#         omui.M3dView().active3dView().viewToWorld(int(vpX), int(vpY), pos, direction)
#         dragIntersection = self.fnMesh.closestIntersection(om.MFloatPoint(pos), om.MFloatVector(direction),
#                                                            om.MSpace.kWorld, 99999, False)
#
#         if dragIntersection:
#             hitPoint, hitRayParam, hitFace, hitTriangle, hitBary1, hitBary2 = dragIntersection
#
#         if hitTriangle != -1:
#             self.loc1.localPosition.set(0, 0, 0)
#             verts = [self.geo.vtx[i] for i in self.geo.f[hitFace].getVertices()]
#             closest = None
#             minLength = None
#             pos = pm.datatypes.Point(*hitPoint)
#             for v in verts:
#                 vpos = v.getPosition(space='world')
#                 thisLength = (pos - vpos).length()
#                 if minLength is None or thisLength < minLength:
#                     minLength = thisLength
#                     closest = vpos
#
#             self.loc1.setTranslation(closest, space='world')
#             cmds.refresh()
#
#
# '''
# Select the base mesh before running the following
# '''
# a = SamsClass()
# a.pointLocator()