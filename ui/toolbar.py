import pymel.core as pm

def _null(*args):
    pass

class SamsonToolBar(object):
    '''A simple class to build toolbars to Maya's MainWindow.
    Since the build method is empty,
    it should be extended by the derived class to build the necessary shelf elements.
    By default it creates an empty toolbar called "RFLCustomToolBar".'''
    def __init__(self, name="Samson", icon_dir="", tear_off=True):
        # Name of Toolbar DropDown
        self.name = name
        # Get Maya's Main Window
        self.parent = pm.melGlobals["gMainWindow"]
        # Getting Directory for Icons
        if len(icon_dir):
            self.iconDir = icon_dir
        else:
            self.iconDir = ""

        self._cleanOldMenu()

        self.menuRoot = self._createMenu(tear_off=tear_off)
        self.build()

    @staticmethod
    def addSeparator(parent):
        pm.menuItem(parent=parent, divider=True)

    def build(self):
        '''This method should be overwritten in derived classes to actually build the shelf
        elements. Otherwise, nothing is added to the shelf.'''
        pass

    def _createMenu(self, tear_off):
        MainMayaWindow = pm.melGlobals['gMainWindow']
        return pm.menu(self.name, parent=MainMayaWindow)

    def addMenuItem(self, parent, label, command=_null, icon=None, tear_off=True):
        '''Adds a shelf button with the specified label, command, double click command and image.'''
        if icon:
            icon = self.iconDir + icon
        else:
            icon = "dot.png"
        return pm.menuItem(p=parent, l=label, c=command, i=icon)

    def addSubMenu(self, parent, label, icon=None, tear_off=True):
        '''Adds a sub menu item with the specified label and icon to the specified parent popup menu.'''
        if icon:
            icon = self.iconDir + icon
        else:
            icon = "empty.png"
        return pm.menuItem(p=parent, l=label, i=icon, subMenu=1, tearOff=tear_off)

    def _cleanOldMenu(self):
        try:
            if pm.menu(self.name, exists=1):
                pm.deleteUI(self.name)
        except RuntimeError:
            pass






