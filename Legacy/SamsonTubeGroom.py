import maya.mel as mm
import maya.cmds as mc
import pymel.core as pm
import maya.OpenMaya as om

import random

# HDA Locations for -HoudiniAsset Load Asset
#hdalib = 'C:\Users\Chris Thwaites\Desktop\SAMSON\hdas\\'

hdalib = '/sunrise/global/sunrise/assetbuilds/houdini_library/release/'

voronoi = hdalib + 'mayavoronoisurface-v02.00.hda'
voronoi_ass = 'sunrise_asset::Sop/mayavoronoisurface::02.00'

curvefromface = hdalib + 'mayacurvefrompolygonface-v01.00.hda'
curvefromface_ass = 'sunrise_asset::Sop/mayacurvefrompolygonface::01.00'

tubefromface = hdalib + 'mayahairtubefrompolygonface-v01.00.hda'
tubefromface_ass = 'sunrise_asset::Sop/mayahairtubefrompolygonface::01.00'

curvesfromtube = hdalib + 'mayacurvesfromtubegenerator-v01.00.hda'
curvesfromtube_ass = 'sunrise_asset::Sop/mayacurvesfromtubegenerator::01.00'


# GLOBAL FUNCTIONS

def samson_check():
    contents = pm.ls(assemblies=True)
    samson_systems = []
    for item in contents:
        if item == 'samson':
            samson_systems.append(item)

    if len(samson_systems) == 1:
        print "Samson System Found"
        return True
    else:
        check = pm.confirmDialog(m="No Samson Systems Found.\nWould you like to create a new one?", ma='center', b=('OK', 'Cancel'))
        if check == 'OK':
            return 'OK'
        if check == 'Cancel':
            return 'Cancel'


def fetchdescriptions():
    descriptions = []


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
    items = mc.listRelatives(group_name, c=True, type='transform')
    groom = group_name.split('_')[0]
    nums = []
    for i in items:
        if groom in i:
            clumpid = re.findall('\d+', i)[0]
            nums.append(int(clumpid))

    nums.sort()
    if len(nums)>0:
        iteration_num = nums[-1] + 1
    else:
        iteration_num = 0
    iteration_num = format(iteration_num, '03')
    return iteration_num


def addgroomattr(object, groom):
    mc.addAttr(object, longName='groom', dataType='string')
    mc.setAttr(object + '.groom', groom, type='string')


# SCALP FUNCTIONS

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


def refresh_scalp():
    # selecting verts and detaching to create separate faces
    selection = mc.ls(selection=True)[0]
    vertex_count = mc.polyEvaluate(v=True)
    mc.select(selection + '.vtx[0:' + str(vertex_count) + ']')
    mc.DetachComponent()
    vertex_count = mc.polyEvaluate(v=True)

    # iterate over faces vertices, applying colour according to face number
    for vert in range(0, vertex_count):
        mc.select(selection + '.vtx[' + str(vert) + ']')
        facenumber = mc.polyInfo(vf=True)[0]
        facenumber = int(facenumber.split(':')[1])
        color = random_color(facenumber)
        mc.polyColorPerVertex(rgb = color)

    mc.select(selection)
    mc.polyMergeVertex(d=0.25, am=True)
    clean(selection)
    mc.select(cl=True)


def export_regionmap(refresh=False):

    # refresh scalp if necessary
    if refresh:
        refresh_scalp()
    # selecting verts and detaching to create separate faces

    selection = mc.ls(selection=True)[0]
    face_count  = mc.polyEvaluate(selection, f=True)
    new_shaders = []

    for face in range(0, face_count):
        color = random_color(face)
        shader = mc.shadingNode('lambert', asShader=True)
        new_shaders.append(shader)
        mc.setAttr(shader + '.color', color[0], color[1], color[2])
        mc.select(selection + '.f[' + str(face) + ']')
        mc.hyperShade(assign=shader)

    path= ""

    # mc.surfaceSampler(target='pSphere1',
    #                   source='pSphere1',
    #                   mapOutput='diffuseRGB',
    #                   mapWidth=225,
    #                   mapHeight=225,
    #                   filename="/home/christhwaites/Desktop/test/",
    #                   fileFormat="jpg",
    #                   superSampling=0)
    #
    #
    # for i in range(0, face_count):
    #     mc.delete(new_shaders[i], new_shaders[i] + 'SG')


