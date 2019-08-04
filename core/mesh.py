import maya.api.OpenMaya as om
import maya.cmds as mc


def create_face_from_positions(positions):
    # Number of vertices per polygon
    vertices = []
    for position in positions:
        vertices.append(om.MPoint(position))

    # Number of vertices per polygon/face
    verts_per_face = []
    verts_per_face.append(int(len(positions)))

    # How each group of N vertices per face is connected
    vertices_build_order = om.MIntArray()
    for i in range(0, len(positions)):
        vertices_build_order.append(i)

    #create face
    mFace = om.MObject()
    FnFace = om.MFnMesh()
    FnFace.create(vertices, verts_per_face, vertices_build_order)

    #set to default shading group
    mc.sets(FnFace.name(), edit=True, forceElement="initialShadingGroup")
