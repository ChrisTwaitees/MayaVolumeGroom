"""
Samson set up
"""

import os

import maya.cmds as mc

def load_plugins():
    plugin_folder = os.path.join(os.path.dirname(__file__).replace("utils", ""), "plugin")
    python_plugin_dir = os.path.join(plugin_folder, "python")
    print python_plugin_dir
    if os.path.exists(python_plugin_dir):
        for plugin in os.listdir(python_plugin_dir):
            try:
                mc.loadPlugin(os.path.join(python_plugin_dir, plugin), quiet=True)
                print "Succefully loaded plugin: %s " % plugin.split(".")[0]
            except:
                print "could not load: %s plugin" % plugin
    else:
        raise ImportError("Cannot Find plugins/ folder at root of Samson installation.")