# CENTERGUIDE FUNCTIONS

def curvefromsurface(length, groom):
    # fetching face and surface info

    sel = mc.ls(selection=True)[0]
    face = sel.split('.')[1].split('f')[1]
    facenumber = ''.join(x for x in face if x.isdigit())
    surface = sel.split('.')[0]
    id = getrandom_id()

    polyShape = mc.listRelatives(sel, p=True)[0]
    polyTransform = mc.listRelatives(polyShape, p=True)[0]

    # generating colour from clumpid

    color = random_color(id)

    # creating iteration number and clumpgroup

    groom_clumpgroup = groom + '_clumps_grp'
    clump_number = iteration(groom_clumpgroup)
    clumpgroup = mc.group(empty=True, n=groom + '_clump_' + clump_number)

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

    addgroomattr(curveShape, groom)

    # colouring curve

    try:
        set_curvecolor(curveShape, color)
    except:
        pass

    # renaming and parenting curve group

    curveid = groom + '_controlCurve_' + clump_number
    mc.rename(curveTransform, curveid)
    curveShape = mc.listRelatives(curveid, ad=True, type='nurbsCurve')
    mc.rename(curveShape, curveid + 'Shape')

    mc.parent(curveid, clumpgroup)
    mc.parent(clumpgroup, groom_clumpgroup)
    clean(curveid)

    # removing asset

    mc.delete(asset)

    # adding groom and clumpids attrs


    add_id_attr(clumpgroup, id)
    add_id_attr(curveid, id)
    add_id_attr(curveid + 'Shape', id)

    addgroomattr(clumpgroup, groom)
    addgroomattr(curveid, groom)


def editcenterguide():
    tube = mc.ls(selection=True)
    if len(tube) == 0:
        mc.confirmDialog(m="Nothing Selected. Please select either a HairTube or CenterGuide", ma='center', b='OK')
    else:
        tube = tube[0]
        connection = mc.connectionInfo(tube + '.drawOverride', sfd=True)

        # disconnect attribute if connected and store previous layer input

        if connection != '':
            try:
                mc.disconnectAttr(connection, tube + '.drawOverride')
                mc.select(tube)
                mc.addAttr(longName='layerDrawOveride', dataType='string')
                mc.setAttr(tube + '.layerDrawOveride', connection, type='string')
            except:
                pass

        groom = mc.getAttr(tube + '.groom')
        mc.setAttr(tube + '.overrideEnabled', 1)
        mc.setAttr(tube + '.overrideDisplayType', 1)
        clumpid = re.findall('\d+', tube)[0]
        curve = groom + '_controlCurve_' + clumpid
        mc.select(curve)
        mc.selectMode(co=True)


def savecenterguide_changes():
    curve = mc.ls(selection=True)
    if len(curve) == 0:
        mc.confirmDialog(m="Nothing Selected. PLease select either a HairTube or CenterGuide", ma='center', b='OK')

    curve = curve[0]
    if 'cv' in curve:
        curve = curve.split('.')[0]
    else:
        curve = curve
    groom = mc.getAttr(curve + '.groom')

    clumpid = re.findall('\d+', curve)[0]
    tube = groom + '_tube_' + clumpid
    if mc.attributeQuery(tube + '.layerDrawOveride', exists=True, node=tube):
        connection = mc.getAttr(tube + '.layerDrawOveride')
    else:
        connection = ''

    if connection is not '':
        mc.connectAttr(connection, tube + '.drawOverride')
    else:
        mc.setAttr(tube + '.overrideDisplayType', 0)
    mc.selectMode(o=True)
    mc.select(tube)


def rebuildcurve(spans):
    curve = mc.ls(selection=True)[0]
    if 'cv' in curve:
        curve = curve.split('.')[0]
        groom = curve.split('_')[0]
    else:
        groom = mc.getAttr(curve + '.groom')
    clumpid = int(re.findall('\d+', curve)[0])
    clumpid = format(clumpid, '03')
    curve = groom + "_controlCurve_" + clumpid
    mc.rebuildCurve(curve, rt=0, spans=spans)
    mc.select(curve)
    mc.selectMode(co=True)


def select_curves(groom):
    curves = mc.ls(groom + '_controlCurve*', type='transform')
    mc.select(curves)
    return curves


def select_guidecurves():
    guidecurves = mc.ls('*guideCurve*', type='transform')
    mc.select(guidecurves)
    return guidecurves


