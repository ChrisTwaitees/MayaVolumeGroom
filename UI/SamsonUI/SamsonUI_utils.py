import maya.cmds as mc
from Source import main as src

def fetchselection():
    return src.utils.selection.fetch_selection(shape=True, cmds=True)