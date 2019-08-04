import maya.cmds as mc
import maya.api.OpenMaya as om
from context import SamsonContext
import context
reload(context)
import mesh
reload(mesh)

def get_surface_pos_from_mouse(surface):
    # the surface needs to be live
    return mc.autoPlace(um=True)

def getuv_from_world(self, queryPos):
    # use om
    return

class AddCellContext(SamsonContext):
    def __init__(self, surface):
        super(AddCellContext, self).__init__()
        self.context_name = self.__class__.__name__
        self.samson_surface = surface
        self.create_context()

    def intialize_command(self):
        print "intialization invoked"
        # make surface live to query positions on surface
        mc.makeLive(self.samson_surface)
        # cell points
        self.cell_points = []

    def pre_press_command(self):
        mc.makeLive(self.samson_surface)
        print "Pre_press command invoked"

    def press_command(self):
        print "press invoked"
        point_on_surface = get_surface_pos_from_mouse(self.samson_surface)
        mc.spaceLocator(p=point_on_surface)
        self.cell_points.append(point_on_surface)
        print len(self.cell_points)

    def hold_command(self):
        print "hold invoked"
        print mc.draggerContext(self.context_name, q=True, plane=True)

    def drag_command(self):
        print   "drag invoked"
        print self.context_name
        print   mc.draggerContext(self.context_name, q=True, dragPoint=True)
        print "nearest surface point : \n"
        print get_surface_pos_from_mouse(self.samson_surface)

    def release_command(self):
        print "release invoked"
        print mc.draggerContext(self.context_name, q=True, cs=True)

    def finalize_command(self):
        print "finalize invoked"
        mesh.create_face_from_positions(self.cell_points)
        mc.makeLive(none=True)




def add_cell(surface):
    print "adding cell to surface: " + surface
    mc.setToolTo(AddCellContext(surface=surface).context_name)