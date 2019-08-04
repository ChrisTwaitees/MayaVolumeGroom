from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import pymel.core as pm

from ..utils import pyside
reload(pyside)
from ..utils import selection
reload(selection)
from ..utils import environment
reload(environment)
from ..core import voronoi
from ..core import guides
from ..core import cells
reload(cells)


# setting up environment for Samson
environment.load_plugins()


class SamsonUIMain(pyside.SimpleToolWindow):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(logger=False, tool_name="SAMSON")
        self.create_layout()
        self.create_widgets()

    def create_layout(self):
        # creating layouts

        # Scalp
        self.scalp_widget = pyside.SimplePanelledVBoxWidget()
        self.addWidget(self.scalp_widget)

        # Centerguide
        self.centerguide_widget = pyside.SimplePanelledVBoxWidget()
        self.addWidget(self.centerguide_widget)

        # Tube
        self.tube_widget = pyside.SimplePanelledVBoxWidget()
        self.addWidget(self.tube_widget)

        # Curves
        self.guides_widget = pyside.SimplePanelledVBoxWidget()
        self.addWidget(self.guides_widget)

    def create_widgets(self):

        # SCALP widgets
            #header
        self.scalp_widget.addWidget(pyside.create_label("SCALP"))
            # surface
        self.scalp_surface_button = pyside.SimpleLabelledButton(button_label="Select Mesh",
                                                                button_callback = self.set_scalp_surface_callback,
                                                                tip="Select mesh you wish to groom.")
        self.scalp_widget.addWidget(self.scalp_surface_button)
            # add new cell
        add_cell_bttn = pyside.SimpleLabelledButton(label="Add New Cell", tip="Draw new Cell on Samson Surface.",
                                                    button_callback=self.add_new_cell_callback,
                                                    standard_icon_name="Add", reverse=True)
        self.scalp_widget.addWidget(add_cell_bttn)

            # voronoi
        voronoi_bttn = pyside.create_button(text="Voronoi Mesh", tip="Cuts the mesh into voronoi patterned cells."
                                                                     "Number of cells defined by user.",
                                            callback=self.voronoi_callback)
        self.scalp_widget.addWidget(voronoi_bttn)

        ## ----------------------------------------##

        # CENTERGUIDE widgets
            # header
        self.centerguide_widget.addWidget(pyside.create_label("CENTERGUIDES"))
            # add guide
        self.add_guide_bttn = pyside.SimpleButtonLineEdit(button_label="Add Guide",
                                                          button_callback=self.add_guide_callback,
                                                          tip="Opens Add Guide Context Tool",
                                                          label="5", reverse=True)
        self.centerguide_widget.addWidget(self.add_guide_bttn)
            # rebuild guide
        self.rebuild_guide_bttn = pyside.SimpleButtonLineEdit(button_label="Resample Guides",
                                                              button_callback=self.rebuild_guides_callback,
                                                              tip="Rebuilds Selected Guides",
                                                              label="8", reverse=True)
        self.centerguide_widget.addWidget(self.rebuild_guide_bttn)
            # select all guides
        select_all_guides_bttn = pyside.create_button(text="Select all Guides", tip="Selects all Samson centerguides.",
                                                      callback=self.select_all_guides_callback)
        self.centerguide_widget.addWidget(select_all_guides_bttn)

        ## ----------------------------------------##

        # TUBE widgets
            # header
        self.tube_widget.addWidget(pyside.create_label("TUBE"))
            # new tube
        new_tube_bttn = pyside.create_button(text="Add Tube",
                                             callback=self.add_tube_callback,
                                             tip="Creates Samson Tube Volume from either centerguide or "
                                                 "new cell.")
        self.tube_widget.addWidget(new_tube_bttn)

        ## ----------------------------------------##

        # GUIDES widgets
            # header
        self.guides_widget.addWidget(pyside.create_label("GENERATE GUIDES"))

        self.build_guides_bttn = pyside.SimpleButtonLineEdit(button_label="Build Guides",
                                                              button_callback=self.build_guides_callback,
                                                              tip="Creates guides from Center Guide or Tube",
                                                              label="8", reverse=True)

        self.guides_widget.addWidget(self.build_guides_bttn)

    # getters
    def get_surface(self):
        return self.scalp_surface_button.label.text()

    # CALLBACKS

    # Scalp callbacks
    def set_scalp_surface_callback(self):
        scalp = selection.fetch_selection(shape=True)
        if scalp:
            self.scalp_surface_button.set_text(scalp)
        else:
            self.scalp_surface_button.set_text("No Mesh Selected")

    def add_new_cell_callback(self):
        cells.add_cell(self.get_surface())

    def voronoi_callback(self):
        pm.select(self.get_surface())
        voronoi.main()

    # Center Guides callbacks
    def add_guide_callback(self):
        guides(self.get_surface(), int(self.add_guide_bttn.get_entry()))

    def rebuild_guides_callback(self):
        print "rebuild guides callback"

    def select_all_guides_callback(self):
        print "selecting all center guides"

    # Tubes callback
    def add_tube_callback(self):
        print "add Tube call back"

    # Guides callback
    def build_guides_callback(self):
        num_guides = self.build_guides_bttn.get_entry()
        print num_guides





def main():
    SamsonUIMain().run()


