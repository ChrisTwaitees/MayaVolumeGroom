import maya.cmds as mc
import pymel.core as pm
import maya.mel as mm

dt = pm.dt

worldUp = dt.Vector([0, 1, 0])

sel = mc.ls(selection=1, l=1)[0]
selShape = mc.listRelatives(sel, shapes=1, ad=1, f=1)[0]

curveBaseNormal = mc.pointOnCurve(sel, pr=0, nn=1, top=1)
curveBasePosition = mc.pointOnCurve(sel, pr=0, p=1, top=1)
curveBasePosition_UpRef = mc.pointOnCurve(sel, pr=0.1, p=1, top=1)

# creates vector datatype so we get helper functions like cross product from pymel
base = dt.Vector(curveBasePosition)

normal = dt.Vector(curveBaseNormal)

up = dt.Vector(curveBasePosition_UpRef)

up = -(up - normal).normal()

aim = dt.cross(up, normal)

referenceFrame = {"normal": normal, "up": up, "aim": aim}

[pm.spaceLocator(p=base + v, n=k) for k, v in referenceFrame.items()]

# create polycylinder

axis = referenceFrame["aim"]
subdivisionsX = 8
subdivisionsY = 8
subdivisionsZ = 8
cylinder = mc.polyCylinder(axis=axis, radius=1, height=1, sx=subdivisionsX, sy=subdivisionsY, sz=subdivisionsZ, cuv=3)

# selects every second edge loop
# mm.eval('polySelectEdgesEveryN "edgeRing" 2')

# polySelect() has some really interesting arguments in order to generate
# mc.polySelect()


# mc.setAttr()