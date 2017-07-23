import maya.mel as mm
import maya.cmds as mc
import pymel.core as pm
import maya.OpenMaya as om
import random

# HDA Locations for -HoudiniAsset Load Asset
hdalib = 'C:\Users\Chris Thwaites\Desktop\SAMSON\hdas\\'

#hdalib = '/sunrise/global/sunrise/assetbuilds/houdini_library/release/'

voronoi = hdalib + 'mayavoronoisurface-v02.00.hda'
voronoi_ass = 'sunrise_asset::Sop/mayavoronoisurface::02.00'

curvefromface = hdalib + 'mayacurvefrompolygonface-v01.00.hda'
curvefromface_ass = 'sunrise_asset::Sop/mayacurvefrompolygonface::01.00'

tubefromface = hdalib + 'mayahairtubefrompolygonface-v01.00.hda'
tubefromface_ass = 'sunrise_asset::Sop/mayahairtubefrompolygonface::01.00'

curvesfromtube = hdalib + 'mayacurvesfromtubegenerator-v01.00.hda'
curvesfromtube_ass = 'sunrise_asset::Sop/mayacurvesfromtubegenerator::01.00'



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


def add_id_attr(geo, id):
    mc.addAttr(geo, longName='clumpid', attributeType='long')
    mc.setAttr(geo + '.clumpid', id, lock=True)


def clean(geo):
    mc.delete(geo, ch=True, icn=True)
    mc.xform(cp=True, ztp=True)
    return geo


def iteration(group_name):
    items = mc.ls(assemblies=True)
    nums = []
    for i in items:
        if group_name in i:
            nums.append(int(i.split(group_name)[1]))

    nums.sort()
    if len(nums)>0:
        iteration_num = nums[-1] + 1
    else:
        iteration_num = 0
    iteration_num = format(iteration_num, '03')
    return iteration_num


def voronoisurface(subdivs):
    surface = mc.ls(selection=True)[0]

    iteration_num = iteration('VoronoiSurface_Grp_')
    surface = mc.rename(surface, "scalpSurface_clumpid_"+iteration_num)
    surfacegroup = mc.group(empty=True, n='VoronoiSurface_Grp_'+iteration_num)
    asset = mm.eval('houdiniAsset -loadAsset "{0}" "{1}"'.format(voronoi, voronoi_ass))
    mc.setAttr(asset + '.houdiniAssetParm_npts', subdivs)
    mc.select(surface)
    mm.eval('AEhoudiniAssetSetInputToSelection "{0}.input[0].inputNodeId"'.format(asset))
    mc.hide(surface)
    mc.parent(surface, surfacegroup)
    surface = clean(surface)
    mc.rename(surface, 'VoronoiOriginalSurface_' + iteration_num)
    mc.parent(asset, surfacegroup)
    face = mc.listRelatives(asset, ad=True, typ='mesh')
    scalpfaceid = "scalpFace_clumpid_"+iteration_num
    face = mc.parent(face, surfacegroup)
    mc.rename(face, scalpfaceid)
    clean(scalpfaceid)
    mc.polyOptions(scalpfaceid, cm='diffuse')
    mc.polyMergeVertex(scalpfaceid, d=0.25)
    mc.delete(asset)


def curvefromsurface(length):
    # fetching face and surface info

    sel = mc.ls(selection=True)[0]
    face = sel.split('.')[1].split('f')[1]
    facenumber = ''.join(x for x in face if x.isdigit())
    surface = sel.split('.')[0]

    polyShape = mc.listRelatives(sel, p=True)[0]
    polyTransform = mc.listRelatives(polyShape, p=True)[0]

    # fetching selected face color

    verts = mc.polyInfo(sel, fv=True)[0]
    verts = [int(s) for s in verts.split() if s.isdigit()]
    mc.select(polyTransform + '.vtx[{0}]'.format(verts[0]))
    try:
        color = mc.polyColorPerVertex(query=True, r=True, g=True, b=True)
    except:
        pass

    # creating iteration number and clumpgroup

    clump_number = iteration('clumpid_')
    clumpgroup = mc.group(empty=True, n='clumpid_'+clump_number)

    # creating houdiniAsset, setting inputs and setting attributes

    asset = mm.eval('houdiniAsset -loadAsset "{0}" "{1}"'.format(curvefromface, curvefromface_ass))
    mc.select(surface)
    mm.eval('AEhoudiniAssetSetInputToSelection "{0}.input[0].inputNodeId"'.format(asset))
    mc.setAttr(asset + '.houdiniAssetParm_length', length)
    mc.setAttr(asset + '.houdiniAssetParm_facenumber', int(facenumber))
    mc.parent(asset, clumpgroup)

    # fetching curve

    curveShape = mc.listRelatives(asset, ad=True, typ='nurbsCurve')[0]
    curveTransform = mc.listRelatives(curveShape, p=True)

    # colouring curve

    try:
        set_curvecolor(curveShape, color)
    except:
        pass

    # renaming and parenting curve

    curveid = 'centerGuide_clumpid_'+clump_number
    mc.rename(curveTransform, curveid)
    mc.parent(curveid, clumpgroup)
    clean(curveid)

    # removing asset

    mc.delete(asset)