# TUBE FUNCTIONS

def attachtube(width):

    # fetching face, facenumber, curveshape, curvetransform, groom

    sel = mc.ls(selection=True)

    curveShape = mc.listRelatives(sel, ad=True, typ='nurbsCurve')[0]
    curveTransform = mc.listRelatives(curveShape, p=True)[0]

    groom = mc.getAttr(curveTransform + '.groom')

    surfaceTransform = groom + '_scalp'
    surfaceShape = mc.listRelatives(surfaceTransform, ad=True, typ='mesh')[0]

    # fetching id and clumpid and clumpgroup

    rand_id = mc.getAttr(curveTransform + '.clumpid')

    clumpid = int(re.findall('\d+', curveTransform)[0])
    clumpid = format(clumpid, '03')

    clumpgroup = groom + '_clump_' + clumpid

    # if face in selection, snap first cv to face center

    for item in sel:
        itemType = mc.ls(item, st=True)
        if 'float' in itemType[1]:
            face = item
            facenumber = face.split('.')[1].split('f')[1]
            facenumber = ''.join(x for x in facenumber if x.isdigit())
            # fetching face center
            facegeo = pm.MeshFace(face)
            pt = facegeo.__apimfn__().center(om.MSpace.kWorld)
            faceCenter = pm.datatypes.Point(pt)
            # snapping first point on curve to faceCenter
            firstPoint = curveTransform + '.cv[0]'
            mc.move(faceCenter[0], faceCenter[1], faceCenter[2], firstPoint, a=True)
            # fetching colour of polyface
            verts = mc.polyInfo(face, fv=True)[0]
            verts = [int(s) for s in verts.split() if s.isdigit()]
            mc.select(surfaceTransform + '.vtx[{0}]'.format(verts[0]))
            color = mc.polyColorPerVertex(query=True, r=True, g=True, b=True)
    else:
        color = random_color(rand_id)

    # dropping HoudiniAsset, setting inputs and setting parameters

    asset = mm.eval('houdiniAsset -loadAsset "{0}" "{1}"'.format(tubefromface, tubefromface_ass))
    mc.select(curveTransform)
    mm.eval('AEhoudiniAssetSetInputToSelection "{0}.input[0].inputNodeId"'.format(asset))
    mc.select(surfaceTransform)
    mm.eval('AEhoudiniAssetSetInputToSelection "{0}.input[1].inputNodeId"'.format(asset))
    mc.setAttr(asset + '.houdiniAssetParm_width_multiply', width)
    mc.setAttr(asset + '.houdiniAssetParm_facenumber', 0)
    mc.parent(asset, clumpgroup)

    # creating HoudiniAsset names

    hda = groom + '_hdaTube_' + clumpid
    tube = groom + '_tube_' + clumpid

    # fetching generated hair tube

    houdiniAsset = mc.listRelatives(clumpgroup, ad=True, type='houdiniAsset', f=True)[0]
    mc.rename(houdiniAsset, hda)

    tubeShape = mc.listRelatives(hda, ad=True, type='mesh', f=True)[0]
    mc.rename(tubeShape, tube + 'Shape')

    tubeTransform = mc.listRelatives(tube + 'Shape', p=True, f=True)[0]
    mc.rename(tubeTransform, tube)

    mc.parent(tube, clumpgroup)

    # setting colour

    set_polycolor(tube, color)

    # setting random ID as extra attrib

    add_id_attr(tube, rand_id)
    add_id_attr(tube + 'Shape', rand_id)

    addgroomattr(tube, groom)
    addgroomattr(tube + 'Shape', groom)

    # cleanup

    unused = mc.listRelatives(hda, ad=True)
    for object in unused:
        mc.delete(object)


def edittube():
    tube = mc.ls(selection=True)[0]
    clumpid = re.findall('\d+', tube)[0]
    clump_hda = 'HDA_tubefromface_clumpid_' + clumpid
    mc.select(clump_hda)


def select_tubes(groom):
    tubes = mc.ls(groom + '_tube_*', type='transform')
    mc.select(tubes)
    return tubes


def deletetube():
    tube = mc.ls(selection=True)[0]
    groom = mc.getAttr(tube + '.groom')
    clumpid = re.findall('\d+', tube)[0]
    mc.delete(groom + '_tube_' + clumpid)
    mc.delete(groom + '_hdaTube_' + clumpid)


