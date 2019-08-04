import pymel.core as pm

def _null(*args):
    pass


class SamsonShelf(object):
    '''A simple class to build shelves in maya. Since the build method is empty,
    it should be extended by the derived class to build the necessary shelf elements.
    By default it creates an empty shelf called "customShelf".'''

    def __init__(self, name="Samson", icon_dir=""):
        self.name = name

        if len(icon_dir):
            self.iconPath = icon_dir
        else:
            self.iconPath = ""

        self.labelBackground = (0, 0, 0, 0)
        self.labelColour = (.9, .9, .9)

        self._cleanOldShelf()
        self.shelfRoot = self._createShelf()

        pm.setParent(self.shelfRoot)

    def build(self):
        '''This method should be overwritten in derived classes to actually build the shelf
        elements. Otherwise, nothing is added to the shelf.'''
        pass

    def _createShelf(self):
        return pm.shelfLayout(self.name, p="ShelfLayout")

    def addButton(self, label, icon="commandButton.png", command=_null, doubleCommand=_null):
        '''Adds a shelf button with the specified label, command, double click command and image.'''
        pm.setParent(self.name)
        if icon:
            icon = self.iconPath + icon
        pm.shelfButton(width=37, height=37, image=icon, l=label, command=command, dcc=doubleCommand, imageOverlayLabel=label, olb=self.labelBackground, olc=self.labelColour)

    def addMenuItem(self, parent, label, command=_null, icon=""):
        '''Adds a shelf button with the specified label, command, double click command and image.'''
        if icon:
            icon = self.iconPath + icon
        return pm.menuItem(p=parent, l=label, c=command, i="")

    def addSubMenu(self, parent=None, label="", icon=None):
        '''Adds a sub menu item with the specified label and icon to the specified parent popup menu.'''
        if icon:
            icon = self.iconPath + icon
        if parent is None:
            return pm.menuItem(parent=self.shelfRoot, l=label, i=icon, subMenu=1)
        else:
            return pm.menuItem(parent=parent, l=label, i=icon, subMenu=1)

    def addSeparator(self, parent=None, horizontal=False):
        if parent:
            pm.separator(parent=parent, horizontal=horizontal)
        else:
            pm.separator(parent=self.shelfRoot, horizontal=horizontal)

    def addPopUpMenu(self, button):
        pm.setParent(button)
        return pm.popupMenu(b=1)

    def _cleanOldShelf(self):
        '''Checks if the shelf exists and empties it if it does or creates it if it does not.'''
        if pm.shelfLayout(self.name, ex=1):
            if pm.shelfLayout(self.name, q=1, ca=1):
                for each in pm.shelfLayout(self.name, q=1, ca=1):
                    pm.deleteUI(each)
            pm.deleteUI(self.name)

###################################################################################
'''This is an example shelf.'''
# class customShelf(_shelf):
#     def build(self):
#         self.addButon(label="button1")
#         self.addButon("button2")
#         self.addButon("popup")
#         p = cmds.popupMenu(b=1)
#         self.addMenuItem(p, "popupMenuItem1")
#         self.addMenuItem(p, "popupMenuItem2")
#         sub = self.addSubMenu(p, "subMenuLevel1")
#         self.addMenuItem(sub, "subMenuLevel1Item1")
#         sub2 = self.addSubMenu(sub, "subMenuLevel2")
#         self.addMenuItem(sub2, "subMenuLevel2Item1")
#         self.addMenuItem(sub2, "subMenuLevel2Item2")
#         self.addMenuItem(sub, "subMenuLevel1Item2")
#         self.addMenuItem(p, "popupMenuItem3")
#         self.addButon("button3")
# customShelf()
###################################################################################