def attachtube(width):

    # fetching face, facenumber, curveshape, curvetransform

    sel = mc.ls(selection=True)

    curveShape = mc.listRelatives(sel, ad=True, typ='nurbsCurve')[0]
    curveTransform = mc.listRelatives(curveShape, p=True)[0]


    for item in sel:
        itemType = mc.ls(item, st=True)
        if 'float' in itemType[1]:
            face = item
            facenumber = face.split('.')[1].split('f')[1]
            facenumber = ''.join(x for x in facenumber if x.isdigit())

    surfaceShape = mc.listRelatives(face, p=True)[0]
    surfaceTransform = mc.listRelatives(surfaceShape, p=True)[0]

    # fetching face center

    facegeo = pm.MeshFace(face)
    pt = facegeo.__apimfn__().center(om.MSpace.kWorld)
    faceCenter = pm.datatypes.Point(pt)

    # snapping first point on curve to faceCenter and locking point

    firstPoint = curveTransform + '.cv[0]'
    mc.move(faceCenter[0],faceCenter[1],faceCenter[2], firstPoint, a=True)

    # creating random id and color

    rand_id = getrandom_id()

    verts = mc.polyInfo(face, fv=True)[0]
    verts = [int(s) for s in verts.split() if s.isdigit()]
    mc.select(surfaceTransform + '.vtx[{0}]'.format(verts[0]))
    color = mc.polyColorPerVertex(query=True, r=True, g=True, b=True)

    clump_number = iteration('clumpid_')

    # parenting to world to join back to clumpgroup

    mc.parent(curveTransform, w=True)

    # if in existing clumpid group use group, if not, create new group

    for geo in sel:
        if 'clumpid' in geo:
            clump_number = geo.split('clumpid_')[-1]
            clumpgroup = 'clumpid_'+clump_number
        else:
            clumpgroup = mc.group(empty=True, n='clumpid_' + clump_number)

    # renaming curve

    curveid = 'centerGuide_clumpid_' + clump_number

    try:
        mc.rename(curveTransform, curveid)
    except:
        print curveid, "already exists"

    # parenting curve to clumpgroup

    mc.parent(curveid, clumpgroup)

    # dropping HoudiniAsset, setting inputs and setting parameters

    asset = mm.eval('houdiniAsset -loadAsset "{0}" "{1}"'.format(tubefromface, tubefromface_ass))
    mc.select(curveid)
    mm.eval('AEhoudiniAssetSetInputToSelection "{0}.input[0].inputNodeId"'.format(asset))
    mc.select(surfaceTransform)
    mm.eval('AEhoudiniAssetSetInputToSelection "{0}.input[1].inputNodeId"'.format(asset))
    mc.setAttr(asset + '.houdiniAssetParm_width_multiply', width)
    mc.setAttr(asset + '.houdiniAssetParm_facenumber', int(facenumber))
    mc.parent(asset, clumpgroup)

    # creating HoudiniAsset names

    hda = 'HDA_tubefromface_clumpid_' + clump_number
    tube = 'tube_clumpid_' + clump_number
    tubetransform = 'tubeTransform_clumpid_' + clump_number

    # fetching generated hair tube

    houdiniAsset = mc.listRelatives(clumpgroup, ad=True, type='houdiniAsset')[0]
    tubeShape = mc.listRelatives(houdiniAsset, ad=True, type='mesh')[0]
    tubeTransform = mc.listRelatives(tubeShape, p=True)[0]

    # renaming

    mc.rename(houdiniAsset, hda)
    mc.rename(tubeShape, tube)
    mc.rename(tubeTransform, tubetransform)

    mc.parent(tube, clumpgroup)

    # setting colour

    set_polycolor(tube, color)

    # setting random ID as extra attrib

    add_id_attr(tubetransform, rand_id)
    add_id_attr(tube, rand_id)
    add_id_attr(curveShape, rand_id)
    add_id_attr(curveTransform, rand_id)

    # cleanup

    #re

    unused = mc.listRelatives(hda, ad=True)
    for object in unused:
        mc.delete(object)


def templategeo():
    pass


def gencurvesfromtube():
    # dropping HoudiniAsset, setting inputs and setting parameters

    selection = mc.ls(selection=True)[0]
    asset = mc.houdiniAsset(loadAsset=[curvesfromtube, curvesfromtube_ass])
    mc.select(selection)
    mm.eval('AEhoudiniAssetSetInputToSelection "{0}.input[0].inputNodeId"'.format(asset))

    pass


def export_regionmap():

    # selecting verts and detaching to create separate faces
    selection = mc.ls(selection=True)[0]
    vertex_count = mc.polyEvaluate(v=True)
    mc.select(selection + '.vtx[0:' + str(vertex_count) + ']')
    mc.DetachComponent()

    # exporting vertex map

    mc.select(selection)
    iter = getrandom_id()
   #polypaint = 'artAttrPaintVertexCtx1' + str(iter)
    polypaint = 'artAttrPaintVertexCtx'
    # try:
    #     mc.artAttrPaintVertexCtx(polypaint, ch=True)
    # except():
    #     pass
    mc.select(selection + '.vtx[0:' + str(vertex_count) + ']')
    mc.setToolTo(polypaint)
    mc.artAttrPaintVertexCtx(efm='rgb', fsx=2048, fsy=2048, pvf=False)
    mm.eval('artExportMapDialog "{0}"'.format(polypaint))


    # reconnecting verts to form whole geo and deleting history

    # mc.polyMergeVertex(selection, d=0.25)
    # clean(selection)
    # print 'exporting of map successful!'

def switchselection_mode(selectionType):
    modes = {'object': 'o', 'component': 'co'}
    mc.selectMode(oc=True)
    pass


def exporttubes_and_guides(all=False, separate=False):

    contents = mc.ls()

    tubes = []

    for item in contents:
        if 'tubeTransform' in item:
            tubes.append(item)
            mc.select(item, add=True)

    