# GENERATE CURVES

def deleteguidecurves():

    # establishing clumpid

    selection = mc.ls(selection=True)[0]
    clumpid = re.findall('\d+', selection)[0]
    clumpgroup = 'clumpid_' + str(clumpid)

    # deleting existing guide curves in group

    group_contents = mc.listRelatives(clumpgroup, ad=True, type='transform')
    existing_guides = []
    for guide in group_contents:
        if 'guideCurve' in guide:
            existing_guides.append(guide)
    if len(existing_guides) > 0:
        mc.delete(existing_guides)


def gencurvesfromtube(keepLive=False, numberofcurves=3, onlyoutercurves=False):

    # dropping HoudiniAsset, setting inputs and setting parameters
    selection = mc.ls(selection=True)[0]
    clumpid = re.findall('\d+', selection)[0]
    clumpgroup = 'clumpid_' + str(clumpid)

    # deleting existing guide curves in group
    group_contents = mc.listRelatives(clumpgroup, ad=True)
    existing_guides = []
    for guide in group_contents:
        if 'guideCurve' in guide:
            existing_guides.append(guide)
    if len(existing_guides) > 0:
        mc.delete(existing_guides)

    # dropping hda and creating guide curves

    asset = mc.houdiniAsset(loadAsset=[curvesfromtube, curvesfromtube_ass])
    mc.select('tubeTransform_clumpid_'+clumpid)
    mm.eval('AEhoudiniAssetSetInputToSelection "{0}.input[0].inputNodeId"'.format(asset))

    curves = mc.listRelatives(asset, ad=True, type='nurbsCurve')

    for i, curve in enumerate(curves):
        curveName = 'clumpid_' + str(clumpid) + '_guideCurve_' + str(i)
        curveTransform = mc.listRelatives(curve, p=True)[0]
        mc.rename(curveTransform, curveName)
        mc.parent(curveName, clumpgroup)
        clean(curveName)

    mc.setAttr(asset + '.houdiniAssetParm_GuideCurves', numberofcurves)
    if onlyoutercurves:
        mc.setAttr(asset + '.houdiniAssetParm_onlyOuterCurves', 1)
    mc.delete(asset)


def gencurvesglobal(numberofcurves, onlyoutercurves=False):
    tubes = select_tubes()
    for tube in tubes:
        mc.select(tube)
        gencurvesfromtube(numberofcurves=numberofcurves, onlyoutercurves=onlyoutercurves)


def remove_allguidecurves():
    tubes = select_tubes()
    for tube in tubes:
        mc.select(tube)
        deleteguidecurves()


def extract_guide_curves():

    guideGroup = mc.group(em=True, n='ExtractedGuideCurves_GRP', w=True)
    curves = select_curves()
    guidecurves = select_guidecurves()
    curves = curves + guidecurves

    # disconnect attribute if connected and store previous layer input

    for i, curve in enumerate(curves):
        name = "guideCurve_" + str(i)
        mc.select(curve)
        mc.duplicate(n=name, ic=False, un=False)
        curveShape = mc.listRelatives(name, shapes=True)

        connection = mc.connectionInfo(name + '.drawOverride', sfd=True)
        if connection != '':
            mc.disconnectAttr(connection, name + '.drawOverride')
        # shapeconnection = mc.connectionInfo(curveShape + '.drawOverride', sfd=True)
        # if shapeconnection != '':
        #     mc.disconnectAttr(shapeconnection, curveShape + '.drawOverride')

        if curveShape:
            mc.parent(name, guideGroup)



# DELETE CLUMP

def deleteclump():
    selection = mc.ls(selection=True)[0]
    clumpid = int(re.findall('\d+', selection)[0])
    print "clumpid {0} successfully deleted".format(clumpid)
    clumpid = format(clumpid, '03')
    mc.delete('clumpid_' + str(clumpid))


# EXPORT FUNCTIONS

def setfacenumbertozero():
    tubes = select_tubes()
    for tube in tubes:
        clumpid = re.findall('\d+', tube)[0]
        hda = 'HDA_tubefromface_clumpid_' + str(clumpid)
        mc.setAttr(hda + '.houdiniAssetParm_facenumber', 0)


def exporttubes_and_guides(all=False, separate=False):

    contents = mc.ls()

    tubes = []

    for item in contents:
        if 'tubeTransform' in item:
            tubes.append(item)
            mc.select(item, add=True)
