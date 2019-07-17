import maya.api.OpenMaya as om


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


meshes = get_meshes_from_selection()
fnMesh = om.MFnMesh(meshes[0][0])
fnMesh.getPoints()
locators = get_locators_from_selection()
