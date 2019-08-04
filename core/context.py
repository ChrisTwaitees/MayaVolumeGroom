import maya.cmds as mc


class SamsonContext(object):
    def __init__(self):
        self.context_name = "SamsonContext"

    def create_context(self):
        self.delete_existing_contexts()
        mc.draggerContext(self.context_name, name=self.context_name, releaseCommand=self.release_command,
                          cursor="crossHair", pressCommand=self.press_command, prePressCommand=self.pre_press_command,
                          holdCommand=self.hold_command, initialize=self.intialize_command, dragCommand=self.drag_command,
                          finalize=self.finalize_command)

    def intialize_command(self):
        print "intialization invoked"

    def pre_press_command(self):
        print "Pre_press command invoked"

    def press_command(self):
        print "press invoked"

    def hold_command(self):
        print "hold invoked"

    def drag_command(self):
        print   "drag invoked"

    def release_command(self):
        print "release invoked"

    def finalize_command(self):
        print "finalize invoked"

    def delete_existing_contexts(self):
        if mc.draggerContext(self.context_name, exists=True):
            mc.deleteUI(self.context_name)