'''
MAIN
'''


'''
Maya Intrinsic Imports
'''
import maya.cmds as mc
import maya.api.OpenMaya as om
import pymel.core as pm

'''
Necessary Modules
'''
import utils as utils


def test_print(message):
    print message


def print_selection():
    print Utilities.selection.fetch_selection(cmds=True, shape=True)