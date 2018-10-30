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
import utilities as utils


def test_print(message):
    print message


def print_selection():
    print utils.selection.fetch_selection(cmds=True, shape=True)