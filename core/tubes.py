'''
Creating Cylinder at the base of a selected curve,
correctly orienting to curve's normal.
'''

'''
Maya Intrinsic Imports
'''
import maya.cmds as mc
import pymel.core as pm

def addTube(selection, tubesubdivs=8):
    dt = pm.dt

    worldUp = dt.Vector([0, 1, 0])
    selShape = mc.listRelatives(selection, shapes=1, ad=1, f=1)[0]

    curveBaseNormal = mc.pointOnCurve(sel, pr=0, nn=1, top=1)
    curveBasePosition = mc.pointOnCurve(sel, pr=0, p=1, top=1)
    curveBasePosition_UpRef = mc.pointOnCurve(sel, pr=0.1, p=1, top=1)

    # creates vector datatype so we get helper functions like cross product from pymel
    base = dt.Vector(curveBasePosition)
    normal = dt.Vector(curveBaseNormal)
    up = dt.Vector(curveBasePosition_UpRef)
    up = -(up - normal).normal()
    aim = dt.cross(up, normal)

    # locators at reference frame vectors
    referenceframe = {"normal": normal, "up": up, "aim": aim}
    [pm.spaceLocator(p=base + v, n=k) for k, v in referenceframe.items()]

    # create polycylinder
    axis = referenceframe["aim"]
    subdivisionsx = tubesubdivs
    subdivisionsy = tubesubdivs
    subdivisionsz = tubesubdivs
    cylinder = mc.polyCylinder(axis=axis, radius=1, height=1, sx=subdivisionsx, sy=subdivisionsy, sz=subdivisionsz, cuv=3)
    return cylinder