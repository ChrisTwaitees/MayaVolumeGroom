def fetch_selection(om=False, mc = False, mm=False):
    if om:
        sel_list = om.MGlobal.getActiveSelectionList()
        path = sel_list.getDagPath(0)
        path.extendToShape()
        surface = om.MFnMesh(path)
        return surface
    elif mc:
        selection = mc.ls(selection=1, l=1)[0]
        return selection
    elif mm:
        return
    else:
        print "No Method of Selection chosen, valid args:\n" \
              "om <OpenMaya>, mc <Maya.cmds>, mm <Pymel>"



