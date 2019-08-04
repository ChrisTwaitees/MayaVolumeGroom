'''
Collection of Maya selection methods
'''
import maya.cmds as mc
import pymel.core as pm
import maya.api.openMaya as om


def fetch_selection(OpenMaya=False, cmds = False, pymel=False, shape=False):
    if OpenMaya:
        sel_list = om.MGlobal.getActiveSelectionList()
        path = sel_list.getDagPath(0)
        path.extendToShape()
        surface = om.MFnMesh(path)
        return surface
    elif cmds:
        selection = mc.ls(selection=1, l=1)[0]
        return selection
    elif shape:
        selection = mc.ls(selection=1, l=1)[0]
        selection = mc.listRelatives(selection, shapes=1, ad=1, f=1)[0]
        return selection
    elif pymel:
        selection = pm.ls(selection=1, l=1)[0]
        return pm.listRelatives(selection, shapes=1, ad=1, f=1)[0]
    else:
        print "No Method of Selection chosen, valid args:\n" \
              " <OpenMaya>, <cmds>, <pymel>, <shape> "


def get_items_from_selection():
    oSelection = om.MGlobal.getActiveSelectionList()
    objects = []
    for i in range(0, oSelection.length()):
        path, object = oSelection.getComponent(i)
        objects.append((path, object))
    return objects


def get_locators_from_selection():
    objects = get_items_from_selection()
    locators = []
    for path, object in objects:
        if path.extendToShape().apiType() == om.MFn.kLocator:
            locators.append((path, object))
    return locators


def get_meshes_from_selection():
    objects = get_items_from_selection()
    meshes = []
    for path, oject in objects:
        if path.extendToShape().apiType() == om.MFn.kMesh:
            meshes.append((path, object))

    return meshes