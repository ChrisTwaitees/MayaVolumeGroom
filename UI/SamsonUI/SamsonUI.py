print "refresh successful"
import maya.cmds as mc
from maya import OpenMayaUI as omui
from maya.app.general.mayaMixin import MayaQDockWidget
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from shiboken2 import wrapInstance

from PySide2 import __version__
import PySide2.QtCore as qc
import PySide2.QtGui as qg
import PySide2.QtWidgets as qw

from Source import main as STB
from UI.SamsonUI import SamsonUI_utils as utils


class SamsonUIMain(MayaQWidgetDockableMixin, qw.QDialog):
    toolName = 'SamsonUI'

    def __init__(self, parent=None):
        # Delete any previous instances that is detected. Do this before parenting self to main window!
        self.deleteInstances()

        super(self.__class__, self).__init__(parent=parent)

        mayaMainWindowPtr = omui.MQtUtil.mainWindow()
        self.mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), qw.QDialog)
       # self.setObjectName(__class__.toolName)

        # Setup window's properties
        self.setWindowFlags(qc.Qt.Window)
        self.setWindowTitle('SAMSON')
        self.setModal(False)
        self.setMinimumHeight(700)
        self.setMinimumWidth(300)

        self.setLayout(qw.QVBoxLayout())
        self.layout().setContentsMargins(5, 5, 5, 5)
        self.layout().setSpacing(7)
        qw.QApplication.setStyle(qw.QStyleFactory.create('Plastique'))

        # adding frames for each step

        scalp_frame = qw.QFrame()
        scalp_frame.setFrameStyle(qw.QFrame.Panel | qw.QFrame.Raised)

        centerguide_frame = qw.QFrame()
        centerguide_frame.setFrameStyle(qw.QFrame.Panel | qw.QFrame.Raised)

        tube_frame = qw.QFrame()
        tube_frame.setFrameStyle(qw.QFrame.Panel | qw.QFrame.Raised)

        generatecurves_frame = qw.QFrame()
        generatecurves_frame.setFrameStyle(qw.QFrame.Panel | qw.QFrame.Raised)

        # creating layouts

        scalplayout = qw.QVBoxLayout()
        scalplayout.setContentsMargins(5, 5, 5, 5)
        scalplayout.setAlignment(qc.Qt.AlignVCenter)

        centerguidelayout = qw.QVBoxLayout()
        centerguidelayout.setAlignment(qc.Qt.AlignVCenter)

        tubelayout = qw.QVBoxLayout()
        tubelayout.setAlignment(qc.Qt.AlignVCenter)

        gencurveslayout = qw.QVBoxLayout()
        gencurveslayout.setAlignment(qc.Qt.AlignVCenter)

        # setting layouts to frames

        scalp_frame.setLayout(scalplayout)
        centerguide_frame.setLayout(centerguidelayout)
        tube_frame.setLayout(tubelayout)
        generatecurves_frame.setLayout(gencurveslayout)

        # widgets

        bold_font = qg.QFont()
        bold_font.setBold(True)

        # SCALP widgets

        scalp_header = qw.QLabel('SCALP')
        scalp_header.setFont(bold_font)
        scalplayout.addWidget(scalp_header)

        scalpvoronoilayout = qw.QFormLayout()
        scalpvoronoilayout.setAlignment(qc.Qt.AlignVCenter)
        scalplayout.addLayout(scalpvoronoilayout)

        voronoi_surface_entry = qw.QLineEdit()
        voronoi_surface_entry.setClearButtonEnabled(True)
        voronoi_surface_entry.insert("Select Surface")
        voronoi_surface_button = qw.QPushButton('<<')
        scalpvoronoilayout.addRow(voronoi_surface_entry, voronoi_surface_button)

        voronoi_bttn = qw.QPushButton('Voronoi Surface')
        voronoi_densitycount = qw.QLineEdit()
        voronoi_densitycount.setMaxLength(3)
        voronoi_densitycount.setClearButtonEnabled(True)
        voronoi_densitycount.insert('50')
        voronoi_densitycount.setSizePolicy(qw.QSizePolicy.Minimum, qw.QSizePolicy.Minimum)
        scalpvoronoilayout.addRow(voronoi_bttn, voronoi_densitycount)

        voronoi_bttn.clicked.connect(lambda: STB.utils.Voronoi(int(voronoi_densitycount.text())))

        refreshscalp_bttn = qw.QPushButton('Refresh Scalp')
        scalplayout.addWidget(refreshscalp_bttn)
        refreshscalp_bttn.clicked.connect(lambda: STB.refresh_scalp())

        exportregionmap_bttn = qw.QPushButton('Export Region Map')
        scalplayout.addWidget(exportregionmap_bttn)

        # CENTERGUIDE widgets

        centerguide_header = qw.QLabel('CENTERGUIDE')
        centerguide_header.setFont(bold_font)
        centerguidelayout.addWidget(centerguide_header)

        generatecurve_layout = qw.QFormLayout()
        generatecurve_layout.setAlignment(qc.Qt.AlignVCenter)
        centerguidelayout.addLayout(generatecurve_layout)

        generatecurve_bttn = qw.QPushButton('Generate New Curve')
        generatecurve_densitycount = qw.QLineEdit()
        generatecurve_densitycount.setMaxLength(3)
        generatecurve_densitycount.insert('10')
        generatecurve_densitycount.setSizePolicy(qw.QSizePolicy.Minimum, qw.QSizePolicy.Minimum)
        generatecurve_bttn.clicked.connect(lambda: STB.curvefromsurface(int(generatecurve_densitycount.text()),
                                                                        self.descriptions_dropdown.currentText()))

        generatecurve_layout.addRow(generatecurve_bttn, generatecurve_densitycount)

        editcurve_bttn = qw.QPushButton('Edit Curve')
        centerguidelayout.addWidget(editcurve_bttn)
        editcurve_bttn.clicked.connect(lambda: STB.editcenterguide())

        savechangescurve_bttn = qw.QPushButton('Save Changes')
        centerguidelayout.addWidget(savechangescurve_bttn)
        savechangescurve_bttn.clicked.connect(lambda: STB.savecenterguide_changes())

        rebuildcurvelayout = qw.QFormLayout()
        rebuildcurvelayout.setAlignment(qc.Qt.AlignVCenter)
        centerguidelayout.addLayout(rebuildcurvelayout)

        rebuildcurve_bttn = qw.QPushButton('Rebuild Curve')

        rebuildcurve_densitycount = qw.QLineEdit()
        rebuildcurve_densitycount.setMaxLength(3)
        rebuildcurve_densitycount.insert('8')
        rebuildcurve_densitycount.setSizePolicy(qw.QSizePolicy.Minimum, qw.QSizePolicy.Minimum)
        rebuildcurve_bttn.clicked.connect(lambda: STB.rebuildcurve(int(rebuildcurve_densitycount.text())))
        rebuildcurvelayout.addRow(rebuildcurve_bttn, rebuildcurve_densitycount)

        centerguidelayout.addLayout(rebuildcurvelayout)

        selectallcurves_bttn = qw.QPushButton('Select All CenterGuides')
        centerguidelayout.addWidget(selectallcurves_bttn)
        selectallcurves_bttn.clicked.connect(lambda: STB.select_curves(self.descriptions_dropdown.currentText()))

        deletecurve_bttn = qw.QPushButton('Delete CenterGuide')
        centerguidelayout.addWidget(deletecurve_bttn)
        deletecurve_bttn.clicked.connect(lambda: STB.deleteclump())

        # TUBE widgetes

        tube_header = qw.QLabel('TUBE')
        tube_header.setFont(bold_font)
        tubelayout.addWidget(tube_header)

        generatenewtube_bttn = qw.QPushButton('Generate New Tube')
        tubelayout.addWidget(generatenewtube_bttn)
        generatenewtube_bttn.clicked.connect(lambda: STB.attachtube(0.8))

        edittube_bttn = qw.QPushButton('Edit Tube')
        tubelayout.addWidget(edittube_bttn)
        edittube_bttn.clicked.connect(lambda: STB.edittube())

        # savechangestube_bttn = qw.QPushButton('Save Changes')
        # tubelayout.addWidget(savechangestube_bttn)

        selectalltubes_bttn = qw.QPushButton('Select All Tubes')
        tubelayout.addWidget(selectalltubes_bttn)
        selectalltubes_bttn.clicked.connect(lambda: STB.select_tubes(self.descriptions_dropdown.currentText()))

        deletetube_bttn = qw.QPushButton('Delete Tube')
        tubelayout.addWidget(deletetube_bttn)
        deletetube_bttn.clicked.connect(lambda: STB.deletetube())

        # CURVE GEN widgets

        gencurves_header = qw.QLabel('GENERATE CURVES')
        gencurves_header.setFont(bold_font)
        gencurveslayout.addWidget(gencurves_header)

        generateguidecurveslayout = qw.QFormLayout()
        generateguidecurveslayout.setAlignment(qc.Qt.AlignVCenter)
        gencurveslayout.addLayout(generateguidecurveslayout)

        generate_onlyexternalguides_check = qw.QCheckBox('Generate Only Outer Guides')
        gencurveslayout.addWidget(generate_onlyexternalguides_check)

        # generate_onlyexternalguides_check.stateChanged.connect()

        filltube_bttn = qw.QPushButton('Fill Selected Tube With Curves')

        filltube_densitycount = qw.QLineEdit()
        filltube_densitycount.setMaxLength(3)
        filltube_densitycount.insert('2')
        filltube_densitycount.setSizePolicy(qw.QSizePolicy.Minimum, qw.QSizePolicy.Minimum)
        filltube_bttn.clicked.connect(lambda: STB.gencurvesfromtube(numberofcurves=int(filltube_densitycount.text()),
                                                                    onlyoutercurves=generate_onlyexternalguides_check.isChecked()))

        generateguidecurves_bttn = qw.QPushButton('Generate Guide Curves')

        gencurves_densitycount = qw.QLineEdit()
        gencurves_densitycount.setMaxLength(3)
        gencurves_densitycount.setClearButtonEnabled(True)
        gencurves_densitycount.insert('2')
        gencurves_densitycount.setSizePolicy(qw.QSizePolicy.Minimum, qw.QSizePolicy.Minimum)
        generateguidecurves_bttn.clicked.connect(lambda: STB.gencurvesglobal(int(gencurves_densitycount.text()),
                                                                             onlyoutercurves=generate_onlyexternalguides_check.isChecked()))

        generateguidecurveslayout.addRow(filltube_bttn, filltube_densitycount)
        generateguidecurveslayout.addRow(generateguidecurves_bttn, gencurves_densitycount)

        deleteguidecurves_bttn = qw.QPushButton("Delete Selected Tube's Guide Curves")
        gencurveslayout.addWidget(deleteguidecurves_bttn)
        deleteguidecurves_bttn.clicked.connect(lambda: STB.deleteguidecurves())

        deleteallguidecurves_bttn = qw.QPushButton("Delete All Guide Curves")
        gencurveslayout.addWidget(deleteallguidecurves_bttn)
        deleteallguidecurves_bttn.clicked.connect(lambda: STB.remove_allguidecurves())

        extractguides_bttn = qw.QPushButton('Extract Guides')
        gencurveslayout.addWidget(extractguides_bttn)
        extractguides_bttn.clicked.connect(lambda: STB.extract_guide_curves())

        #   adding frames

        self.layout().addWidget(scalp_frame)
        self.layout().addWidget(centerguide_frame)
        self.layout().addWidget(tube_frame)
        self.layout().addWidget(generatecurves_frame)

    # functions

    def deleteInstances(self):
        mayaMainWindowPtr = omui.MQtUtil.mainWindow()
        mayaMainWindow = wrapInstance(long(mayaMainWindowPtr),
                                      qw.QMainWindow)  # Important that it's QMainWindow, and not QWidget/QDialog
        # Go through main window's children to find any previous instances
        for obj in mayaMainWindow.children():
            if type(obj) == MayaQDockWidget:
                # if obj.widget().__class__ == self.__class__: # Alternatively we can check with this, but it will fail if we re-evaluate the class
                if obj.widget().objectName() == self.__class__.toolName:  # Compare object names
                    # If they share the same name then remove it
                    print 'Deleting instance {0}'.format(obj)
                    mayaMainWindow.removeDockWidget(
                        obj)  # This will remove from right-click menu, but won't actually delete it! ( still under mainWindow.children() )
                    # Delete it for good
                    obj.setParent(None)
                    obj.deleteLater()

    def dockCloseEventTriggered(self):
        self.deleteInstances()


def DockableWidgetUIScript(restore=False):
    global customMixinWindow

    ''' When the control is restoring, the workspace control has already been created and
        all that needs to be done is restoring its UI.
    '''
    if restore == True:
        # Grab the created workspace control with the following.
        restoredControl = omui.MQtUtil.getCurrentParent()

    customMixinWindow = SamsonUIMain()
    if customMixinWindow is None:
        # Create a custom mixin widget for the first time
        # customMixinWindow = DockableWidget()
        customMixinWindow.setObjectName('SamsonUI')

    if restore == True:
        # Add custom mixin widget to the workspace control
        mixinPtr = omui.MQtUtil.findControl(customMixinWindow.objectName())
        omui.MQtUtil.addWidgetToMayaLayout(long(mixinPtr), long(restoredControl))
    else:
        # Create a workspace control for the mixin widget by passing all the needed parameters. See workspaceControl command documentation for all available flags.
        customMixinWindow.show(dockable=True, uiScript='DockableWidgetUIScript(restore=True)')

    return customMixinWindow


def main():
    if not 'SamsonUI' in globals():
        customMixinWindow = None
    ui = DockableWidgetUIScript()
    return ui


