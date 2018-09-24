'''
Maya Intrinsic Imports
'''
import maya.cmds as mc
import maya.api.OpenMaya as om
import pymel.core as pm

def fetch_selection(openMaya=False, cmds = False, pymel=False, shape=False):
    if openMaya:
        sel_list = om.MGlobal.getActiveSelectionList()
        path = sel_list.getDagPath(0)
        path.extendToShape()
        surface = om.MFnMesh(path)
        return surface
    elif cmds:
        selection = mc.ls(selection=1, l=1)[0]
        if shape:
            selection = mc.listRelatives(selection, shapes=1, ad=1, f=1)[0]
            return selection
        else:
            return selection
    elif pymel:
        return
    else:
        print "No Method of Selection chosen, valid args:\n" \
              "om <OpenMaya>, mc <Maya.cmds>, mm <Pymel>"



